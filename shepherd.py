import configparser
import streamlit as st
import streamlit_scrollable_textbox as stx

# ROOT_DIR = 
from lib.creature import (
    Creature,
    get_all_creature_names,
    get_creature_names_of_type_by_cr_from_json,
)

from lib.utils import (
    save_state,
    load_state,
    get_saved_sessions
)

from lib.config import Config

CONFIG_FILENAME = 'config.ini'

################################################################################################
# PAGE SETUP
################################################################################################
def load_config():
    # st.session_state.config.read(CONFIG_FILENAME)

    st.session_state.mighty_summoner = st.session_state.config.get_mighty_summoner()
    st.session_state.flanking_bonus = st.session_state.config.get_flanking_bonus()


st.set_page_config(layout="wide")

if "summoned_creatures" not in st.session_state:
    st.session_state.summoned_creatures = []

if "session_log" not in st.session_state:
    st.session_state.session_log = [""]

# if "config" not in st.session_state:
#     st.session_state.config = configparser.ConfigParser()
if "config" not in st.session_state:
    st.session_state.config = Config()
    # load_config()

load_config()

creature_names = get_all_creature_names()


################################################################################################
# DIALOG METHODS
################################################################################################
@st.dialog("Summon Something")
def summon_dialog():
    creature = st.selectbox(
        "What would you like to summon?",
        creature_names,
    )
    number = st.number_input("How many?",value=1)
    mighty_summoner = st.checkbox("Apply Mighty Summoner (lvl 6)?", value=st.session_state.mighty_summoner)

    if st.button("Submit"):
        st.session_state.summoned_creatures = []
        st.session_state.session_log = []

        for i in range(number):
            print(f'st.session_state.flanking_bonus: {st.session_state.flanking_bonus}')
            st.session_state.summoned_creatures.append(Creature(creature,mighty_summoner,flanking_bonus=st.session_state.flanking_bonus))

        st.session_state.session_log.append(f"🔮 Summoned {number} {creature}, Mighty Summoner = {mighty_summoner}\n")
        st.rerun()

def ca_radio_format_func(raw_cr):
    num = get_creature_num_from_cr(raw_cr)

    if num==1: description = f"{num} beast of challenge rating {raw_cr}"
    else: description = f"{num} beasts of challenge rating {raw_cr}"
    return description

def get_creature_num_from_cr(raw_cr):
    num = 0
    match raw_cr:
        case "2":
            num = 1
        case "1":
            num = 2
        case "1/2":
            num = 4
        case "1/4":
            num = 8
    return num

@st.dialog("Conjure Animals")
def conjure_animals_dialog():
    st.caption("3rd-level Conjuration")

    info = """
        **Casting Time:** 1 action<br>
        **Range:** 60 feet<br>
        **Components:** V, S<br>
        **Duration:** Concentration, up to 1 hour
        """
    st.markdown(info,unsafe_allow_html=True)
    st.caption("go [here](%s) for the full spell description" % "https://roll20.net/compendium/dnd5e/Conjure%20Animals#content")

    creature_options = get_creature_names_of_type_by_cr_from_json("beast")
    creature_options = st.session_state.config.get_available_creature_names_of_type_by_cr("beast")
 
    summonable_crs = ["2","1","1/2","1/4"]
    summon_cr = st.radio(
        "CR to summon",
        summonable_crs,
        format_func=ca_radio_format_func,
        label_visibility='collapsed'
    )
    if summon_cr:
        creature = st.selectbox(
            "Select a Creature",
            creature_options[summon_cr],
        )
        number = get_creature_num_from_cr(summon_cr)

    mighty_summoner = st.checkbox("Apply Mighty Summoner (lvl 6)?", value=st.session_state.mighty_summoner)

    if st.button("Summon"):
        st.session_state.summoned_creatures = []
        st.session_state.session_log = []

        for i in range(number):
            st.session_state.summoned_creatures.append(Creature(creature,mighty_summoner,flanking_bonus=st.session_state.flanking_bonus))

        st.session_state.session_log.append(f"🔮 Summoned {number} {creature}, Mighty Summoner = {mighty_summoner}\n")
        st.rerun()


