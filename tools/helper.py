import re


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
    return re.sub(r"^['\"]*(.+?)['\"]*$", r"\1",
                  data.strip())
