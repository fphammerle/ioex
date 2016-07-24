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
            ur'(Z|[\+-]\d{2}:\d{2})$',
            loader.construct_yaml_str(node),
            )
        if timezone_match:
            loaded_dt = loaded_dt.replace(tzinfo = dateutil.tz.tz.tzutc())
    return loaded_dt

def add_yaml_timestamp_constructor(loader, tag = u'tag:yaml.org,2002:timestamp'):
    loader.add_constructor(tag, construct_yaml_timestamp)
