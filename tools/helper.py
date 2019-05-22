import regex as re


def remove_wrapping_quotes(data):
    """Remove surrounding quotes (', ") in the provided string.

    Args:
        data: The string that would have the surrounding quotes removed.

    Returns:
        The string without the surrounding quotes

    """
    if data and isinstance(data, basestring):
        return re.sub(r"^['\"]*(.+?)['\"]*$", r"\1",
                      data.strip())


def extract_field_name(data, pattern, flag=None):
    """Extract string from the provided data.

    Extracts the needed column value from the data provided using regex
    provided as a parameter.

    Args:
        data: Input string where the needed field would be extracted
        pattern: Regex pattern that will be used to extract the needed field

    Returns:
        The needed field value extracted from the regex pattern

    """
    if flag:
        # Field has either single or multiple values.
        # If the field has multiple values it is wrapped in 2 double quotes
        # and if the field has a single value there is no quotes wrapped in it.
        # The regex expression below fulfill both conditions
        match = re.search(
            pattern + r'(("{1,2}.+?"{1,2})|([^\s]+))', data, flags=flag)
    else:
        match = re.search(
            pattern + r'(("{1,2}.+?"{1,2})|([^\s]+))', data)
    if match:
        field = remove_wrapping_quotes(match.group().strip())
        return field.strip()

    return ''


def extract_column_with_type(data, pattern):
    """Extract a certain column and disregard the column type.

    Certain columns has a type (name, any, group). The method
    extracts the value that sits next the type and disregard the
    type.

    Args:
        pattern: The regex pattern used for extracting the column value.
            Usually the pattern has the column name as the value usually
            sits right next to the column name.

    Returns:
        The needed field value extracted from the regex pattern

    """
    match = re.search(pattern, data, flags=re.M)
    if match:
        field = match.group().strip()
        if re.search(r'^any', field):
            return 'any'
        elif re.search(r'^name', field):
            pattern = r'(?<=name\s)'
            return extract_field_name(field, pattern)
        elif re.search(r'^group', field):
            pattern = r'(?<=group\s)'
            return extract_field_name(field, pattern)
        elif field is not None:
            if 'original' == field:
                return 'none'
            return field
    return ''
