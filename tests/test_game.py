"""
Integration tests for game functionality
"""

import unittest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dice import DiceSet
from player import Player, ScoreCalculator


class TestGameIntegration(unittest.TestCase):
    """Integration tests for game components"""
    
    def test_full_turn_flow(self):
        """Test a complete turn flow"""
        # Create components
        player = Player("Test Player")
        dice_set = DiceSet()
        calculator = ScoreCalculator()
        
        # Start turn
        dice_set.reset_turn()
        self.assertEqual(dice_set.rolls_remaining, 3)
        
        # First roll
        dice_values = dice_set.roll_all()
        self.assertEqual(len(dice_values), 12)
        self.assertEqual(dice_set.rolls_remaining, 2)
        
        # Keep some dice
        dice_set.keep_dice([0, 1, 2])  # Keep first 3 dice
        kept_indices = dice_set.get_kept_indices()
        self.assertEqual(len(kept_indices), 3)
        
        # Second roll (only unkept dice should roll)
        dice_values2 = dice_set.roll_all()
        self.assertEqual(dice_set.rolls_remaining, 1)
        
        # Calculate score
        final_values = dice_set.get_values()
        score_result = calculator.calculate_score(final_values)
        
        # Apply score to player
        player.add_score(1, score_result['score'], score_result['category'])
        
        # Verify player state
        self.assertEqual(player.score, score_result['score'])
        self.assertEqual(len(player.score_history), 1)
        
        history_entry = player.score_history[0]
        self.assertEqual(history_entry['score'], score_result['score'])
        self.assertEqual(history_entry['category'], score_result['category'])
    
    def test_multiple_players(self):
        """Test game with multiple players"""
        players = [
            Player("Player 1"),
            Player("Player 2"),
            Player("Player 3")
        ]
        
        dice_set = DiceSet()
        calculator = ScoreCalculator()
        
        # Simulate a round
        for i, player in enumerate(players):
            dice_set.reset_turn()
            
            # Roll dice
            dice_set.roll_all()
            
            # Get score
            dice_values = dice_set.get_values()
            score_result = calculator.calculate_score(dice_values)
            
            # Apply score (different scores for each player)
            score = score_result['score'] + (i * 5)  # Vary scores
            player.add_score(1, score, score_result['category'])
        
        # Verify all players have scores
        for i, player in enumerate(players):
            self.assertGreater(player.score, 0)
            self.assertEqual(len(player.score_history), 1)
    
    def test_score_calculation_consistency(self):
        """Test that score calculation is consistent"""
        calculator = ScoreCalculator()
        
        # Test with same dice values multiple times
        dice_values = [1, 1, 1, 2, 2, 2, 3, 3, 4, 4, 5, 6]
        
        # Calculate score multiple times
        results = []
        for _ in range(5):
            result = calculator.calculate_score(dice_values.copy())
            results.append((result['category'], result['score']))
        
        # All results should be the same
        first_category, first_score = results[0]
        for category, score in results[1:]:
            self.assertEqual(category, first_category)
            self.assertEqual(score, first_score)
    
    def test_dice_statistics(self):
        """Test dice statistics collection"""
        dice_set = DiceSet()
        
        # Roll multiple times
        for _ in range(3):
            dice_set.roll_all()
        
        stats = dice_set.get_statistics()
        
        # Verify statistics
        self.assertEqual(stats['rolls_used'], 3)
        self.assertEqual(stats['kept_count'], 0)
        
        # Values should be within valid range
        for value in stats['values']:
            self.assertTrue(1 <= value <= 6)
        
        # Sum should be reasonable
        self.assertTrue(12 <= stats['sum'] <= 72)  # 12*1 to 12*6


if __name__ == '__main__':
    unittest.main()