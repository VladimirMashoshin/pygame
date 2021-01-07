class Config:
    def __init__(self):
        self.dict = {}

    def get_value(self, param):
        return self.dict.get(param, None)

    def set_value(self, param, value):
        self.dict[param] = value

    def set_values(self, dict_values):
        for key in dict_values:
            self.dict[key] = dict_values[key]

    def get_all_values(self):
        return self.dict

    def get_list_values(self, *keys):
        return [self.get_value(param) for param in keys]
