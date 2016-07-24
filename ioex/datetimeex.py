import datetime
import dateutil.tz.tz
import re
try:
    import yaml
except ImportError:
    yaml = None

def construct_yaml_timestamp(loader, node):
    loaded_dt = loader.construct_yaml_timestamp(node)
    if type(loaded_dt) is datetime.datetime and loaded_dt.tzinfo is None:
        timezone_match = re.search(
            ur'(Z|(?P<sign>[\+-])(?P<h>\d{2}):(?P<m>\d{2}))$',
            loader.construct_yaml_str(node),
            )
        if timezone_match:
            # loader.construct_yaml_timestamp converts to UTC
            loaded_dt = loaded_dt.replace(tzinfo = dateutil.tz.tz.tzutc())
            timezone_attr = timezone_match.groupdict()
            if timezone_attr['h']:
                timezone = dateutil.tz.tz.tzoffset(
                        name = timezone_match.group(0),
                        offset = (int(timezone_attr['h']) * 60 + int(timezone_attr['m'])) * 60
                            * (-1 if timezone_attr['sign'] == '-' else 1),
                        )
                loaded_dt = loaded_dt.astimezone(timezone)
    return loaded_dt

def add_yaml_timestamp_constructor(loader, tag = u'tag:yaml.org,2002:timestamp'):
    loader.add_constructor(tag, construct_yaml_timestamp)