@st.dialog("Save current session")
def save_dialog():
    save_name = st.text_input("save name")

    if st.button("Submit"):
        save_state(save_name,
                   st.session_state.summoned_creatures,
                   st.session_state.session_log)

        st.session_state.session_log.append(f"💾 Saved session: {save_name}\n")
        st.rerun()


@st.dialog("Load a saved session")
def load_dialog():
    saved_sessions = get_saved_sessions()
    session_name = st.selectbox(
        "Select a session to load.",
        saved_sessions,
    )

    if st.button("Submit"):
        st.session_state.summoned_creatures, st.session_state.session_log = load_state(session_name)

        st.session_state.session_log.append(f"💾 Loaded session: {session_name}\n")
        st.rerun()


st.title('Circle of Shepherd, Summon Manager')

but_col1, but_col2, but_col3, but_col4, but_col5 = st.columns([1,1,1,1,1])
with but_col1:
    st.button("Summon Anything",on_click=summon_dialog,use_container_width=True)
with but_col2:
    st.button("Conjure Animals :small[(3rd)]",type='primary',on_click=conjure_animals_dialog,use_container_width=True)
with but_col3:
    st.button("Save",on_click=save_dialog,use_container_width=True)
with but_col4:
    st.button("Load",on_click=load_dialog,use_container_width=True)
with but_col5:
    if st.button("⚙ Settings",use_container_width=True):
        del st.session_state['config']
        st.switch_page("pages/settings.py")

if len(st.session_state.summoned_creatures)>0:
    a_creature = st.session_state.summoned_creatures[0]

    str_mod = a_creature.abilities["str"][1]
    dex_mod = a_creature.abilities["dex"][1]
    con_mod = a_creature.abilities["con"][1]
    int_mod = a_creature.abilities["int"][1]
    wis_mod = a_creature.abilities["wis"][1]
    cha_mod = a_creature.abilities["cha"][1]
    
    # cr_header_col1, cr_header_col2 = st.columns([5,1])
    st.write(f"## {a_creature.name}")
    # cr_header_col2.link_button(
    #     "", 
    #     a_creature.source_link,
    #     icon=":material/link:"
    # )

    cd_col1, cd_col2, cd_col3, cd_col4 = st.columns([1,1,1,3])

    with cd_col1:
        st.write(f":grey[AC:] &nbsp;&nbsp; {a_creature.ac}")
        st.write(f":grey[Max HP:] &nbsp;&nbsp; {a_creature.max_hp}")
        st.write(f":grey[Speed:] &nbsp;&nbsp; {a_creature.speed} ft")
        st.write(f":grey[Darkvision:] &nbsp;&nbsp; {a_creature.darkvision} ft")
        st.write(f":grey[Size:] &nbsp;&nbsp; {a_creature.size}")

    with cd_col2:
        txt = f'''
            :grey[STR:] &nbsp;&nbsp; {str_mod}  \n
            :grey[DEX:] &nbsp;&nbsp; {dex_mod}  \n
            :grey[CON:] &nbsp;&nbsp; {con_mod}  
        '''
        st.write(txt)

    with cd_col3:
        txt = f'''
            :grey[INT:] &nbsp;&nbsp; {int_mod}  \n
            :grey[WIS:] &nbsp;&nbsp; {wis_mod}  \n
            :grey[CHA:] &nbsp;&nbsp; {cha_mod}  
        '''
        st.write(txt)

        st.link_button(
            "Source", 
            a_creature.source_link,
            icon=":material/link:",
            use_container_width=True
        )

    with cd_col4:
        txt = f':green[Skills]: &nbsp; '
        for s in a_creature.skills: txt += f'{s}: {a_creature.skills[s]} &nbsp; &nbsp;'
        st.write(txt)

        for t in a_creature.traits:
            st.write(f':blue[{t}]: &nbsp; {a_creature.traits[t]}')
            

        for a in a_creature.actions:
            attack = a_creature.actions[a]['attack']
            reach = a_creature.actions[a]['reach']
            dmg_dice = a_creature.actions[a]['dmg_dice']
            dmg_mod = a_creature.actions[a]['dmg_mod']
            dmg_type = a_creature.actions[a]['dmg_type']
            note = a_creature.actions[a]['note']

            dmg_str = ''
            for dd in dmg_dice: dmg_str += f'{dmg_dice[dd]}{dd}'
            dmg_str += f'+{dmg_mod}'

            txt = f':red[{a}]: &nbsp;'
            txt += f':grey[atk]: +{attack} &nbsp;'
            txt += f':grey[dmg]: {dmg_str} &nbsp; {dmg_type}'

            if note:
                txt += f'  \n &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {note}'
            st.write(txt)


