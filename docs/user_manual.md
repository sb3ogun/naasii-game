# Naasii Dice Game - User Manual

## Introduction
Naasii is a dice game from Coyote & Crow, created by Kenna Alexander. This Python implementation provides both a basic version and an enhanced version with additional features.

## Game Rules

### Official Rules (Simplified)
1. **Players**: 2-4 players
2. **Dice**: 12 six-sided dice
3. **Turns**: Each player gets 3 rolls per turn
4. **Scoring**: Points awarded based on dice combinations
5. **Rounds**: Game consists of multiple rounds (default: 10)
6. **Winning**: Player with highest total score after all rounds wins

### Scoring (This Implementation)
- **Pairs/Triples**: Score increases with more dice of the same value
- **Straights**: Consecutive numbers (3+)
- **Combinations**: Multiple pairs, triples, etc.

## How to Play

### Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Run basic game
python naasii_game.py

# Run enhanced game (recommended)
python enhanced_naasii.py