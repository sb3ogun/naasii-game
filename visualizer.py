"""
Visualization module using matplotlib and seaborn
For Advanced Topics points
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import List, Dict, Optional
import os
from datetime import datetime


class GameVisualizer:
    """Creates visualizations for game data"""
    
    def __init__(self, output_dir: str = "plots"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Set seaborn style
        sns.set_style("whitegrid")
        self.colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    
    def create_score_chart(self, players_data: List[Dict], 
                          title: str = "Score Progression") -> str:
        """
        Create a score progression line chart
        
        Args:
            players_data: List of player data dictionaries
            title: Chart title
            
        Returns:
            Path to saved chart
        """
        plt.figure(figsize=(10, 6))
        
        for i, player_data in enumerate(players_data):
            if 'score_history' not in player_data:
                continue
            
            df = pd.DataFrame(player_data['score_history'])
            if not df.empty:
                # Calculate cumulative scores
                df['cumulative'] = df['total']
                
                # Plot line
                plt.plot(df['round'], df['cumulative'], 
                        label=player_data.get('name', f'Player {i+1}'),
                        marker='o',
                        color=self.colors[i % len(self.colors)],
                        linewidth=2)
        
        plt.title(title, fontsize=14)
        plt.xlabel('Round', fontsize=12)
        plt.ylabel('Total Score', fontsize=12)
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Save chart
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"score_chart_{timestamp}.png"
        filepath = os.path.join(self.output_dir, filename)
        
        plt.tight_layout()
        plt.savefig(filepath, dpi=150)
        plt.close()
        
        return filepath
    
    def create_score_distribution(self, players_data: List[Dict]) -> str:
        """
        Create box plot of score distribution
        
        Returns:
            Path to saved chart
        """
        plt.figure(figsize=(8, 6))
        
        scores_by_player = []
        player_names = []
        
        for player_data in players_data:
            if 'score_history' not in player_data:
                continue
            
            df = pd.DataFrame(player_data['score_history'])
            if not df.empty and 'score' in df.columns:
                scores_by_player.append(df['score'].values)
                player_names.append(player_data.get('name', 'Unknown'))
        
        if not scores_by_player:
            return ""
        
        # Create box plot
        plt.boxplot(scores_by_player, labels=player_names)
        plt.title('Score Distribution by Player', fontsize=14)
        plt.xlabel('Player', fontsize=12)
        plt.ylabel('Score per Round', fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3, axis='y')
        
        # Save chart
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"distribution_{timestamp}.png"
        filepath = os.path.join(self.output_dir, filename)
        
        plt.tight_layout()
        plt.savefig(filepath, dpi=150)
        plt.close()
        
        return filepath
    
    def create_category_chart(self, players_data: List[Dict]) -> str:
        """
        Create bar chart of scoring category frequency
        
        Returns:
            Path to saved chart
        """
        # Collect all categories
        all_categories = []
        for player_data in players_data:
            if 'score_history' not in player_data:
                continue
            
            df = pd.DataFrame(player_data['score_history'])
            if not df.empty and 'category' in df.columns:
                all_categories.extend(df['category'].tolist())
        
        if not all_categories:
            return ""
        
        # Count categories
        category_counts = pd.Series(all_categories).value_counts()
        
        # Create bar chart
        plt.figure(figsize=(10, 6))
        bars = plt.bar(range(len(category_counts)), category_counts.values,
                      color=self.colors[:len(category_counts)])
        
        plt.title('Scoring Category Frequency', fontsize=14)
        plt.xlabel('Category', fontsize=12)
        plt.ylabel('Frequency', fontsize=12)
        plt.xticks(range(len(category_counts)), 
                  category_counts.index, rotation=45, ha='right')
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{int(height)}', ha='center', va='bottom')
        
        plt.tight_layout()
        
        # Save chart
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"categories_{timestamp}.png"
        filepath = os.path.join(self.output_dir, filename)
        
        plt.savefig(filepath, dpi=150)
        plt.close()
        
        return filepath
    
    def create_summary_table(self, players_data: List[Dict]) -> str:
        """
        Create a summary statistics table
        
        Returns:
            Path to saved text file with statistics
        """
        summary_lines = []
        summary_lines.append("=" * 60)
        summary_lines.append("GAME STATISTICS SUMMARY")
        summary_lines.append("=" * 60)
        summary_lines.append("")
        
        for player_data in players_data:
            if 'score_history' not in player_data:
                continue
            
            df = pd.DataFrame(player_data['score_history'])
            if df.empty:
                continue
            
            player_name = player_data.get('name', 'Unknown Player')
            
            summary_lines.append(f"Player: {player_name}")
            summary_lines.append("-" * 40)
            
            if 'score' in df.columns:
                summary_lines.append(f"  Total Score: {df['score'].sum():.0f}")
                summary_lines.append(f"  Average Score: {df['score'].mean():.2f}")
                summary_lines.append(f"  Best Score: {df['score'].max():.0f}")
                summary_lines.append(f"  Worst Score: {df['score'].min():.0f}")
                summary_lines.append(f"  Score Std Dev: {df['score'].std():.2f}")
            
            if 'category' in df.columns:
                most_common = df['category'].mode()
                if not most_common.empty:
                    summary_lines.append(f"  Most Common Category: {most_common.iloc[0]}")
            
            summary_lines.append(f"  Rounds Played: {len(df)}")
            summary_lines.append("")
        
        # Save to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"summary_{timestamp}.txt"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(summary_lines))
        
        return filepath