import configparser

config = configparser.ConfigParser()

config.read('configs.ini')


def get_config_value(section, parameter, is_bool=False):
    if is_bool:
        return bool(int(config[section][parameter]))
    return config[section][parameter]


def set_config_value(section, parameter, value):
    if type(value) is bool:
        config[section][parameter] = str(int(value))
    else:
        config[section][parameter] = str(value)
    with open('configs.ini', 'w') as configfile:
        config.write(configfile)