st.divider()


def damage_creature_on_click(idx):
    creature = st.session_state.summoned_creatures[idx]
    c_number = idx+1
    k = f'hp_num_{idx}'
    dmg_amount = st.session_state[k]

    creature.dmg(dmg_amount)

    if creature.is_dead():
        st.session_state.session_log.append(f"☠️ Creature {c_number} died after {dmg_amount} damage.\n")
    else:
        st.session_state.session_log.append(f"🔥 Creature {c_number} recieved {dmg_amount} damage. New HP: {creature.current_hp}\n")

    st.session_state[k] = 0
    # k2 = f'hp_dmg_{idx}'
    # st.session_state[k2] = False

def heal_creature_on_click(idx):
    creature = st.session_state.summoned_creatures[idx]
    c_number = idx+1
    k = f'hp_num_{idx}'
    heal_amount = st.session_state[k]

    creature.heal(heal_amount)

    st.session_state.session_log.append(f"❤️‍🩹 Creature {c_number} healed {heal_amount} HP. New HP: {creature.current_hp}\n")

    st.session_state[k] = 0

def temp_creature_on_click(idx):
    creature = st.session_state.summoned_creatures[idx]
    c_number = idx+1
    k = f'hp_num_{idx}'
    amount = st.session_state[k]

    creature.give_temp_hp(amount)

    st.session_state.session_log.append(f"🩹 Creature {c_number} given {amount} temp HP.\n")

    st.session_state[k] = 0

def atk_roll_on_click(idx):
    creature = st.session_state.summoned_creatures[idx]
    c_number = idx+1

    k = f'atk_select_{idx}'
    atk_type = st.session_state[k]

    k = f'atk_advantage_{idx}'
    has_advantage = st.session_state[k]

    k = f'atk_disadvantage_{idx}'
    has_disadvantage = st.session_state[k]

    k = f'atk_flanking_{idx}'
    is_flanking = st.session_state[k]

    atk_desc = creature.attack(atk_type,
                               advantage=has_advantage,
                               disadvantage=has_disadvantage,
                               flanking=is_flanking)

    # creature.give_temp_hp(amount)

    description = f'⚔️ Creature {c_number} rolled {atk_type} attack → {atk_desc}\n'

    st.session_state.session_log.append(description)


col_names = ["","№",'HP','Temp HP','Update HP Value',":small[dmg]",":small[heal]",":small[tmp]","Attack",":red[:material/casino:]",":green[:material/casino:]",":grey[:material/group:]",""]
creature_header_cols = st.columns([1,1,1,1,2,1,1,1,2,1,1,1,1])
for col, name in zip(creature_header_cols,col_names): col.write(f':grey[{name}]')

