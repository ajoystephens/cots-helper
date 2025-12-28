import streamlit as st
import configparser

# from lib.creature import (
#     # Creature,
#     # get_all_creature_names,
#     get_creature_names_of_type_by_cr,
# )
from lib.config import Config

CONFIG_FILENAME = 'config.ini'


def save_config_on_click():
    st.session_state.config.set_flanking_bonus(st.session_state.flanking_bonus)
    st.session_state.config.set_mighty_summoner(st.session_state.mighty_summoner)
    # print(f'st.session_state.available_beasts: \n{st.session_state.available_beasts}')
    st.session_state.config.set_creature_availability_of_type_by_cr(st.session_state.available_beasts)



    # ['class_abilities'] = {
    #     'mighty_summoner': st.session_state.mighty_summoner
    # }

    # with open(CONFIG_FILENAME, 'w') as configfile:
    #      st.session_state.config.write(configfile)

def load_config():
    # print(f'in load_config')
    # st.session_state.config.read(CONFIG_FILENAME)
    st.session_state.flanking_bonus = st.session_state.config.get_flanking_bonus(default="advantage")
    st.session_state.mighty_summoner = st.session_state.config.get_mighty_summoner()

    # st.session_state.available_beasts = {}
    st.session_state.available_beasts = st.session_state.config.get_creature_availability_of_type_by_cr(c_type='beast')
    # print(f'st.session_state.available_beasts: \n{st.session_state.available_beasts}')
    # beasts_from_json = get_creature_names_of_type_by_cr(c_type="beast")
    # beasts_from_config = st.session_state.config['available_beasts']
    # for cr in beasts_from_json:
    #     st.session_state.available_beasts[cr]={}
    #     for beast in beasts_from_json[cr]:
    #         st.session_state.available_beasts[cr][beast]=False
    #         if cr in beasts_from_config and beast in beasts_from_config[cr]:
    #             st.session_state.available_beasts[cr][beast]=beasts_from_config[cr][beast]

st.set_page_config(layout="wide")

if "config" not in st.session_state:
    with st.spinner("Wait for settings to load..."):
        st.session_state.config = Config()
        load_config()



st.write('# Settings')

def available_beast_on_change(cr,c_name):
    key = f'ab_{cr}_{c_name}'
    value = st.session_state[key]

    st.session_state.available_beasts[cr][c_name]=value

col1, col2 = st.columns(2)
with col1:
    st.write('## Game Mechanics')
    flanking_bonus = st.radio(
        "Flanking Bonus",
        ["advantage", "+1 attack"],
        key='flanking_bonus'
    )

    st.write('## Class Features')
    mighty_summoner = st.toggle("Mighty Summoner (lvl 6 ability)", key='mighty_summoner')

    # st.write('## Crit Rules') TODO

with col2:
    st.write(f'## Available Creatures')

    st.write(f'### Beasts')
    # beasts_by_cr = get_creature_names_of_type_by_cr(c_type="beast")

    for cr in st.session_state.available_beasts:
        st.write(f'#### CR: {cr}')
        for c_name in st.session_state.available_beasts[cr]:
            key = f'ab_{cr}_{c_name}'
            st.checkbox(c_name, value=st.session_state.available_beasts[cr][c_name], key=key, on_change=available_beast_on_change, args=(cr,c_name))
    # st.write(st.session_state.available_beasts)




buttons_col1, buttons_col2 = st.columns(2)
with buttons_col1:
    st.button("💾 Save Config",type='primary',on_click=save_config_on_click,use_container_width=True)
with buttons_col2:
    if st.button("Back to the App",use_container_width=True):
        del st.session_state['config']
        st.switch_page("shepherd.py")