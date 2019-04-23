import regex as re


def remove_wrapping_quotes(data):
    """ Removes surrounding quotes (', ") in the provided string

    Parameters
    ----------
    data : str
        The string that would have the surrounding quotes removed.

    Returns
    -------
    string
        The string without the surrounding quotes
    """
    if data and isinstance(data, basestring):
        return re.sub(r"^['\"]*(.+?)['\"]*$", r"\1",
                      data.strip())


def extract_field_name(data, pattern, flag=None):
    """ Extracts a string from the provided input using regex
    provided as a parameter

    Parameters
    ----------
    data : str
        Input string where the needed field would be extracted

    pattern : str
        Regex pattern that will be used to extract the needed field

    Returns
    -------
    string
        The needed field extracted from the regex pattern
    """
    if flag:
        # Field has either single or multiple values.
        # If the field has multiple values it is wrapped in 2 double quotes
        # and if the field has a single value there is no quotes wrapped in it.
        # The regex expression below fulfill both conditions
        match = re.search(
            pattern + r'(("{1,2}.+"{1,2})|([^\s]+))', data, flags=flag)
    else:
        match = re.search(
            pattern + r'(("{1,2}.+"{1,2})|([^\s]+))', data)
    if match:
        field = remove_wrapping_quotes(match.group().strip())
        return field.strip()

    return ''
