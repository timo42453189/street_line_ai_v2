import configparser

class Configuarator:
    def __init__(self, path):
        self.path = path
        self.config = configparser.ConfigParser()
        self.config.read(self.path)
        self.config_dict = {}
    
    def read_config(self):
        for section in self.config.sections():
            for option in self.config.options(section):
                self.config_dict[option] = self.config.get(section, option)
        return self.config_dict