import pytest
from datetime import datetime
from main import decode_metar, MetarReport, AtmosphericPhenomenaE, CloudsE

# Replace 'your_module_name' with the actual name of the module where your code resides.


@pytest.mark.parametrize("raw_report, expected_result", [
    ("METAR ABC 010101Z 09010KT 9999 SCT030 BKN050 25/M15 A3000 NOSIG", MetarReport(
        airport_code="ABC",
        observation_time=datetime(2022, 1, 1, 1, 1),
        wind_direction=90,
        wind_speed=10,
        visibility=9999,
        atmospheric_phenomena=[],
        clouds=[CloudsE.SCT, CloudsE.BKN],
        cloud_base=[3000, 5000],
        temperature=25,
        dew_point=-15,
        pressure=3000,
        significant_changes=False,
    )),
    # Additional test cases for valid METAR reports
    ("METAR ABC 010101Z 27030KT 9999 BR020 25/M15 A3000 NOSIG", MetarReport(
        airport_code="ABC",
        observation_time=datetime(2022, 1, 1, 1, 1),
        wind_direction=270,
        wind_speed=30,
        visibility=9999,
        atmospheric_phenomena=[AtmosphericPhenomenaE.BR],
        clouds=[CloudsE.SCT],
        cloud_base=[2000],
        temperature=25,
        dew_point=-15,
        pressure=3000,
        significant_changes=False,
    )),
    ("METAR ABC 010101Z 00000KT 9999 25/M15 A3000 NOSIG", MetarReport(
        airport_code="ABC",
        observation_time=datetime(2022, 1, 1, 1, 1),
        wind_direction=0,
        wind_speed=0,
        visibility=9999,
        atmospheric_phenomena=[],
        clouds=[],
        cloud_base=[],
        temperature=25,
        dew_point=-15,
        pressure=3000,
        significant_changes=False,
    )),
    ("METAR ABC 010101Z 36020G30KT 9999 25/M15 A3000 NOSIG", MetarReport(
        airport_code="ABC",
        observation_time=datetime(2022, 1, 1, 1, 1),
        wind_direction=360,
        wind_speed=20,
        wind_gusts=30,
        visibility=9999,
        atmospheric_phenomena=[],
        clouds=[],
        cloud_base=[],
        temperature=25,
        dew_point=-15,
        pressure=3000,
        significant_changes=False,
    )),
    # Test cases for invalid METAR reports
    ("METAR ABC", None),
    ("METAR ABC 010101Z", None),
    ("METAR ABC 010101Z 09010KT 9999", None),
    ("METAR ABC 010101Z 09010KT 9999 SCT030", None),
    # Additional test cases for edge cases, exceptions, etc.
])
def test_decode_metar(raw_report, expected_result):
    result = decode_metar(raw_report)
    assert result == expected_result


def test_decode_metar_invalid_input():
    result = decode_metar("Invalid METAR report")
    assert result is None


if __name__ == '__main__':
    pytest.main()
