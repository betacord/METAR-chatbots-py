import pytest
from datetime import datetime
from main import decode_metar, MetarReport, AtmosphericPhenomenaE, CloudsE

# Replace 'your_module_name' with the actual name of the module where your code resides.

@pytest.mark.parametrize("raw_report, expected_result", [
    # Valid METAR reports
    ("METAR AAA 010101Z 09010KT 9999 SCT030 BKN050 25/M15 A3000 NOSIG", MetarReport(
        airport_code="AAA",
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
    # Add more valid METAR reports here

    # Invalid METAR reports
    ("Invalid METAR report", None),
    ("METAR BBB 010101Z 09010KT 9999 SCT030 BKN050 25/M15 A3000", None),  # Missing NOSIG
    ("METAR CCC 010101Z 09010KT ABCD SCT030 BKN050 25/M15 A3000 NOSIG", None),  # Invalid wind speed
    # Add more invalid METAR reports here

    # Edge cases
    ("METAR DDD 010101Z 00000KT 9999 VA 00/M00 A1000 NOSIG", MetarReport(
        airport_code="DDD",
        observation_time=datetime(2022, 1, 1, 1, 1),
        wind_direction=0,
        wind_speed=0,
        visibility=9999,
        atmospheric_phenomena=[AtmosphericPhenomenaE.VA],
        clouds=[],
        cloud_base=[],
        temperature=0,
        dew_point=0,
        pressure=1000,
        significant_changes=False,
    )),
    # Add more edge cases here
])
def test_decode_metar(raw_report, expected_result):
    result = decode_metar(raw_report)
    assert result == expected_result

# Additional test cases for edge cases, exceptions, etc.

# For example, you might want to add tests for cases where ParserError is raised.
def test_decode_metar_invalid_input():
    result = decode_metar("Invalid METAR report")
    assert result is None


if __name__ == '__main__':
    pytest.main()
