import re
from typing import Collection, Union


def regex_extract_value(
    regex_exp: str, *, string: str, first: bool = True
) -> Union[Collection, str]:
    """
    Given a regex expression, return the value that you want to extract
    :param regex_exp: the regex expression to extract the value
    :param string: the string
    :param first: if you only want the first element
    :return:
    """
    results = re.compile(regex_exp).search(string)

    return results.group(1) if first else list(results.groups())
