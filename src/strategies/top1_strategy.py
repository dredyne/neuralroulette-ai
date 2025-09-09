"""Top-1 Strategy Implementation
Highest risk/reward strategy that predicts a single number
"""

import asyncio
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.utils import to_categorical
import os
from datetime import datetime

class Top1Strategy:
    """Strategy that predicts a single most likely number"""
    
    def __init__(self, balance=10.0, auto_train=False):
        self.name = "Top-1 Single Number"
        self.description = "Highest risk/reward - predicts single most likely number"
        self.balance = balance
        self.auto_train = auto_train
        self.game_history = []
        self.total_spins = 0
        self.correct_predictions = 0
        self.model_file = "models/top1_model.keras"
        
        # Configuration
        self.sequence_length = 10
        self.roulette_range = 37
        self.epochs = 50
        self.batch_size = 32
        
        # Betting
        self.bet_amount = 0.01
        self.payout = 35
        
        # Roulette colors
        self.red_numbers = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
        self.black_numbers = {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}

    def get_color(self, number):
        """Get the color of a roulette number"""
        if number == 0:
            return "green"
        elif number in self.red_numbers:
            return "red"
        else:
            return "black"
        
    def load_model(self):
        """Load or create the LSTM model"""
        if os.path.exists(self.model_file):
            print(f"✅ Loading existing model: {self.model_file}")
            return load_model(self.model_file)
        else:
            print("🔄 Creating new model...")
            return self.build_model()
    
    def build_model(self):
        """Build LSTM neural network"""
        model = Sequential([
            LSTM(128, input_shape=(self.sequence_length, 1), return_sequences=True),
            Dropout(0.2),
            LSTM(64, return_sequences=False),
            Dropout(0.2),
            Dense(64, activation="relu"),
            Dense(self.roulette_range, activation="softmax")
        ])
        model.compile(
            loss="categorical_crossentropy",
            optimizer="adam",
            metrics=["accuracy"]
        )
        return model
    
    def preprocess_data(self, data):
        """Prepare roulette data for LSTM training"""
        X, y = [], []
        for i in range(len(data) - self.sequence_length):
            X.append(data[i : i + self.sequence_length])
            y.append(data[i + self.sequence_length])
        
        if not X:
            return None, None
            
        X = np.array(X) / 36.0
        X = X.reshape((X.shape[0], self.sequence_length, 1))
        y = to_categorical(y, num_classes=self.roulette_range)
        return X, y
    
    def predict_numbers(self, recent_results):
        """Predict the single most likely number"""
        if len(recent_results) < self.sequence_length:
            return [0]  # Default to zero
            
        model = self.load_model()
        sequence = np.array(recent_results[-self.sequence_length:]) / 36.0
        sequence = sequence.reshape((1, self.sequence_length, 1))
        
        probabilities = model.predict(sequence, verbose=0)[0]
        top_index = np.argmax(probabilities)
        predicted_number = int(top_index)
        
        return [predicted_number]
    
    def calculate_bets(self, predicted_numbers):
        """Calculate bet amount for the single predicted number"""
        total_bet = min(self.balance * 0.1, self.bet_amount)
        return {num: total_bet for num in predicted_numbers}