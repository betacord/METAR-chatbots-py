from argparse import ArgumentParser
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

from metar.Metar import Metar, ParserError


class AtmosphericPhenomenaE(Enum):
    DZ = 'drizzle'
    RA = 'rain'
    SN = 'snow'
    SG = 'snow grains'
    IC = 'ice crystals'
    GR = 'hail'
    PL = 'ice pellets'
    GS = 'graupel'
    BR = 'mist'
    FG = 'fog'
    FU = 'smoke'
    VA = 'volcanic ash'
    SA = 'sand'
    HZ = 'haze'
    DU = 'widespread dust'
    SQ = 'squall'
    FC = 'funnel cloud'
    DS = 'duststorm'
    PO = 'dust'
    SS = 'sandstorm'


class CloudsE(Enum):
    SKC = '0/8'
    FEW = '1/8-2/8'
    SCT = '3/8-4/8'
    BKN = '5/8-7/8'
    OVC = '8/8'


@dataclass
class MetarReport:
    airport_code: str
    observation_time: datetime
    wind_direction: float
    wind_speed: float
    visibility: float
    atmospheric_phenomena: list[AtmosphericPhenomenaE]
    clouds: list[CloudsE]
    cloud_base: list[float]
    temperature: float
    dew_point: float
    pressure: float
    significant_changes: Optional[bool]


def decode_metar(raw_report: str) -> Optional[MetarReport]:
    try:
        parsed_report = Metar(raw_report)
        return MetarReport(
            airport_code=parsed_report.station_id,
            observation_time=parsed_report.time,
            wind_direction=parsed_report.wind_dir.value(),
            wind_speed=parsed_report.wind_speed.value(),
            visibility=parsed_report.vis.value(),
            atmospheric_phenomena=[AtmosphericPhenomenaE[weather[2]] for weather in parsed_report.weather],
            clouds=[CloudsE[clouds[0]] for clouds in parsed_report.sky],
            cloud_base=[base[1].value() for base in parsed_report.sky],
            temperature=parsed_report.temp.value(),
            dew_point=parsed_report.dewpt.value(),
            pressure=parsed_report.press.value(),
            significant_changes=parsed_report.trend() != 'NOSIG',
        )
    except ParserError:
        return None


def main() -> None:
    parser = ArgumentParser(
        prog='METAR parser',
        description='Script parsing METAR information.',
        epilog='Please read full description.',
    )
    parser.add_argument('metar')
    args = parser.parse_args()

    result = decode_metar(args.metar)
    print(result)


if __name__ == '__main__':
    main()
