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


def parse_args(parser: argparse.ArgumentParser, cmd_str: str, skip: int = 1):
    return parser.parse_args(shlex.split(cmd_str)[skip:])


class ErrorCatchingArgumentParser(argparse.ArgumentParser):
    def exit(self, status=0, message=None):
        if status:
            raise CVParseException(''.join(message.split(':')[1:]).strip())
        exit(status)


CV_PARSER = ErrorCatchingArgumentParser()
CV_PARSER.add_argument('command', type=str, help='Type of stats to get: cases, deaths, or recovered')
CV_PARSER.add_argument('country', type=str, help='Country to get stats from. Also works with US states')
CV_PARSER.add_argument('-s', '--series', action='store_true', help='Return a time series')
CV_PARSER.add_argument('-d', '--double', action='store_true', help='Return the doubling time')
CV_PARSER.add_argument('-c', '--compare', nargs='+', help='Compare to this place')
