import configparser


def get_int(key):
    config = configparser.ConfigParser()
    config.read('config')
    return config.getint('config', key)

def get_float(key):
    config = configparser.ConfigParser()
    config.read('config')
    return config.getfloat('config', key)
