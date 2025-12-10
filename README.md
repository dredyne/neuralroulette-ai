<h1 align="center">
  <br>
  <a href="https://github.com/Dredyne/NeuralRoulette-AI"><img src="assets/logo.svg" alt="NeuralRoulette AI" width="200"></a>
  <br>
  NeuralRoulette AI
  <br>
</h1>

<h4 align="center">An advanced machine learning system for predicting roulette outcomes using LSTM</a>.</h4>

<p align="center">
  <a href="https://github.com/Dredyne/NeuralRoulette-AI/issues">
    <img alt="GitHub Issues" src="https://img.shields.io/github/issues/Dredyne/NeuralRoulette-AI?style=plastic">
  </a>  
  <a href="https://github.com/Dredyne/NeuralRoulette-AI/pulls">
    <img alt="GitHub Pull Requests" src="https://img.shields.io/github/issues-pr/Dredyne/NeuralRoulette-AI?style=plastic">
  </a>
  <a href="https://discord.gg/UPyggZ2cK8">
    <img alt="Discord" src="https://img.shields.io/discord/827945236218904627?style=plastic&label=discord">
  </a>
  <a href="https://github.com/Dredyne/NeuralRoulette-AI/graphs/contributors">
    <img alt="GitHub contributors" src="https://img.shields.io/github/contributors/Dredyne/NeuralRoulette-AI?style=plastic">
  </a>
  <a href="https://github.com/sponsors/Dredyne">
    <img alt="GitHub Sponsors" src="https://img.shields.io/github/sponsors/Dredyne?style=plastic">
  </a>
</p>

<p align="center">
  <a href="#-project-overview">Project Overview</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-configuration">Configuration</a> •
  <a href="#-usage-examples">Usage Examples</a> •
  <a href="#-contributing">Contributing</a> •
  <a href="#-license">License</a>
</p>

<p align="center">
  <img src="assets/image.png" alt="NeuralRoulette AI Demo">
</p>

## ⚠️ Disclaimer

**Important**: This system is for educational and entertainment purposes only. Roulette is a game of chance with inherent house edge. No prediction system can guarantee wins. Always gamble responsibly and within your means.

## 🎯 Project Overview

NeuralRoulette-AI is a sophisticated roulette prediction system that leverages deep learning to analyze historical roulette spin data and predict future outcomes. The system uses multiple prediction strategies with varying risk levels to provide comprehensive betting insights.

### Key Features
- **Real-time Data**: Live WebSocket connection to Pragmatic Play Live Casino
- **Multiple Prediction Models**: Top-1, Top-3, Top-18 number predictions
- **LSTM Neural Networks**: Advanced sequence learning for pattern recognition
- **Betting Simulation**: Track win rates and balance changes
- **Model Persistence**: Save and load trained models for continuous learning
- **Comprehensive Logging**: Detailed session tracking and performance metrics

## 🧠 Technical Architecture

### Machine Learning Pipeline
1. **Data Collection**: Real-time roulette spin results via WebSocket
2. **Preprocessing**: Sequence generation and normalization
3. **Model Training**: LSTM networks with dropout regularization
4. **Prediction**: Multi-class classification for roulette outcomes
5. **Evaluation**: Win rate calculation and performance tracking

### Model Specifications
- **Architecture**: LSTM with 128→64→Dense layers
- **Sequence Length**: 10-18 historical spins
- **Output Classes**: 37 (0-36) for numbers
- **Training**: 50 epochs with Adam optimizer
- **Regularization**: 20% dropout to prevent overfitting

## 📁 Project Structure

```
NeuralRoulette-AI/
├── README.md                    # This documentation file
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore rules
├── main.py                      # Unified execution script for all strategies
├── config/                      # Configuration files
│   └── settings.py              # Centralized configuration management
├── src/                         # Source code
│   ├── strategies/              # Betting strategies
│   ├── data/                    # WebSocket data handling
│   └── utils/                   # Logging & utilities
└── models/                      # Trained model files
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- TensorFlow 2.x
- WebSocket support

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Dredyne/NeuralRoulette-AI.git
cd NeuralRoulette-AI
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the prediction system**
```bash
# List all available strategies
python main.py --list-strategies

# Run specific strategy
python main.py --strategy top1 --balance 100
python main.py --strategy top3 --balance 50
python main.py --strategy top18 --auto-train
```

### Requirements
```bash
tensorflow>=2.8.0
numpy>=1.21.0
websockets>=10.0
```

## 📊 Prediction Strategies

### 1. Top-1 Prediction
- **Strategy**: Predicts the single most likely number
- **Risk Level**: Very High
- **Payout**: 35:1
- **Break-even Win Rate**: >2.70%
- **Use Case**: High-risk, high-reward betting

### 2. Top-3 Prediction
- **Strategy**: Predicts the 3 most likely numbers
- **Risk Level**: High
- **Payout**: 35:1 per hit
- **Break-even Win Rate**: >8.57%
- **Use Case**: Balanced risk/reward approach

### 3. Top-18 Prediction
- **Strategy**: Predicts the 18 most likely numbers
- **Risk Level**: Medium
- **Payout**: 35:1 per hit
- **Break-even Win Rate**: >51.43%
- **Use Case**: Conservative betting strategy

## 🔧 Configuration

### WebSocket Settings
- **URL**: `wss://dga.pragmaticplaylive.net/ws`
- **Casino ID**: `ppcds00000003709`
- **Table**: `236` (Pragmatic Play Live Roulette)

### Model Parameters
- **Sequence Length**: 10-18 historical spins
- **Memory Limit**: 1000 recent spins
- **Training Frequency**: Every new spin
- **Batch Size**: 32
- **Epochs**: 50

## 📈 Performance Metrics

### Key Performance Indicators
- **Win Rate**: Percentage of correct predictions
- **Balance**: Simulated betting balance
- **ROI**: Return on investment over time
- **Accuracy**: Model prediction accuracy

### Logging
All sessions are logged with:
- Session timestamps
- Total spins
- Win rates
- Final balances

## 🎮 Usage Examples

### Basic Usage
```bash
# List all strategies
python main.py --list-strategies

# Run specific strategy
python main.py --strategy top1 --balance 100

# Run with automatic training
python main.py --strategy top18 --auto-train

# Use simulated data instead of live WebSocket
python main.py --strategy top3 --balance 50 --simulate
```

### Output Example
```
🎰 NeuralRoulette-AI Available Strategies
==================================================

TOP1 - Top-1 Single Number
  Description: Highest risk/reward - predicts single most likely number
  Risk Level: High
  Numbers to Predict: 1
  Target Win Rate: 2.71%
  Model File: top1_model.keras

TOP3 - Top-3 Numbers
  Description: Medium risk - predicts top 3 most likely numbers
  Risk Level: Medium
  Numbers to Predict: 3
  Target Win Rate: 8.11%
  Model File: top3_model.keras

TOP18 - Top-18 Numbers
  Description: Lower risk - covers half the wheel
  Risk Level: Low
  Numbers to Predict: 18
  Target Win Rate: 48.65%
  Model File: top18_model.keras
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Pragmatic Play for providing live roulette data
- TensorFlow team for the excellent ML framework
- WebSocket community for real-time communication tools

---

<div align="center"><sub>

Built with ❤️ by [Dredyne](https://github.com/Dredyne)</sub></div>
