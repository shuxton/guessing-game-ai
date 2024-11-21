import streamlit as st
import pandas as pd


class StatisticsUi():
    def __init__(self) -> None:
        pass

    def render(self,title="Game Statistics",layout="wide"):
        st.set_page_config(layout=layout)
        st.title(title)
        col1, col2 = st.columns([2, 2])

        with col1: #left column
            self._display_table()

        with col2: #right column
            self._display_bar_chart()

    def _display_table(self):
       st.table(pd.DataFrame([] if "game_statistics" not in st.session_state else st.session_state.game_statistics)
                .rename(columns={'game_number': 'Game Number', 'hint_count': 'Hints','guess_count':"Guesses","word_length":"Word Length","time_taken":"Time taken","total_score":"Total Score","guessing_quality":"Guessing Quality"}))

    def _display_bar_chart(self):
        if "game_statistics" in st.session_state and st.session_state.game_statistics:
            df = pd.DataFrame(st.session_state.game_statistics)
            filtered_df = df[['game_number', 'guess_count']].rename(columns={
                'game_number': 'Game Number', 
                'guess_count': 'Number of Guesses'
            })
            st.bar_chart(filtered_df.set_index('Game Number'),x_label="Game number",y_label="Number of Guesses")
        else:
            st.write("No game statistics available to display.")
        

        