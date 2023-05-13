import time
from datetime import datetime

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
        self.seconds_between_updates: int = 5
        self.time_of_last_update: datetime = datetime(2000, 1, 1)

    def __str__(self):
        return f"<{self.__class__.__name__}>"

    def get_data(self):
        assert self.url is not None

        seconds_since_last_update = (datetime.now() - self.time_of_last_update).total_seconds()
        if seconds_since_last_update > self.seconds_between_updates:
            response = requests_retry_get(self.url)
            self.time_of_last_update = datetime.now()
            return response


class HeishamonAdapter(BaseAdapter):
    def __init__(self):
        super().__init__()
        self.url = "http://heishamon.local/json"
        self.source = Source.HEISHAMON

    def measure(self) -> list[Measurement]:
        response = self.get_data()

        if not response:
            return []

        data = response.json()["heatpump"]
        measurements = [
            Measurement(
                source=Source.HEISHAMON,
                measurement_type=MeasurementType.FLOW,
                value=[d for d in data if d["Name"] == "Pump_Flow"][0]["Value"],
                description="Pump flow",
            ),
            Measurement(
                source=Source.HEISHAMON,
                measurement_type=MeasurementType.TEMPERATURE,
                value=[d for d in data if d["Name"] == "Main_Inlet_Temp"][0]["Value"],
                description="Main inlet",
            ),
            Measurement(
                source=Source.HEISHAMON,
                measurement_type=MeasurementType.TEMPERATURE,
                value=[d for d in data if d["Name"] == "Main_Outlet_Temp"][0]["Value"],
                description="Main outlet",
            ),
            Measurement(
                source=Source.HEISHAMON,
                measurement_type=MeasurementType.TEMPERATURE,
                value=[d for d in data if d["Name"] == "Main_Target_Temp"][0]["Value"],
                description="Main target",
            ),
            Measurement(
                source=Source.HEISHAMON,
                measurement_type=MeasurementType.TEMPERATURE,
                value=[d for d in data if d["Name"] == "DHW_Temp"][0]["Value"],
                description="DHW actual",
            ),
            Measurement(
                source=Source.HEISHAMON,
                measurement_type=MeasurementType.TEMPERATURE,
                value=[d for d in data if d["Name"] == "DHW_Target_Temp"][0]["Value"],
                description="DHW target",
            ),
        ]

        return measurements


class P1Adapter(BaseAdapter):
    def __init__(self, ip_address: str):
        super().__init__()
        self.url = f"http://{ip_address}/api/v1/data"
        self.source = Source.HOMEWIZARD_P1

    def measure(self) -> list[Measurement]:
        response = self.get_data()

        if not response:
            return []

        data = response.json()

        return [
            Measurement(
                source=self.source,
                value=float(data["active_power_w"]),
                measurement_type=MeasurementType.POWER,
                phasecode=PhaseCode.ALL,
            )
        ]


class SolaxAdapter(BaseAdapter):
    def __init__(self, serial_number, token_id):
        super().__init__()
        self.url = (
            f"https://www.solaxcloud.com/proxyApp/proxy/api/getRealtimeInfo.do?tokenId={token_id}&sn={serial_number}"
        )
        self.source = Source.SOLAX
        self.seconds_between_updates: int = 5 * 60

    def measure(self) -> list[Measurement]:
        response = self.get_data()

        if not response:
            return []

        try:
            data = response.json()["result"]
        except KeyError:
            print(response.json())
            self.time_of_last_update = datetime.now()
            return []

        return [
            Measurement(
                source=self.source,
                value=-float(data["acpower"]),  # Power production = negative
                timestamp=datetime.strptime(data["uploadTime"], SOLAX_DATETIME_FORMAT),
                measurement_type=MeasurementType.POWER,
                phasecode=PhaseCode.L3,  # Inverter is single phase (L3)
            )
        ]


if __name__ == "__main__":
    heishamon_adapter = HeishamonAdapter()
    p1_adapter = P1Adapter(ip_address=P1_IP_ADDRESS)
    solax_adapter = SolaxAdapter(serial_number=SOLAX_SERIAL_NUMBER, token_id=SOLAX_TOKEN_ID)

    for _ in range(10):
        for adapter in [heishamon_adapter, p1_adapter]:
            test_response = adapter.measure()
            print(f"Retrieved {len(test_response)} measurements from {adapter}")

        time.sleep(1)
