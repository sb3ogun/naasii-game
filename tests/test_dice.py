"""
Unit tests for dice module
"""

import unittest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dice import Die, DiceSet


class TestDie(unittest.TestCase):
    """Test Die class"""
    
    def test_die_creation(self):
        """Test die initialization"""
        die = Die()
        self.assertEqual(die.value, 1)
        self.assertFalse(die.kept)
    
    def test_die_roll(self):
        """Test die rolling"""
        die = Die()
        for _ in range(10):
            value = die.roll()
            self.assertTrue(1 <= value <= 6)
    
    def test_die_keep(self):
        """Test die keep functionality"""
        die = Die()
        die.keep()
        self.assertTrue(die.kept)
        die.release()
        self.assertFalse(die.kept)
    
    def test_die_string(self):
        """Test string representation"""
        die = Die()
        die.value = 5
        self.assertEqual(str(die), "5")
        die.keep()
        self.assertEqual(str(die), "[5]")


class TestDiceSet(unittest.TestCase):
    """Test DiceSet class"""
    
    def test_dice_set_creation(self):
        """Test dice set initialization"""
        dice_set = DiceSet()
        self.assertEqual(len(dice_set.dice), 12)
        self.assertEqual(dice_set.rolls_remaining, 3)
        self.assertEqual(dice_set.turn_rolls, 0)
    
    def test_roll_all(self):
        """Test rolling all dice"""
        dice_set = DiceSet()
        values = dice_set.roll_all()
        
        self.assertEqual(len(values), 12)
        self.assertEqual(dice_set.rolls_remaining, 2)
        self.assertEqual(dice_set.turn_rolls, 1)
        
        for value in values:
            self.assertTrue(1 <= value <= 6)
    
    def test_keep_dice(self):
        """Test keeping specific dice"""
        dice_set = DiceSet()
        
        # Keep dice at indices 0, 2, 4
        dice_set.keep_dice([0, 2, 4])
        
        kept_indices = dice_set.get_kept_indices()
        self.assertEqual(len(kept_indices), 3)
        self.assertIn(0, kept_indices)
        self.assertIn(2, kept_indices)
        self.assertIn(4, kept_indices)
        
        # Test that kept dice are actually marked as kept
        self.assertTrue(dice_set.dice[0].kept)
        self.assertTrue(dice_set.dice[2].kept)
        self.assertTrue(dice_set.dice[4].kept)
        
        # Test that other dice are not kept
        self.assertFalse(dice_set.dice[1].kept)
    
    def test_reset_turn(self):
        """Test resetting turn"""
        dice_set = DiceSet()
        dice_set.roll_all()
        dice_set.keep_dice([0, 1, 2])
        
        dice_set.reset_turn()
        
        self.assertEqual(dice_set.rolls_remaining, 3)
        self.assertEqual(dice_set.turn_rolls, 0)
        
        # Check that no dice are kept after reset
        kept_indices = dice_set.get_kept_indices()
        self.assertEqual(len(kept_indices), 0)
        
        for die in dice_set.dice:
            self.assertFalse(die.kept)
    
    def test_get_values(self):
        """Test getting dice values"""
        dice_set = DiceSet()
        values = dice_set.get_values()
        
        self.assertEqual(len(values), 12)
        self.assertEqual(values, [die.value for die in dice_set.dice])
    
    def test_keep_all(self):
        """Test keeping all dice"""
        dice_set = DiceSet()
        dice_set.keep_all()
        
        kept_indices = dice_set.get_kept_indices()
        self.assertEqual(len(kept_indices), 12)
    
    def test_release_all(self):
        """Test releasing all dice"""
        dice_set = DiceSet()
        dice_set.keep_all()
        dice_set.release_all()
        
        kept_indices = dice_set.get_kept_indices()
        self.assertEqual(len(kept_indices), 0)
    
    def test_get_statistics(self):
        """Test getting dice statistics"""
        dice_set = DiceSet()
        dice_set.roll_all()
        
        stats = dice_set.get_statistics()
        
        self.assertIn('values', stats)
        self.assertIn('sum', stats)
        self.assertIn('mean', stats)
        self.assertIn('counts', stats)
        self.assertIn('rolls_used', stats)
        self.assertIn('kept_count', stats)
        
        self.assertEqual(len(stats['values']), 12)
        self.assertEqual(stats['rolls_used'], 1)
        self.assertEqual(stats['kept_count'], 0)


if __name__ == '__main__':
    unittest.main()