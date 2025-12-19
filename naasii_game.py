"""
Naasii Dice Game - Clean Implementation
Official 12-dice version without icons
"""

import time
import sys
from dice import DiceSet
from player import Player, ScoreCalculator
import numpy as np


class NaasiiGame:
    """Clean game controller without icons"""
    
    def __init__(self):
        self.players = []
        self.current_round = 1
        self.max_rounds = 10
        self.dice_set = DiceSet()
        self.score_calculator = ScoreCalculator()
        self.game_stats = {
            'start_time': None,
            'total_rolls': 0
        }
        
    def setup_players(self):
        """Setup players without decorative elements"""
        print("=" * 60)
        print("NAASII DICE GAME - Official 12-Dice Version")
        print("=" * 60)
        print("Implementation for INST126 Final Project")
        print("=" * 60)
        
        # Get number of players
        num_players = self.get_number_input("Enter number of players (2-4): ", 2, 4)
        
        # Create players
        for i in range(num_players):
            while True:
                name = input(f"Enter name for Player {i+1}: ").strip()
                if name:
                    player = Player(name)
                    self.players.append(player)
                    print(f"Added player: {name}")
                    break
                else:
                    print("Name cannot be empty.")
    
    def get_number_input(self, prompt: str, min_val: int, max_val: int) -> int:
        """Get validated number input"""
        while True:
            try:
                value = input(prompt)
                if not value:
                    continue
                    
                value = int(value)
                if min_val <= value <= max_val:
                    return value
                print(f"Please enter a number between {min_val} and {max_val}")
            except ValueError:
                print("Please enter a valid number")
    
    def play_round(self):
        """Play a single round"""
        print("\n" + "=" * 40)
        print(f"ROUND {self.current_round}")
        print("=" * 40)
        
        for player in self.players:
            print(f"\n{player.name}'s turn")
            print("-" * 30)
            
            self.play_turn(player)
            
            # Show current standings
            self.display_standings()
            
            # Pause between players
            if player != self.players[-1]:
                time.sleep(1)
    
    def play_turn(self, player):
        """Play a single turn"""
        self.dice_set.reset_turn()
        
        # First roll
        print("First roll...")
        time.sleep(0.5)
        self.dice_set.roll_all()
        dice_values = self.dice_set.get_values()
        self.game_stats['total_rolls'] += 1
        
        print("Dice:")
        print(self.dice_set.display())
        
        # Additional rolls
        roll_num = 2
        while self.dice_set.rolls_remaining > 0:
            print(f"\nRoll {roll_num} - Rolls remaining: {self.dice_set.rolls_remaining}")
            
            # Show analysis
            analysis = self.score_calculator.analyze_dice(dice_values)
            if analysis['suggestions']:
                print("Suggestions:")
                for suggestion in analysis['suggestions'][:2]:
                    print(f"  {suggestion}")
            
            choice = input("Roll again? (y/n): ").lower().strip()
            if choice != 'y':
                break
            
            # Dice selection
            self.select_dice()
            
            print("Rolling...")
            time.sleep(0.5)
            self.dice_set.roll_all()
            dice_values = self.dice_set.get_values()
            self.game_stats['total_rolls'] += 1
            roll_num += 1
            
            print("Dice:")
            print(self.dice_set.display())
        
        # Calculate score
        self.calculate_score(player, dice_values)
    
    def select_dice(self):
        """Let player select dice to keep"""
        kept = self.dice_set.get_kept_indices()
        if kept:
            print(f"Currently kept dice: {[i+1 for i in kept]}")
        
        change = input("Select dice to keep? (y/n): ").lower().strip()
        if change == 'y':
            while True:
                try:
                    indices_input = input("Enter dice numbers (1-12) to keep, separated by spaces: ")
                    if not indices_input:
                        print("No dice selected")
                        break
                    
                    indices = []
                    for num in indices_input.split():
                        idx = int(num) - 1
                        if 0 <= idx < 12:
                            indices.append(idx)
                    
                    if indices:
                        # Clear all keeps
                        self.dice_set.release_all()
                        # Keep selected
                        self.dice_set.keep_dice(indices)
                        print(f"Keeping dice: {[i+1 for i in indices]}")
                        break
                    else:
                        print("No valid dice numbers entered")
                        
                except ValueError:
                    print("Please enter valid numbers (1-12)")
    
    def calculate_score(self, player, dice_values):
        """Calculate and display score"""
        # Use numpy for analysis
        dice_array = np.array(dice_values)
        
        print("\nDice Analysis:")
        print(f"  Total: {np.sum(dice_array)}")
        print(f"  Average: {np.mean(dice_array):.2f}")
        print(f"  Standard Deviation: {np.std(dice_array):.2f}")
        
        # Calculate score
        score_result = self.score_calculator.calculate_score(dice_values)
        
        print("\nScoring Result:")
        print(f"  Category: {score_result['category'].replace('_', ' ').title()}")
        print(f"  Score: {score_result['score']} points")
        
        # Apply score
        player.add_score(self.current_round, score_result['score'], score_result['category'])
        
        print(f"\n{player.name}'s total: {player.score} points")
    
    def display_standings(self):
        """Display current standings"""
        print("\nCurrent Standings:")
        print("-" * 40)
        
        # Sort by score
        sorted_players = sorted(self.players, key=lambda p: p.score, reverse=True)
        
        for i, player in enumerate(sorted_players, 1):
            position = ""
            if i == 1:
                position = " (1st)"
            elif i == 2:
                position = " (2nd)"
            elif i == 3:
                position = " (3rd)"
            
            print(f"{i}. {player.name}: {player.score} points{position}")
    
    def display_final_results(self):
        """Display final results"""
        print("\n" + "=" * 60)
        print("GAME OVER - FINAL RESULTS")
        print("=" * 60)
        
        # Sort players
        sorted_players = sorted(self.players, key=lambda p: p.score, reverse=True)
        
        print("\nFinal Standings:")
        for i, player in enumerate(sorted_players, 1):
            print(f"\n{i}. {player.name}")
            print(f"   Total Score: {player.score}")
            
            # Show statistics
            stats = player.get_statistics()
            if stats['rounds_played'] > 0:
                print(f"   Average per Round: {stats['average_score']:.1f}")
                print(f"   Best Score: {stats['best_score']}")
                if stats['best_category']:
                    print(f"   Best Category: {stats['best_category']}")
        
        print("\n" + "*" * 40)
        print(f"WINNER: {sorted_players[0].name}")
        print("*" * 40)
        
        # Game statistics
        print("\nGame Statistics:")
        print(f"  Total Rounds: {self.current_round - 1}")
        print(f"  Total Rolls: {self.game_stats['total_rolls']}")
        
        if self.game_stats['start_time']:
            duration = time.time() - self.game_stats['start_time']
            minutes = int(duration // 60)
            seconds = int(duration % 60)
            print(f"  Game Duration: {minutes}m {seconds}s")
    
    def run(self):
        """Main game loop"""
        self.game_stats['start_time'] = time.time()
        
        print("\nStarting game...")
        print(f"Total rounds: {self.max_rounds}")
        print("=" * 40)
        
        try:
            for round_num in range(1, self.max_rounds + 1):
                self.current_round = round_num
                self.play_round()
                
                if round_num < self.max_rounds:
                    print("\n" + "-" * 40)
                    cont = input("Continue to next round? (y/n): ").lower().strip()
                    if cont != 'y':
                        print("\nEnding game early.")
                        break
            
            self.display_final_results()
            
        except KeyboardInterrupt:
            print("\nGame interrupted.")
        except Exception as e:
            print(f"\nError: {e}")


def main():
    """Entry point"""
    print("=" * 60)
    print("NAASII DICE GAME - FINAL PROJECT")
    print("=" * 60)
    print("Official 12-dice implementation")
    print("Credits: Game design by Kenna Alexander (Coyote & Crow)")
    print("=" * 60)
    
    # Check dependencies
    print("\nChecking dependencies...")
    try:
        import numpy
        import pandas
        print("All dependencies available.")
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Some features may not work.")
    
    # Create and run game
    game = NaasiiGame()
    
    try:
        game.setup_players()
        game.run()
    except KeyboardInterrupt:
        print("\nGame terminated.")
    except Exception as e:
        print(f"\nError: {e}")
    finally:
        print("\nThank you for playing Naasii!")


if __name__ == "__main__":
    main()