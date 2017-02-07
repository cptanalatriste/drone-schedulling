"""
General-purpose utilities.
"""

LOAD_COMMAND = "L"
DELIVER_COMMAND = "D"


def split_and_cast(line):
    return [int(string_value) for string_value in line.split(" ")]
