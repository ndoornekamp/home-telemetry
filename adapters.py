from datetime import datetime
from pprint import pprint

from config import (
    P1_IP_ADDRESS,
    SOLAX_DATETIME_FORMAT,
    SOLAX_SERIAL_NUMBER,
    SOLAX_TOKEN_ID,
)
from models import Measurement, MeasurementType, PhaseCode, Source
from request_retry import requests_retry_get


class BaseAdapter:
    def __init__(self):
        self.url = None

    def get_data(self):
        assert self.url is not None
        return requests_retry_get(self.url)


class HeishamonAdapter(BaseAdapter):
    def __init__(self):
        self.url = "http://heishamon.local/json"
        self.source = Source.HEISHAMON

    def measure(self) -> list[Measurement]:
        response = self.get_data().json()["heatpump"]
        measurements = [
            Measurement(
                source=Source.HEISHAMON,
                measurement_type=MeasurementType.FLOW,
                value=[d for d in response if d["Name"] == "Pump_Flow"][0]["Value"],
                description="Pump flow",
            ),
            Measurement(
                source=Source.HEISHAMON,
                measurement_type=MeasurementType.TEMPERATURE,
                value=[d for d in response if d["Name"] == "Main_Inlet_Temp"][0]["Value"],
                description="Main inlet",
            ),
            Measurement(
                source=Source.HEISHAMON,
                measurement_type=MeasurementType.TEMPERATURE,
                value=[d for d in response if d["Name"] == "Main_Outlet_Temp"][0]["Value"],
                description="Main outlet",
            ),
            Measurement(
                source=Source.HEISHAMON,
                measurement_type=MeasurementType.TEMPERATURE,
                value=[d for d in response if d["Name"] == "Main_Target_Temp"][0]["Value"],
                description="Main target",
            ),
            Measurement(
                source=Source.HEISHAMON,
                measurement_type=MeasurementType.TEMPERATURE,
                value=[d for d in response if d["Name"] == "DHW_Temp"][0]["Value"],
                description="DHW actual",
            ),
            Measurement(
                source=Source.HEISHAMON,
                measurement_type=MeasurementType.TEMPERATURE,
                value=[d for d in response if d["Name"] == "DHW_Target_Temp"][0]["Value"],
                description="DHW target",
            ),
        ]

        return measurements


class P1Adapter(BaseAdapter):
    def __init__(self, ip_address: str):
        self.url = f"http://{ip_address}/api/v1/data"
        self.source = Source.HOMEWIZARD_P1

    def measure(self) -> list[Measurement]:
        response = self.get_data().json()

        return [
            Measurement(
                source=self.source,
                value=float(response["active_power_w"]),
                measurement_type=MeasurementType.POWER,
                phasecode=PhaseCode.ALL,
            )
        ]


class SolaxAdapter(BaseAdapter):
    def __init__(self, serial_number, token_id):
        self.url = (
            f"https://www.solaxcloud.com/proxyApp/proxy/api/getRealtimeInfo.do?tokenId={token_id}&sn={serial_number}"
        )
        self.source = Source.SOLAX

    def measure(self) -> list[Measurement]:
        response = self.get_data().json()["result"]

        return [
            Measurement(
                source=self.source,
                value=-float(response["acpower"]),  # Power production = negative
                timestamp=datetime.strptime(response["uploadTime"], SOLAX_DATETIME_FORMAT),
                measurement_type=MeasurementType.POWER,
                phasecode=PhaseCode.L3,  # Inverter is single phase (L3)
            )
        ]


if __name__ == "__main__":
    heishamon_adapter = HeishamonAdapter()
    p1_adapter = P1Adapter(ip_address=P1_IP_ADDRESS)
    solax_adapter = SolaxAdapter(serial_number=SOLAX_SERIAL_NUMBER, token_id=SOLAX_TOKEN_ID)

    for adapter in [heishamon_adapter, p1_adapter, solax_adapter]:
        test_response = adapter.measure()
        print(adapter.__class__)
        pprint(test_response)
        print("\n\n")
