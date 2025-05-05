import streamlit as st
import configparser

CONFIG_FILENAME = 'config.ini'


def save_config_on_click():
    st.session_state.config['class_abilities'] = {
        'mighty_summoner': st.session_state.mighty_summoner
    }

    with open(CONFIG_FILENAME, 'w') as configfile:
         st.session_state.config.write(configfile)

def load_config():
    st.session_state.config.read(CONFIG_FILENAME)

    st.session_state.mighty_summoner = eval(st.session_state.config['class_abilities']['mighty_summoner'])

st.set_page_config(layout="wide")

if "config" not in st.session_state:
    st.session_state.config = configparser.ConfigParser()
    load_config()


st.write('# Settings')

st.write('## Class Features')
mighty_summoner = st.toggle("Mighty Summoner (lvl 6 ability)", key='mighty_summoner')

buttons_col1, buttons_col2 = st.columns(2)
with buttons_col1:
    st.button("💾 Save Config",type='primary',on_click=save_config_on_click,use_container_width=True)
with buttons_col2:
    if st.button("Back to the App",use_container_width=True):
        st.switch_page("shepherd.py")