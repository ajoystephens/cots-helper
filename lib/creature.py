import json
import random
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.resolve()
CREATURE_PATH = ROOT_DIR / "data/creatures.json"
# CONFIG_FILENAME = 'config.ini'

def get_all_creature_names():
        with open(CREATURE_PATH, 'r') as file:
            data = json.load(file)
        
        creature_names = []
        if data:
            for c in data:
                creature_names.append(c["name"])
        
        return(creature_names)


def get_creature_names_of_type_by_cr_from_json(c_type="beast"):
        # print('in get_creature_names_of_type_by_cr_from_json')
        with open(CREATURE_PATH, 'r') as file:
            data = json.load(file)
        
        creature_names = {}
        if data:
            # print(f' - is data')
            for c in data:
                cr = c["cr"]
                name = c["name"]
                this_type = c["type"]
                # print(f' - cr: {cr}, name: {name}, type: {this_type}.... c_type: {c_type}, {this_type==c_type}')

                if this_type==c_type:
                    if cr in creature_names:
                        creature_names[cr].append(name)
                    else:
                        creature_names[cr] = [name]
        
        return(creature_names)

# def get_creature_is_available(c_name,xc_type,c_cr):


class Creature:
    def __init__(self, name, mighty_summoner=False):
        self.name = name

        self._load(mighty_summoner)

    def _load(self,mighty_summoner):

        with open(CREATURE_PATH, 'r') as file:
            data = json.load(file)
        
        raw_creature = {}
        if data:
            for c in data:
                if c["name"] == self.name:
                    raw_creature = c
                    break
        
        self.cr = raw_creature["cr"]

        self.ac = raw_creature["ac"]
        self.speed = raw_creature["speed"]
        self.size = raw_creature["size"]
        self.darkvision = raw_creature["darkvision"]

        self.hit_dice = raw_creature["hit_dice"]

        self.max_hp = raw_creature["hp"]
        self.current_hp = raw_creature["hp"]
        self.temp_hp = 0

        self.abilities = raw_creature["abilities"]
        self.skills = raw_creature["skills"]
        self.traits = raw_creature["traits"]
    
        self.actions = raw_creature['actions']

        self.source_link = raw_creature['source']

        if mighty_summoner: self._apply_mighty_summoner()
    # def set_current_hp(self,value):
    #     self.current_hp = value

    # def set_temp_hp(self,value):
    #     self.temp_hp = value

    def _apply_mighty_summoner(self):
        # get total number of hit dice
        num_hit_dice = 0
        for d in self.hit_dice: num_hit_dice+= self.hit_dice[d]

        # give extra hp
        self.max_hp += 2*num_hit_dice
        self.current_hp += 2*num_hit_dice

        # add reminder of dmg
        self.traits["Mighty Summoner"] = "The damage from its natural weapons is considered **magical** for the purpose of overcoming immunity and resistance to nonmagical attacks and damage."
    def dmg(self,value):
        if value<0: # if value is negative 
            dmg_to_do = -1 * value
        else: dmg_to_do = value

        temp_decrement = min(dmg_to_do,self.temp_hp)
        self.temp_hp -= temp_decrement
        dmg_to_do -= temp_decrement

        self.current_hp -= dmg_to_do

    def heal(self,value):
        if value<0: return # value must be positive

        if (self.current_hp + value) > self.max_hp:
            self.current_hp = self.max_hp
        else: self.current_hp += value

    def give_temp_hp(self,value):
        self.temp_hp = value

    def is_bloodied(self):
        return self.current_hp < (self.max_hp/2)
    def is_dead(self):
        return self.current_hp<=0
    
    def get_attack_names(self):
        return self.actions.keys()
    # def attack

    def attack(self,attack_name,advantage=False,disadvantage=False):
        atk_details = self.actions[attack_name]

        atk_roll, dmg_amount, description = self._single_attack(attack_name,advantage,disadvantage)

        if atk_details["multiattack"]:
            atk_roll_2, dmg_amount_2, description_2 = self._single_attack(attack_name,advantage,disadvantage)

            description = f'Multiattack, Total Dmg (if hit): {dmg_amount+dmg_amount_2}\n →→ ⚔️ {description}\n  →→ ⚔️ {description_2}'
        
        return description

    def _single_attack(self,attack_name,advantage,disadvantage):
        atk_details = self.actions[attack_name]

        atk_roll, atk_roll_str, is_crit = self._get_attack_roll(attack_name,advantage,disadvantage)
        dmg_amount, dmg_str = self._get_attack_dmg(attack_name,is_crit)

        description = f'attack: {atk_roll_str}; dmg: {dmg_str}'

        return atk_roll, dmg_amount, description

    def _get_attack_dmg(self,attack_name,is_crit):
        atk_details = self.actions[attack_name]

        for d in atk_details['dmg_dice']:
            dice_num = int(d[1:])
            dmg = 0
            dmg_str = ''
            roll_cnt = atk_details['dmg_dice'][d]
            if is_crit: roll_cnt = roll_cnt*2
            for i in range(roll_cnt):
                roll = self.roll_d(dice_num)
                dmg += roll
                dmg_str += f'+{roll}'
            
            dmg_str = dmg_str[1:] # remove first +

        dmg_mod = atk_details['dmg_mod']
        dmg += dmg_mod
        dmg_str = f'{dmg} ({dmg_str}+{dmg_mod})'

        return dmg, dmg_str

    def _get_attack_roll(self,attack_name,advantage,disadvantage):
        atk_details = self.actions[attack_name]

        atk_roll = self.roll_d(20)
        atk_roll_str = f'{atk_roll}'

        if advantage:
            atk_roll_1 = self.roll_d(20)
            atk_roll_2 = self.roll_d(20)
            
            atk_roll = max(atk_roll_1,atk_roll_2)
            atk_roll_str = f'(🟢 {atk_roll_1}, {atk_roll_2})'

        if disadvantage:
            atk_roll_1 = self.roll_d(20)
            atk_roll_2 = self.roll_d(20)
            
            atk_roll = min(atk_roll_1,atk_roll_2)
            atk_roll_str = f'(🔴 {atk_roll_1}, {atk_roll_2})'

        atk_mod = atk_details["attack"]
        is_crit = atk_roll==20
        atk_roll += atk_mod
        atk_roll_str = f'{atk_roll} ({atk_roll_str}+{atk_mod})'

        if is_crit: atk_roll_str = f'🍀 {atk_roll_str}'

        return atk_roll, atk_roll_str,is_crit
    
    def roll_d(self,d):
        # here d should be the dice
        # ie. d=8 will roll a d8, randomly generating a number between 1 and 8 (inclusive)
        num = random.randint(1, d)
        return(num)


    # def increment_hp(self,value):
    #     if value < 0: self._dmg(value)