for idx, c in enumerate(st.session_state.summoned_creatures):
    select_col, cc_col1, cc_col2, cc_col3, cc_col4, cc_col5, cc_col6, cc_col7, cc_col8, cc_col9, cc_col10, cc_col11, cc_col12 = st.columns([1,1,1,1,2,1,1,1,2,1,1,1,1])

    creature = st.session_state.summoned_creatures[idx]
    c_number = idx+1

    select_phold = select_col.empty()
    select = select_phold.checkbox(
        "select",
        label_visibility="collapsed",
        value=True,
        key=f'select_creature_{idx}')

    cc_col1.write(c_number)

    if creature.is_dead():
        cc_col2.write('☠️')
    elif creature.is_bloodied():
        cc_col2.write(f':red[{creature.current_hp}]')
    else: cc_col2.write(creature.current_hp)

    cc_col3.write(creature.temp_hp)

    update_hp_input_phold = cc_col4.empty()
    hp_number_input = update_hp_input_phold.number_input("HP",step=1,label_visibility="collapsed",key=f'hp_num_{idx}')


    hp_dmg_button_phold = cc_col5.empty()
    hp_dmg_button = hp_dmg_button_phold.button(
        ":material/bomb:",
        key=f'hp_dmg_{idx}',
        on_click=damage_creature_on_click,
        args=(idx,))
    
    hp_heal_button_phold = cc_col6.empty()
    hp_heal_button = hp_heal_button_phold.button(
        ":material/health_and_safety:",
        key=f'hp_heal_{idx}',
        on_click=heal_creature_on_click,
        args=(idx,))
    
    hp_temp_button_phold = cc_col7.empty()
    hp_temp_button = hp_temp_button_phold.button(
        ":material/healing:",
        key=f'hp_temp_{idx}',
        on_click=temp_creature_on_click,
        args=(idx,))
    
    atk_select_phold = cc_col8.empty()
    atk_select = atk_select_phold.selectbox(
        "attack",
        # ["a","b"],
        creature.get_attack_names(),
        label_visibility="collapsed",
        key=f'atk_select_{idx}')

    atk_disadvantage_phold = cc_col9.empty()
    atk_disadvantage = atk_disadvantage_phold.checkbox(
        "disadvantage",
        label_visibility="collapsed",
        key=f'atk_disadvantage_{idx}')

    atk_advantage_phold = cc_col10.empty()
    atk_advantage = atk_advantage_phold.checkbox(
        "advantage",
        label_visibility="collapsed",
        key=f'atk_advantage_{idx}')
    
    atk_flanking_phold = cc_col11.empty()
    atk_flanking = atk_flanking_phold.checkbox(
        "flanking",
        label_visibility="collapsed",
        key=f'atk_flanking_{idx}')
    
    atk_button_phold = cc_col12.empty()
    atk_button = atk_button_phold.button(
        "⚔️",
        key=f'atk_{idx}',
        on_click=atk_roll_on_click,
        args=(idx,))

def bulk_damage_on_click():
    dmg_amount = st.session_state.bulk_hp_num
    dmg_txt = f'🔥🔥🔥 Applied {dmg_amount} points of dmg to the following: \n'
    for i in range(len(st.session_state.summoned_creatures)):
        creature = st.session_state.summoned_creatures[i]
        if st.session_state[f'select_creature_{i}'] and not creature.is_dead():

            c_number = i+1

            creature.dmg(dmg_amount)

            if creature.is_dead():
                dmg_txt += f" → ☠️ Creature {c_number} (died)\n"
            else:
                dmg_txt += f" → 🔥 Creature {c_number} ({creature.current_hp} remaining)\n"

    st.session_state.session_log.append(dmg_txt)
    st.session_state.bulk_hp_num = 0

