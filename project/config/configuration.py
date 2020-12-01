import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('../config.ini')

#Use as: config.get('iniSection', 'property.name');