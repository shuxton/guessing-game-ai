import streamlit as st


class InformationUi():
    def __init__(self) -> None:
        pass

    def render(self,title="ReadME",layout="wide"):
        st.set_page_config(layout=layout)
        st.title(title)
        col1, col2 = st.columns([2, 2])

        with col1: #left column
            self._display_formulas()

        with col2: #right column
            self._display_about()
            self._display_instructions()

    def _display_formulas(self):
       st.write("""
### Estimate Guessing Quality

The **guessing quality** is calculated using the following factors:

- **Guess Factor**: Penalizes based on the number of guesses.

    $$
    \\text{guess\\_factor} = \\max\\left(0, \\left(1 - \\frac{\\text{guess\\_count}}{10}\\right)\\right)
    $$

- **Hint Factor**: Penalizes based on the number of hints.

    $$
    \\text{hint\\_factor} = \\max\\left(0, \\left(1 - \\frac{\\text{hint\\_count}}{5}\\right)\\right)
    $$

- **Time Factor**: Penalizes based on the time taken.

    $$
    \\text{time\\_factor} = \\max\\left(0, \\left(1 - \\frac{\\text{time\\_taken}}{300}\\right)\\right)
    $$

The **guessing quality score** is calculated as:

$$
\\text{quality\\_score} = \\left(\\text{guess\\_factor} + \\text{hint\\_factor} + \\text{time\\_factor}\\right) \\times \\frac{\\text{max\\_quality}}{3}
$$

The final quality score is clamped between a **minimum** and **maximum** value:

$$
\\text{guessing\\_quality} = \\text{round}\\left(\\max\\left(\\text{min\\_quality}, \\min\\left(\\text{max\\_quality}, \\text{quality\\_score}\\right)\\right)\\right)
$$

---

### Calculate Score

The **total score** is calculated using the following formula:

1. **Time Taken** and **Word Length** are considered:

    $$
    \\text{time\\_taken} = \\text{end\\_time} - \\text{start\\_time}
    $$

    $$
    \\text{word\\_length} = \\text{len(word)}
    $$

2. **Penalty Factors** for **Hints**, **Guesses**, and **Time** are adjusted based on word length:

    $$
    \\text{hint\\_penalty} = \\frac{\\text{hint\\_penalty\\_base}}{1 + (\\text{word\\_length} \\times \\text{length\\_scaling\\_factor})}
    $$

    $$
    \\text{guess\\_penalty} = \\frac{\\text{guess\\_penalty\\_base}}{1 + (\\text{word\\_length} \\times \\text{length\\_scaling\\_factor})}
    $$

    $$
    \\text{time\\_penalty} = \\frac{\\text{time\\_penalty\\_base}}{1 + (\\text{word\\_length} \\times \\text{length\\_scaling\\_factor})}
    $$

3. **Calculate Total Score**:

    If the game was completed with exactly 1 guess and 1 hint:

    $$
    \\text{total\\_score} = \\text{max\\_score}
    $$

    Otherwise, the score is calculated as:

    $$
    \\text{total\\_score} = \\text{round}\\left( \\max\\left( \\text{min\\_score}, \\text{max\\_score} - (\\text{hint\\_count} \\times \\text{hint\\_penalty}) - (\\text{guess\\_count} \\times \\text{guess\\_penalty}) - \\left(\\text{floor}\\left(\\frac{\\text{time\\_taken}}{45}\\right) \\times \\text{time\\_penalty}\\right) \\right) \\right)
    $$
""")

        
    def _display_about(self):
        st.write("""
        ### About This Project

        This project is developed as part of the **AI and the Web** course.

        **Contributors**:
        - **Shubham Nilesh Jariwala**  
        - **Krzysztof Wesolek**  
        - **Aleksandra Sokolowska**  
        """)

    def _display_instructions(self):
        st.write("""
        ### Instructions

        Welcome to the **Guess the Word Game**! Follow these steps to play:

        1. **Choose a Category**: Select a category to begin the game.
        2. **Get Hints**: The game will provide:
            - A hint related to the word.
            - The number of characters in the word to be guessed.
        3. **Make Your Guess**: Type the entire word in the chat box to win.
        4. **Generate More Hints** (Optional):  
            - To request additional hints, simply type **"Ola"** followed by your question (e.g., *Ola Is the word a fruit?*).
            - **Note**: Each extra hint will reduce your score, so use them wisely!
        5. **Scoring Rules**:  
            - Incorrect guesses, taking more time, and requesting more hints will lower your points.
            - Aim to guess the word quickly and accurately to maximize your score.

        **Note**:  
        - This app does not use a database and does not store any data.  
        - All progress will be lost on page refresh.

        Enjoy the challenge and test your guessing skills!
        """)



            