def bulk_attack_on_click():

    note_txt = f'⚔️⚔️⚔️ Rolled the following attacks: \n'
    for i in range(len(st.session_state.summoned_creatures)):
        creature = st.session_state.summoned_creatures[i]
        if st.session_state[f'select_creature_{i}'] and not creature.is_dead():
            k = f'atk_select_{i}'
            atk_type = st.session_state[k]

            k = f'atk_advantage_{i}'
            has_advantage = st.session_state[k]

            k = f'atk_disadvantage_{i}'
            has_disadvantage = st.session_state[k]

            k = f'atk_flanking_{i}'
            is_flanking = st.session_state[k]

            c_number = i+1

            atk_desc = creature.attack(atk_type,
                                    advantage=has_advantage,
                                    disadvantage=has_disadvantage,
                                    flanking=is_flanking)

            note_txt += f' → ⚔️ Creature {c_number} rolled {atk_type} attack → {atk_desc}\n'

    st.session_state.session_log.append(note_txt)

def bulk_heal_on_click():
    heal_amount = st.session_state.bulk_hp_num
    note_txt = f'❤️‍🩹❤️‍🩹❤️‍🩹 Applied {heal_amount} points of dmg to the following: \n'
    for i in range(len(st.session_state.summoned_creatures)):
        creature = st.session_state.summoned_creatures[i]
        if st.session_state[f'select_creature_{i}'] and not creature.is_dead():

            c_number = i+1

            creature.heal(heal_amount)

            note_txt += f" → ❤️‍🩹 Creature {c_number} ({creature.current_hp} HP)\n"
    st.session_state.session_log.append(note_txt)
    st.session_state.bulk_hp_num = 0

def bulk_temp_on_click():
    amount = st.session_state.bulk_hp_num
    note_txt = f'🩹🩹🩹 Applied {amount} points of temp HP to the following: \n'
    for i in range(len(st.session_state.summoned_creatures)):
        creature = st.session_state.summoned_creatures[i]
        if st.session_state[f'select_creature_{i}'] and not creature.is_dead():

            c_number = i+1

            creature.give_temp_hp(amount)

            note_txt += f" → 🩹 Creature {c_number} ({creature.temp_hp} Temp HP)\n"

    st.session_state.session_log.append(note_txt)
    st.session_state.bulk_hp_num = 0

if len(st.session_state.summoned_creatures)>0:
    st.write('### Bulk Actions:primary[*]')

    bulk_hp_col1, bulk_hp_col2, bulk_hp_col3, bulk_hp_col4 = st.columns([2,1,1,1])
    with bulk_hp_col1:
        bulk_hp_number_input = st.number_input("HP",step=1,label_visibility="collapsed",key=f'bulk_hp_num')

    with bulk_hp_col2:
        bulk_hp_dmg_button = st.button(
            'damage',
            icon=":material/bomb:",
            use_container_width=True,
            on_click=bulk_damage_on_click)
        
    with bulk_hp_col3:
        bulk_heal_button = st.button(
            'heal',
            icon=":material/health_and_safety:",
            use_container_width=True,
            on_click=bulk_heal_on_click)
        
    with bulk_hp_col4:
        bulk_heal_button = st.button(
            'temp',
            icon=":material/healing:",
            use_container_width=True,
            on_click=bulk_temp_on_click)
        
    bulk_atk_button = st.button(
        'attack',
        icon=":material/casino:",
        use_container_width=True,
        on_click=bulk_attack_on_click)
            
    st.write(f':primary[*]Actions are applied to selected creatures')


st.divider()

st.write('## Notes')
stx.scrollableTextbox(st.session_state.session_log[::-1],height = 300)

def add_note_on_click():
    new_note = st.session_state.add_note_txt+'\n'
    st.session_state.session_log.append(new_note)
    st.session_state.add_note_txt = ""
an_col1, an_col2 = st.columns([5,1])
with an_col1:
    add_note_txt = st.text_input("Add Note",label_visibility="collapsed", key="add_note_txt")
with an_col2:
    add_note_btn = st.button("Add Note",on_click=add_note_on_click,use_container_width=True)

