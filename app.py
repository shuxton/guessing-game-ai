import streamlit as st
from ui.game_ui import GameUi
from ui.information_ui import InformationUi
from ui.statistics_ui import StatisticsUi

def game_page():
    if "game_ui" not in st.session_state:
            st.session_state.game_ui = GameUi()
    st.session_state.game_ui.render()

def stats_page():
    if "stats_ui" not in st.session_state:
            st.session_state.stats_ui = StatisticsUi()
    st.session_state.stats_ui.render()

def info_page():
    if "info_ui" not in st.session_state:
            st.session_state.info_ui = InformationUi()
    st.session_state.info_ui.render()

pg = st.navigation([
    st.Page(game_page, title="Play", icon="🪩"),
    st.Page(stats_page, title="Stats", icon="📊"),
    st.Page(info_page, title="Info", icon="ℹ️")
])

pg.run()
