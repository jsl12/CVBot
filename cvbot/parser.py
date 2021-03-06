import argparse

import shlex

"""
@CVBot cases Italy
@CVBot compare cases Italy US
@CVBot series deaths China
@CVBot series cases Iran

cases Italy --compare US
cases Italy --compare US --compare India
deaths...
recovered...
"""


class CVParseException(Exception):
    pass


def parse_args_shlex(parser: argparse.ArgumentParser, cmd_str: str):
    return parser.parse_args([s for s in shlex.split(cmd_str) if '<' not in s])


class ErrorCatchingArgumentParser(argparse.ArgumentParser):
    def exit(self, status=0, message=None):
        if status:
            raise CVParseException(''.join(message.split(':')[1:]).strip())
        exit(status)


CV_PARSER = ErrorCatchingArgumentParser()
CV_PARSER.add_argument('command', type=str, help='Type of stats to get: "cases", "deaths", or "recovered"')
CV_PARSER.add_argument('places', metavar='PLACE', type=str, nargs='+', help='Place to get stats from.')
CV_PARSER.add_argument('-s', '--series', action='store_true', help='Return a time series')
CV_PARSER.add_argument('-d', '--double', action='store_true', help='Return the doubling time')
CV_PARSER.add_argument('-n', '--normalize', action='store_true', help='Normalize each series to its start date')
CV_PARSER.add_argument('-p', '--plot', action='store_true', default=False, help='Normalize each series to its start date')

if __name__ == '__main__':
    CV_PARSER.parse_args(shlex.split('cases Italy US China'))
