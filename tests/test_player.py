"""
Unit tests for player module
"""

import unittest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from player import Player, ScoreCalculator


class TestPlayer(unittest.TestCase):
    """Test Player class"""
    
    def test_player_creation(self):
        """Test player initialization"""
        player = Player("Test Player")
        
        self.assertEqual(player.name, "Test Player")
        self.assertEqual(player.score, 0)
        self.assertEqual(len(player.score_history), 0)
        self.assertEqual(len(player.round_scores), 0)
    
    def test_add_score(self):
        """Test adding score"""
        player = Player("Test Player")
        
        player.add_score(1, 50, "full_house")
        
        self.assertEqual(player.score, 50)
        self.assertEqual(len(player.score_history), 1)
        self.assertEqual(len(player.round_scores), 1)
        
        # Check score history entry
        history_entry = player.score_history[0]
        self.assertEqual(history_entry['round'], 1)
        self.assertEqual(history_entry['score'], 50)
        self.assertEqual(history_entry['category'], "full_house")
        self.assertEqual(history_entry['total'], 50)
        
        # Check round scores
        self.assertEqual(player.round_scores[1], 50)
        
        # Add another score
        player.add_score(2, 30, "three_of_a_kind")
        
        self.assertEqual(player.score, 80)
        self.assertEqual(len(player.score_history), 2)
        self.assertEqual(len(player.round_scores), 2)
        self.assertEqual(player.round_scores[2], 30)
    
    def test_get_score_summary(self):
        """Test getting score summary as DataFrame"""
        player = Player("Test Player")
        
        # Add some scores
        player.add_score(1, 50, "full_house")
        player.add_score(2, 30, "three_of_a_kind")
        player.add_score(3, 40, "straight")
        
        df = player.get_score_summary()
        
        # Check DataFrame properties
        self.assertEqual(len(df), 3)
        self.assertEqual(list(df.columns), ['round', 'score', 'category', 'total', 'player'])
        
        # Check values
        self.assertEqual(df.iloc[0]['round'], 1)
        self.assertEqual(df.iloc[0]['score'], 50)
        self.assertEqual(df.iloc[0]['category'], "full_house")
        self.assertEqual(df.iloc[0]['total'], 50)
        
        self.assertEqual(df.iloc[2]['round'], 3)
        self.assertEqual(df.iloc[2]['total'], 120)  # 50 + 30 + 40
    
    def test_get_statistics(self):
        """Test getting player statistics"""
        player = Player("Test Player")
        
        # Add scores
        player.add_score(1, 50, "full_house")
        player.add_score(2, 30, "three_of_a_kind")
        player.add_score(3, 40, "straight")
        
        stats = player.get_statistics()
        
        self.assertEqual(stats['name'], "Test Player")
        self.assertEqual(stats['total_score'], 120)
        self.assertAlmostEqual(stats['average_score'], 40.0, places=1)
        self.assertEqual(stats['rounds_played'], 3)
        self.assertEqual(stats['best_score'], 50.0)
        self.assertEqual(stats['best_category'], "full_house")
    
    def test_player_string(self):
        """Test string representation"""
        player = Player("Test Player")
        player.add_score(1, 50, "full_house")
        
        self.assertEqual(str(player), "Test Player: 50 points")


class TestScoreCalculator(unittest.TestCase):
    """Test ScoreCalculator class"""
    
    def test_calculate_score_valid(self):
        """Test score calculation with valid dice"""
        calculator = ScoreCalculator()
        
        # Test with 12 dice
        dice_values = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6]
        result = calculator.calculate_score(dice_values)
        
        self.assertIn('category', result)
        self.assertIn('score', result)
        self.assertIn('counts', result)
        
        self.assertEqual(len(result['counts']), 6)  # Should have counts for 1-6
        
        # Check that all dice values are counted
        counts = result['counts']
        for i in range(1, 7):
            self.assertEqual(counts[i], 2)
    
    def test_calculate_score_invalid(self):
        """Test score calculation with invalid dice count"""
        calculator = ScoreCalculator()
        
        # Test with wrong number of dice
        with self.assertRaises(ValueError):
            calculator.calculate_score([1, 2, 3, 4, 5])  # Only 5 dice
    
    def test_analyze_dice(self):
        """Test dice analysis"""
        calculator = ScoreCalculator()
        
        dice_values = [1, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6]
        analysis = calculator.analyze_dice(dice_values)
        
        self.assertIn('counts', analysis)
        self.assertIn('suggestions', analysis)
        self.assertIn('total', analysis)
        
        counts = analysis['counts']
        self.assertEqual(counts[1], 3)  # Three 1s
        self.assertEqual(counts[6], 1)  # One 6
        
        self.assertEqual(analysis['total'], sum(dice_values))
        
        # Should have suggestions
        self.assertGreater(len(analysis['suggestions']), 0)


if __name__ == '__main__':
    unittest.main()