from abc import abstractmethod
from collections import defaultdict
from datetime import datetime
from statistics import mean

from home_telemetry.config import SOLAX_DATETIME_FORMAT
from home_telemetry.models import Measurement, MeasurementType, PhaseCode, Source
from home_telemetry.request_retry import requests_retry_get


class BaseAdapter:
    def __init__(self):
        self.url: str
        self.source: Source | None = None
        self.seconds_between_updates: int = 5
        self.time_of_last_update: datetime = datetime(2000, 1, 1)
        self.aggregation_cache: dict = defaultdict(defaultdict(defaultdict(list).copy).copy)
        self.aggregation_period_seconds: int = 5 * 60
        self.time_of_last_aggregation: datetime = datetime.now()

    def __str__(self):
        return f"<{self.__class__.__name__}>"

    def get_data(self):
        seconds_since_last_update = (datetime.now() - self.time_of_last_update).total_seconds()
        if seconds_since_last_update > self.seconds_between_updates:
            response = requests_retry_get(self.url)
            self.time_of_last_update = datetime.now()
            return response

    @abstractmethod
    def measure(self) -> list[Measurement]:
        ...

    def aggregate(self, measurements: list[Measurement]) -> list[Measurement]:
        for measurement in measurements:
            self.aggregation_cache[measurement.measurement_type][measurement.phasecode][measurement.description].append(
                measurement.value
            )

        # TODO: split this up
        seconds_since_last_aggregation = (datetime.now() - self.time_of_last_aggregation).total_seconds()
        if seconds_since_last_aggregation < self.aggregation_period_seconds:
            return []
        else:
            aggregated_measurements = []
            for measurement_type, cache_per_type in self.aggregation_cache.items():
                for phasecode, cache_per_phasecode in cache_per_type.items():
                    for description, measurements_per_phasecode in cache_per_phasecode.items():
                        aggregated_measurements.append(
                            Measurement(
                                source=self.source,
                                measurement_type=measurement_type,
                                value=mean(measurements_per_phasecode),
                                description=description,
                                phasecode=phasecode,
                            )
                        )
            self.aggregation_cache = defaultdict(defaultdict(defaultdict(list).copy).copy)

            return aggregated_measurements


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
            ),
            Measurement(
                source=self.source,
                value=float(data["active_voltage_l1_v"]),
                measurement_type=MeasurementType.VOLTAGE,
                phasecode=PhaseCode.L1,
            ),
            Measurement(
                source=self.source,
                value=float(data["active_voltage_l2_v"]),
                measurement_type=MeasurementType.VOLTAGE,
                phasecode=PhaseCode.L2,
            ),
            Measurement(
                source=self.source,
                value=float(data["active_voltage_l1_v"]),
                measurement_type=MeasurementType.VOLTAGE,
                phasecode=PhaseCode.L3,
            ),
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
