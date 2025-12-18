"""
Enhanced Naasii Game - Clean Professional Version
Includes all advanced features without icons
"""

import time
import sys
import os
import json
from datetime import datetime
from typing import List, Dict, Optional
from dice import DiceSet
from player import Player, ScoreCalculator
import numpy as np
import pandas as pd

# Try to import visualization libraries
try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    VISUALIZATION_AVAILABLE = True
except ImportError:
    VISUALIZATION_AVAILABLE = False
    print("Note: Visualization libraries not available.")


class GameStateManager:
    """Manages game state saving and loading"""
    
    def __init__(self, game):
        self.game = game
        self.save_dir = "saves"
        os.makedirs(self.save_dir, exist_ok=True)
    
    def create_save_state(self) -> Dict:
        """Create save state from current game"""
        players_data = []
        for player in self.game.players:
            player_data = {
                'name': player.name,
                'score': player.score,
                'score_history': player.score_history
            }
            players_data.append(player_data)
        
        return {
            'players': players_data,
            'current_round': self.game.current_round,
            'max_rounds': self.game.max_rounds,
            'game_date': datetime.now().isoformat(),
            'version': '1.0'
        }
    
    def save_game(self, filename: Optional[str] = None) -> str:
        """Save game to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"naasii_save_{timestamp}.json"
        
        save_state = self.create_save_state()
        filepath = os.path.join(self.save_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(save_state, f, indent=2, default=str)
            
            print(f"Game saved to: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"Error saving game: {e}")
            return ""
    
    def load_game(self, filename: str) -> bool:
        """Load game from JSON file"""
        filepath = os.path.join(self.save_dir, filename)
        
        if not os.path.exists(filepath):
            print(f"Save file not found: {filepath}")
            return False
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                save_state = json.load(f)
            
            # Reset and restore game
            self.game.players = []
            
            for player_data in save_state['players']:
                player = Player(player_data['name'])
                player.score = player_data['score']
                player.score_history = player_data['score_history']
                self.game.players.append(player)
            
            # Restore game state
            self.game.current_round = save_state['current_round']
            self.game.max_rounds = save_state['max_rounds']
            
            print(f"Game loaded from: {filepath}")
            print(f"Game date: {save_state['game_date']}")
            return True
            
        except Exception as e:
            print(f"Error loading game: {e}")
            return False


class GameVisualizer:
    """Creates visualizations for game statistics"""
    
    def __init__(self):
        if not VISUALIZATION_AVAILABLE:
            self.available = False
            return
        
        self.available = True
        self.output_dir = "visualizations"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Set style
        sns.set_style("whitegrid")
    
    def plot_score_progression(self, players: List[Player], 
                              save: bool = True) -> Optional[str]:
        """Plot score progression over rounds"""
        if not self.available:
            return None
        
        plt.figure(figsize=(12, 6))
        
        colors = ['blue', 'green', 'red', 'purple']
        
        for i, player in enumerate(players):
            df = player.get_score_summary()
            if not df.empty:
                df['cumulative'] = df['total']
                
                plt.plot(df['round'], df['cumulative'], 
                        label=player.name, marker='o',
                        color=colors[i % len(colors)],
                        linewidth=2)
        
        plt.title('Naasii Game - Score Progression', fontsize=16)
        plt.xlabel('Round', fontsize=12)
        plt.ylabel('Cumulative Score', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        if save:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"score_progression_{timestamp}.png"
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            return filepath
        else:
            plt.show()
            return None
    
    def create_statistics_report(self, players: List[Player]) -> str:
        """Create a statistics report"""
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("NAASII GAME STATISTICS REPORT")
        report_lines.append("=" * 60)
        report_lines.append("")
        
        report_lines.append("PLAYER STATISTICS")
        report_lines.append("-" * 40)
        
        for player in players:
            stats = player.get_statistics()
            report_lines.append(f"\nPlayer: {stats['name']}")
            report_lines.append(f"  Total Score: {stats['total_score']}")
            report_lines.append(f"  Average Score: {stats['average_score']:.1f}")
            report_lines.append(f"  Rounds Played: {stats['rounds_played']}")
            if stats['best_category']:
                report_lines.append(f"  Best Score: {stats['best_score']} ({stats['best_category']})")
        
        # Save report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"game_report_{timestamp}.txt"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_lines))
        
        return filepath


class EnhancedNaasiiGame:
    """Enhanced game with all features"""
    
    def __init__(self):
        self.players = []
        self.current_round = 1
        self.max_rounds = 10
        self.dice_set = DiceSet()
        self.score_calculator = ScoreCalculator()
        self.state_manager = GameStateManager(self)
        self.visualizer = GameVisualizer()
        
        self.auto_save = True
        self.game_stats = {
            'start_time': None,
            'total_rolls': 0
        }
    
    def show_menu(self):
        """Display main menu"""
        print("=" * 60)
        print("NAASII - ENHANCED VERSION")
        print("=" * 60)
        print("1. New Game")
        print("2. Load Game")
        print("3. Game Settings")
        print("4. View Statistics")
        print("5. Exit")
        print("=" * 60)
    
    def game_settings(self):
        """Configure game settings"""
        print("\nGAME SETTINGS")
        print("-" * 40)
        
        try:
            rounds = input("Number of rounds (default 10): ").strip()
            if rounds:
                self.max_rounds = max(3, min(int(rounds), 20))
        except:
            self.max_rounds = 10
        
        autosave = input("Auto-save after each round? (y/n): ").lower().strip()
        self.auto_save = autosave == 'y'
        
        print(f"\nSettings saved:")
        print(f"  Rounds: {self.max_rounds}")
        print(f"  Auto-save: {'Enabled' if self.auto_save else 'Disabled'}")
    
    def setup_players(self):
        """Setup players"""
        print("\nPLAYER SETUP")
        print("-" * 40)
        
        num_players = self.get_number_input("Enter number of players (2-4): ", 2, 4)
        
        player_names = set()
        for i in range(num_players):
            while True:
                name = input(f"\nEnter name for Player {i+1}: ").strip()
                
                if not name:
                    print("Name cannot be empty")
                    continue
                
                if name in player_names:
                    print("Name already taken")
                    continue
                
                player = Player(name)
                self.players.append(player)
                player_names.add(name)
                print(f"Player '{name}' added")
                break
    
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
        """Play a round"""
        print(f"\n=== ROUND {self.current_round} ===")
        
        for player in self.players:
            print(f"\n{player.name}'s Turn")
            print("-" * 30)
            
            self.play_enhanced_turn(player)
            
            self.display_standings()
            
            if player != self.players[-1]:
                time.sleep(1)
        
        # Auto-save
        if self.auto_save:
            self.state_manager.save_game()
    
    def play_enhanced_turn(self, player):
        """Enhanced turn with strategy"""
        self.dice_set.reset_turn()
        
        # First roll
        print("First roll...")
        time.sleep(0.5)
        self.dice_set.roll_all()
        dice_values = self.dice_set.get_values()
        self.game_stats['total_rolls'] += 1
        
        print("Dice:")
        print(self.dice_set.display())
        
        # Show analysis
        analysis = self.score_calculator.analyze_dice(dice_values)
        if analysis['suggestions']:
            print("\nSuggestions:")
            for suggestion in analysis['suggestions'][:2]:
                print(f"  {suggestion}")
        
        # Additional rolls
        roll_num = 2
        while self.dice_set.rolls_remaining > 0:
            print(f"\nRoll {roll_num} - Rolls left: {self.dice_set.rolls_remaining}")
            
            choice = input("Roll again? (y/n): ").lower().strip()
            if choice != 'y':
                break
            
            self.select_dice_advanced()
            
            print("Rolling...")
            time.sleep(0.5)
            self.dice_set.roll_all()
            dice_values = self.dice_set.get_values()
            self.game_stats['total_rolls'] += 1
            roll_num += 1
            
            print("Dice:")
            print(self.dice_set.display())
            
            # Update analysis
            analysis = self.score_calculator.analyze_dice(dice_values)
        
        # Calculate score
        self.calculate_final_score(player, dice_values)
    
    def select_dice_advanced(self):
        """Advanced dice selection"""
        print("\nDice Selection:")
        print("  Enter dice numbers (1-12) to keep")
        print("  'all' to keep all dice")
        print("  'none' to release all dice")
        print("  'done' to finish")
        
        while True:
            choice = input("Selection: ").lower().strip()
            
            if choice == 'done':
                break
            elif choice == 'all':
                self.dice_set.keep_all()
                print("All dice kept")
                break
            elif choice == 'none':
                self.dice_set.release_all()
                print("All dice released")
            elif choice.replace(' ', '').isdigit():
                try:
                    indices = [int(num)-1 for num in choice.split() 
                              if num.isdigit() and 1 <= int(num) <= 12]
                    if indices:
                        self.dice_set.release_all()
                        self.dice_set.keep_dice(indices)
                        print(f"Keeping dice: {[i+1 for i in indices]}")
                except:
                    print("Invalid input")
            else:
                print("Invalid option")
    
    def calculate_final_score(self, player, dice_values):
        """Calculate and display final score"""
        # Numpy analysis
        dice_array = np.array(dice_values)
        
        print("\nDice Analysis:")
        print(f"  Values: {dice_array}")
        print(f"  Mean: {np.mean(dice_array):.2f}")
        print(f"  Std Dev: {np.std(dice_array):.2f}")
        
        # Calculate score
        score_result = self.score_calculator.calculate_score(dice_values)
        
        print("\nScoring Result:")
        print(f"  Category: {score_result['category']}")
        print(f"  Score: {score_result['score']} points")
        
        # Show dice counts
        print("  Dice counts:")
        for value, count in score_result['counts'].items():
            if count > 0:
                print(f"    {value}: {count}")
        
        # Apply score
        player.add_score(self.current_round, score_result['score'], score_result['category'])
        
        print(f"\n{player.name}'s total: {player.score} points")
    
    def display_standings(self):
        """Display standings"""
        print("\nCurrent Standings:")
        print("-" * 40)
        
        sorted_players = sorted(self.players, key=lambda p: p.score, reverse=True)
        
        for i, player in enumerate(sorted_players, 1):
            print(f"{i}. {player.name}: {player.score}")
    
    def display_final_results(self):
        """Display final results"""
        print("\n" + "=" * 60)
        print("FINAL RESULTS")
        print("=" * 60)
        
        sorted_players = sorted(self.players, key=lambda p: p.score, reverse=True)
        
        print("\nFinal Standings:")
        for i, player in enumerate(sorted_players, 1):
            print(f"\n{i}. {player.name}")
            print(f"   Score: {player.score}")
            
            df = player.get_score_summary()
            if not df.empty:
                print(f"   Average: {df['score'].mean():.1f}")
                print(f"   Best: {df['score'].max()}")
        
        print("\n" + "*" * 40)
        print(f"WINNER: {sorted_players[0].name}")
        print("*" * 40)
        
        # Offer visualizations
        self.offer_visualizations()
    
    def offer_visualizations(self):
        """Offer to create visualizations"""
        if not VISUALIZATION_AVAILABLE:
            return
        
        print("\n" + "=" * 60)
        print("DATA VISUALIZATION")
        print("=" * 60)
        
        choice = input("\nCreate visualizations? (y/n): ").lower().strip()
        if choice != 'y':
            return
        
        print("\nCreating visualizations...")
        
        try:
            plot1 = self.visualizer.plot_score_progression(self.players)
            if plot1:
                print(f"Score progression chart: {plot1}")
            
            report = self.visualizer.create_statistics_report(self.players)
            print(f"Statistics report: {report}")
            
            print("\nFiles saved to 'visualizations/' folder")
            
        except Exception as e:
            print(f"Error creating visualizations: {e}")
    
    def run(self):
        """Main game loop"""
        self.game_stats['start_time'] = time.time()
        
        print("\nStarting game...")
        print(f"Rounds: {self.max_rounds}")
        print("=" * 40)
        
        for round_num in range(1, self.max_rounds + 1):
            self.current_round = round_num
            self.play_round()
            
            if round_num < self.max_rounds:
                print("\n" + "-" * 40)
                cont = input("Continue? (y/n): ").lower().strip()
                if cont != 'y':
                    print("\nEnding game early.")
                    break
        
        self.display_final_results()
    
    def main_menu(self):
        """Handle main menu"""
        while True:
            self.show_menu()
            choice = input("\nSelect option: ").strip()
            
            if choice == "1":
                self.__init__()
                self.game_settings()
                self.setup_players()
                self.run()
                
                again = input("\nPlay again? (y/n): ").lower().strip()
                if again != 'y':
                    break
                    
            elif choice == "2":
                filename = input("Enter save filename: ").strip()
                if filename and self.state_manager.load_game(filename):
                    self.run()
                    
            elif choice == "3":
                self.game_settings()
                
            elif choice == "4":
                self.view_statistics()
                
            elif choice == "5":
                print("\nThank you for playing!")
                break
                
            else:
                print("Invalid choice.")
    
    def view_statistics(self):
        """View statistics"""
        print("\nStatistics feature would load and display saved game data.")
        print("This requires existing save files.")


def main():
    """Entry point"""
    print("=" * 60)
    print("NAASII - ENHANCED VERSION")
    print("=" * 60)
    print("12-dice implementation with advanced features")
    print("Credits: Game design by Kenna Alexander")
    print("=" * 60)
    
    # Check dependencies
    print("\nChecking dependencies...")
    deps = ['numpy', 'pandas', 'matplotlib', 'seaborn']
    missing = []
    
    for dep in deps:
        try:
            __import__(dep)
            print(f"✓ {dep}")
        except ImportError:
            missing.append(dep)
            print(f"✗ {dep}")
    
    if missing:
        print(f"\nMissing: {', '.join(missing)}")
        print("Some features may not work.")
        print("Install with: pip install " + " ".join(missing))
    
    game = EnhancedNaasiiGame()
    
    try:
        game.main_menu()
    except KeyboardInterrupt:
        print("\n\nGame interrupted.")
    except Exception as e:
        print(f"\nError: {e}")
    finally:
        print("\nThank you for playing Naasii!")


if __name__ == "__main__":
    main()