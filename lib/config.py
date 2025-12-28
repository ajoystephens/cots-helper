import configparser

from lib.creature import (
    get_creature_names_of_type_by_cr_from_json,
)

CONFIG_FILENAME = 'config.ini'

class Config:
    def __init__(self):
        self._config = configparser.ConfigParser()

    def load(self):
        self._config.read(CONFIG_FILENAME)

    def save(self):
        with open(CONFIG_FILENAME, 'w') as configfile:
            self._config.write(configfile)

    def _get_config_value(self,keys,default):
        self.load()
        c = self._config
        for k in keys:
            if k in c: c=c[k]
            else: return default
        return c
    
    def _set_config_value(self,keys,value):
        self.load()
        # TODO make more elegant, right no only works for 2 keys
        if keys[0] not in self._config: self._config[keys[0]] = {}
        self._config[keys[0]][keys[1]] = str(value)
        self.save()

    def get_mighty_summoner(self,default=False):
        keys = ['class_abilities','mighty_summoner']

        value = self._get_config_value(keys,default)
        value = eval(value)
        return(value)
    
    def set_mighty_summoner(self,value):
        # self.load()
        # self._config['class_abilities']['mighty_summoner'] = value
        # self.save()
        keys = ['class_abilities','mighty_summoner']
        self._set_config_value(keys,value)


    def get_flanking_bonus(self,default=False):
        keys = ['game_mechanics','flanking_bonus']

        value = self._get_config_value(keys,default)
        return(value)
    
    def set_flanking_bonus(self,value):
        # self.load()
        # self._config['class_abilities']['mighty_summoner'] = value
        # self.save()
        keys = keys = ['game_mechanics','flanking_bonus']
        self._set_config_value(keys,value)     

    def is_creature_available(self,cr,c_name,c_type):
        self.load()
        top_key = f'available_{c_type}'
        is_available = False # not available by default
        if top_key in self._config and cr in self._config[top_key] and c_name in self._config[top_key][cr]:
            is_available = self._config[top_key][cr][c_name]
        return is_available
    
    def get_available_creature_names_of_type_by_cr(self,c_type="beast"):
        availability = self.get_creature_availability_of_type_by_cr(c_type)
        available_creatures = {}
        for cr in availability:
            names = []
            for creature in availability[cr]:
                if availability[cr][creature]: names.append(creature)
            available_creatures[cr] = names
        return available_creatures


    def get_creature_availability_of_type_by_cr(self,c_type="beast"):
        # self._config.load()
        # must have crature info in json
        c_from_json = get_creature_names_of_type_by_cr_from_json(c_type)
        result = {}
        for cr in c_from_json:
            for c_name in c_from_json[cr]:
                top_key = f'available_{c_type}'
                is_available = False # not available by default
                if top_key in self._config and c_name in self._config[top_key]:
                    is_available = self._config[top_key][c_name] in ('True', 'true') 
                if cr not in result: result[cr] = {}
                result[cr][c_name]=is_available
        return(result)
    
    def set_creature_availability_of_type_by_cr(self,values,c_type="beast"):
        self.load()
        top_key = f'available_{c_type}'
        
        self._config[top_key]={}
        for cr in values:
            # tmp_config_placeholder = {}
            # self._config[top_key][cr]={}
            for c_name in values[cr]:
                 self._config[top_key][c_name] = str(values[cr][c_name])
            # self._config[top_key][cr]=tmp_config_placeholder
        self.save()
    



    # def get_available_creature_names_of_type_by_cr

