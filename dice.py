"""
Dice module for Naasii game
"""

import random
from typing import List, Dict


class Die:
    """Represents a single six-sided die"""
    
    def __init__(self):
        self.value = 1
        self.kept = False
    
    def roll(self) -> int:
        """Roll the die if it's not kept"""
        if not self.kept:
            self.value = random.randint(1, 6)
        return self.value
    
    def keep(self):
        """Mark die as kept (won't be re-rolled)"""
        self.kept = True
    
    def release(self):
        """Release die (allow re-rolling)"""
        self.kept = False
    
    def __str__(self):
        return f"[{self.value}]" if self.kept else f"{self.value}"
    
    def __repr__(self):
        return f"Die(value={self.value}, kept={self.kept})"


class DiceSet:
    """Manages a set of 12 dice for Naasii game"""
    
    def __init__(self):
        self.dice = [Die() for _ in range(12)]  # 12 dice for official rules
        self.rolls_remaining = 3
        self.turn_rolls = 0
    
    def roll_all(self) -> List[int]:
        """Roll all unkept dice"""
        if self.rolls_remaining <= 0:
            raise ValueError("No rolls remaining this turn")
        
        self.rolls_remaining -= 1
        self.turn_rolls += 1
        values = [die.roll() for die in self.dice]
        return values
    
    def get_values(self) -> List[int]:
        """Get current values of all dice"""
        return [die.value for die in self.dice]
    
    def get_kept_indices(self) -> List[int]:
        """Get indices of kept dice"""
        return [i for i, die in enumerate(self.dice) if die.kept]
    
    def keep_dice(self, indices: List[int]):
        """Keep specific dice by index"""
        for idx in indices:
            if 0 <= idx < len(self.dice):
                self.dice[idx].keep()
    
    def keep_all(self):
        """Keep all dice"""
        for die in self.dice:
            die.keep()
    
    def release_all(self):
        """Release all dice"""
        for die in self.dice:
            die.release()
    
    def reset_turn(self):
        """Reset dice for new turn"""
        self.release_all()
        self.rolls_remaining = 3
        self.turn_rolls = 0
    
    def display(self) -> str:
        """Display dice in readable format"""
        dice_display = []
        for i, die in enumerate(self.dice):
            status = "K" if die.kept else "-"
            dice_display.append(f"{i+1:2d}:{die.value}{status}")
        
        # Format in rows of 6 for readability
        rows = []
        for i in range(0, 12, 6):
            row = dice_display[i:i+6]
            rows.append("  ".join(row))
        
        return "\n".join(rows)
    
    def display_simple(self) -> str:
        """Simple display without numbers"""
        return " ".join(str(die) for die in self.dice)
    
    def get_statistics(self) -> Dict:
        """Get statistics about current dice"""
        values = self.get_values()
        counts = {}
        for value in values:
            counts[value] = counts.get(value, 0) + 1
        
        return {
            'values': values,
            'sum': sum(values),
            'mean': sum(values) / len(values),
            'counts': counts,
            'rolls_used': 3 - self.rolls_remaining,
            'kept_count': len(self.get_kept_indices())
        }
    
    def __str__(self):
        return f"DiceSet(12 dice, {self.rolls_remaining} rolls left)"


if __name__ == "__main__":
    # Test the dice module
    dice = DiceSet()
    print("Initial dice set created")
    print(f"Number of dice: {len(dice.dice)}")
    
    print("\nRolling dice...")
    values = dice.roll_all()
    print(f"Values: {values}")
    print(f"Rolls remaining: {dice.rolls_remaining}")
    
    print("\nDisplay:")
    print(dice.display())
    
    # Test keeping dice
    print("\nKeeping dice 1, 3, 5...")
    dice.keep_dice([0, 2, 4])
    print("Kept indices:", dice.get_kept_indices())
    print(dice.display())
    
    # Roll again (kept dice won't change)
    print("\nRolling again...")
    values2 = dice.roll_all()
    print(f"Values: {values2}")
    print(f"Rolls remaining: {dice.rolls_remaining}")
    print(dice.display())
    
    # Get statistics
    stats = dice.get_statistics()
    print("\nStatistics:")
    for key, value in stats.items():
        if key == 'counts':
            print(f"  {key}:")
            for val, count in sorted(value.items()):
                print(f"    {val}: {count}")
        else:
            print(f"  {key}: {value}")
