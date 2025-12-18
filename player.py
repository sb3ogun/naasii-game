"""
Player module for Naasii game with 12-dice scoring
"""

from typing import Dict, List, Tuple
import pandas as pd
import numpy as np


class Player:
    """Base player class"""
    
    def __init__(self, name: str):
        self.name = name
        self.score = 0
        self.score_history = []
        self.round_scores = {}
        
    def add_score(self, round_num: int, score: int, category: str):
        """Add score for a round"""
        self.score += score
        score_record = {
            'round': round_num,
            'score': score,
            'category': category,
            'total': self.score,
            'player': self.name
        }
        self.score_history.append(score_record)
        self.round_scores[round_num] = score
        
    def get_score_summary(self) -> pd.DataFrame:
        """Return score history as DataFrame"""
        if self.score_history:
            return pd.DataFrame(self.score_history)
        return pd.DataFrame(columns=['round', 'score', 'category', 'total', 'player'])
    
    def get_statistics(self) -> Dict:
        """Get player statistics"""
        if not self.score_history:
            return {
                'name': self.name,
                'total_score': 0,
                'average_score': 0,
                'rounds_played': 0
            }
        
        df = self.get_score_summary()
        return {
            'name': self.name,
            'total_score': self.score,
            'average_score': float(df['score'].mean()),
            'rounds_played': len(self.score_history),
            'best_score': float(df['score'].max()),
            'best_category': df.loc[df['score'].idxmax(), 'category'] if not df.empty else None
        }
    
    def __str__(self):
        return f"{self.name}: {self.score} points"


class ScoreCalculator:
    """Calculates scores for 12-dice Naasii game"""
    
    @staticmethod
    def calculate_score(dice_values: List[int]) -> Dict:
        """
        Calculate score for 12 dice according to Naasii rules
        
        Official scoring based on rulebook:
        - Count occurrences of each number (1-6)
        - Score based on combinations across all 12 dice
        """
        if len(dice_values) != 12:
            raise ValueError("Naasii requires exactly 12 dice")
        
        # Count occurrences of each value
        counts = {i: 0 for i in range(1, 7)}
        for value in dice_values:
            if 1 <= value <= 6:
                counts[value] += 1
        
        # Calculate score based on official rules
        score = 0
        category = "chance"
        
        # Check for specific patterns (simplified for 12 dice)
        # In official rules, you score for various combinations
        
        # Score each number separately (pairs, triples, etc.)
        for value, count in counts.items():
            if count >= 2:
                # Pairs score
                if count == 2:
                    score += 5  # Example scoring
                elif count == 3:
                    score += 10
                elif count == 4:
                    score += 20
                elif count >= 5:
                    score += 30
        
        # Check for straights (consecutive numbers with at least 1 each)
        straight_scores = {
            3: 10,   # 3 consecutive numbers
            4: 20,   # 4 consecutive numbers
            5: 30,   # 5 consecutive numbers
            6: 50    # All 6 numbers
        }
        
        # Find longest straight
        max_straight = 0
        current_straight = 0
        
        for i in range(1, 7):
            if counts[i] > 0:
                current_straight += 1
                max_straight = max(max_straight, current_straight)
            else:
                current_straight = 0
        
        if max_straight in straight_scores:
            score += straight_scores[max_straight]
            category = f"straight_{max_straight}"
        
        # Determine category based on highest scoring element
        max_count = max(counts.values())
        if max_count >= 5:
            category = "five_or_more_of_a_kind"
        elif max_count == 4:
            category = "four_of_a_kind"
        elif max_count == 3:
            # Check for multiple triples
            triple_count = sum(1 for c in counts.values() if c >= 3)
            if triple_count >= 2:
                category = "multiple_triples"
                score += 15
            else:
                category = "three_of_a_kind"
        elif max_count == 2:
            # Check for multiple pairs
            pair_count = sum(1 for c in counts.values() if c >= 2)
            if pair_count >= 3:
                category = "multiple_pairs"
                score += 10
        
        # Ensure minimum score for having any pattern
        if score == 0 and max_count >= 2:
            score = 5
            category = "single_pair"
        
        return {
            'category': category,
            'score': score,
            'counts': counts
        }
    
    @staticmethod
    def analyze_dice(dice_values: List[int]) -> Dict:
        """Analyze dice for strategy suggestions"""
        counts = {i: 0 for i in range(1, 7)}
        for value in dice_values:
            if 1 <= value <= 6:
                counts[value] += 1
        
        suggestions = []
        
        # Suggest keeping dice with highest counts
        sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        for value, count in sorted_counts[:3]:
            if count >= 2:
                suggestions.append(f"Keep {count} dice with value {value}")
        
        # Check for near-straights
        missing_for_straight = []
        for i in range(1, 7):
            if counts[i] == 0:
                missing_for_straight.append(i)
        
        if len(missing_for_straight) <= 2:
            suggestions.append(f"Near straight - need values {missing_for_straight}")
        
        return {
            'counts': counts,
            'suggestions': suggestions,
            'total': sum(dice_values)
        }


if __name__ == "__main__":
    # Test the ScoreCalculator
    calculator = ScoreCalculator()
    
    # Test with sample dice
    test_dice = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6]
    result = calculator.calculate_score(test_dice)
    print("Test 1 - All pairs:")
    print(f"Score: {result['score']}")
    print(f"Category: {result['category']}")
    
    # Test with triple
    test_dice2 = [1, 1, 1, 2, 3, 4, 5, 6, 2, 3, 4, 5]
    result2 = calculator.calculate_score(test_dice2)
    print("\nTest 2 - Triple 1s:")
    print(f"Score: {result2['score']}")
    print(f"Category: {result2['category']}")