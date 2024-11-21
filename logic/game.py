import math
from random import randint
import pandas as pd
import openai
from enum import Enum
import os
from dotenv import load_dotenv 
import time
from dataclasses import dataclass


class GameState(Enum):
    START = 1
    PLAYING = 2
    END = 3


@dataclass
class GameStatistics:
    game_number: int = 0
    hint_count: int = 0
    guess_count: int = 0
    word_length: int = 0
    time_taken: float = 0.0
    total_score: int = 0
    guessing_quality:float = 1


class Game():
    def __init__(self):
        self.category=None
        self.state = GameState.START
        self.word = None
        self.prompt=""
        self.guessed_word = None
        self.start_time = 0
        self.end_time = 0
        self.game_stats : GameStatistics = GameStatistics(1,0,0,0,0,0,1) 
        self.df = pd.read_csv("guessing_game_dataset.csv")
        self._initialize_openai()

    def _initialize_openai(self):
        load_dotenv() 
        key = os.getenv("OPEN_AI_KEY")
        if not key:
            raise ValueError("OpenAI API key not found. Please set it in the environment variables.")
        openai.api_key = key 
        self.client = openai  

    def generate_hint(self):
        self.game_stats.hint_count+=1
        chat_completion = self.client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": '''You will be provided with a word, followed by a prompt associated with it. word:prompt format.
                Your task is to provide appropriate hint (only one) if there is no prompt so that the user can guess the word.
                If there is a prompt, try to answer the prompt. Your answers should serve as a hint and never reveal the word'''},
            {
                "role": "user", 
                "content": self.word+":"+self.prompt},
        ],
        )
        return chat_completion.choices[0].message.content

    def fetch_categories(self):
        return self.df["category"].unique()
    
    def set_category(self,category):
        if self.state is GameState.START:
            self.category = category
            self.state = GameState.PLAYING
            self.start_time = time.time()
            return True
        return False

    def _update_guessed_word(self,word):
        previous_word = self.guessed_word
        is_updated=False
        index=0
        for i,j,k in zip(self.word,self.guessed_word,word):
            if str(j).isnumeric() and str.upper(i) == str.upper(k):
                previous_word[index]=str.upper(i)
                is_updated = True
            index+=1
        self.guessed_word=previous_word
        return is_updated

    def generate_question(self):
        df_filtered = self.df[self.df['category'].str.contains(self.category, case=False)]
        row = df_filtered.iloc[randint(0,df_filtered.shape[0]-1)]
        self.word = str.upper(row["word"])
        self.guessed_word = [x for x in range(0,len(self.word))]

    def _check_if_hint_requested(self,input_string):
        first_word = input_string.split()[0] if input_string else ""
        return first_word.upper() == "OLA"
    
    _extract_hint_request = lambda self,s: ' '.join(s.split()[1:]) if len(s.split()) > 1 else ""

    def prompt_handler(self, prompt):
        try:
            if self.state is GameState.START:
                return "Please select a category to start playing the game.", False
            
            if self.state is GameState.PLAYING:
                if self._check_if_hint_requested(prompt):
                    # Process hint request
                    self.prompt = self._extract_hint_request(prompt)
                    return "Your hint is being updated...", True

                self.game_stats.guess_count += 1
                if self._update_guessed_word(prompt):
                    if ''.join(str(x) for x in self.guessed_word) == self.word:
                        # Correct guess, end the game
                        self.state = GameState.END
                        self.end_time = time.time()
                        self._calculate_score()
                        return (f"You guessed the word!\n"
                                f"You scored: {self.game_stats.total_score} points!\n"
                                f"Time taken: {self.game_stats.time_taken}s"), False
                    else:
                        return "You are one step closer to guessing the right word!", False
                else:
                    return "Oops! That was an incorrect guess. Try again.", False
            
            return "The game has ended. Reset to play again.", False
        
        except Exception as e:
            print(e)
            return "Something went wrong", False


    def _calculate_score(self):
        self.game_stats.time_taken = math.ceil(self.end_time - self.start_time)
        self.game_stats.word_length = len(self.word)
        time_penalty = min(20,int(self.game_stats.time_taken / 30))
        self.game_stats.total_score = max(20,math.ceil(100 - self.game_stats.word_length
                                              /(self.game_stats.guess_count+self.game_stats.word_length+self.game_stats.hint_count * 1.5 - 2.5)) 
                                              - time_penalty)
    def _estimate_guessing_quality(self):
        max_quality = 10  
        min_quality = 1  
        
        guess_factor = max(0, (1 - (self.game_stats.guess_count / 10)))  # max 10 guesses assumed
        hint_factor = max(0, (1 - (self.game_stats.hint_count / 5)))  # max 5 hints assumed
        time_factor = max(0, (1 - (self.game_stats.time_taken / 300)))  # max 300 seconds assumed
        quality_score = (guess_factor + hint_factor + time_factor) * max_quality / 3
        self.game_stats.guessing_quality = round(max(min_quality, min(max_quality, quality_score)))

    def _calculate_score(self):
        max_score = 100
        min_score = 10  
        hint_penalty_base = 15  # Base penalty per hint
        guess_penalty_base = 10  # Base penalty per guess
        length_scaling_factor = 0.5  # Reduces penalty for longer words
        time_penalty_base = 20
        self.game_stats.time_taken = self.end_time-self.start_time
        self.game_stats.word_length = len(self.word)

        # Adjust penalties based on word length
        hint_penalty = hint_penalty_base / (1 + (self.game_stats.word_length * length_scaling_factor))
        guess_penalty = guess_penalty_base / (1 + (self.game_stats.word_length * length_scaling_factor))
        time_penalty = time_penalty_base / (1 + (self.game_stats.word_length * length_scaling_factor))
        # Calculate score
        if self.game_stats.guess_count == 1 and self.game_stats.hint_count == 1:
            self.game_stats.total_score = max_score
        else:
            self.game_stats.total_score = round(max(
                min_score,
                max_score 
                - (self.game_stats.hint_count * hint_penalty) 
                - (self.game_stats.guess_count * guess_penalty) 
                - (math.floor(self.game_stats.time_taken/45)*time_penalty)
            ))

        self._estimate_guessing_quality()

    def reset(self):
        self.category=None
        self.state = GameState.START
        self.word = None
        self.guessed_word = None
        self.game_stats=GameStatistics(self.game_stats.game_number+1,0,0,0,0,0,1)
