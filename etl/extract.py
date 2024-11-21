import pandas as pd
from datetime import datetime

def extract_episodes():
    df = pd.read_csv('data/raw/joy-of-painting-episdode-dates.csv', header=None, names=['raw_data'])
    
    # Parse episode data
    episodes = []
    for _, row in df.iterrows():
        # Extract title and date from format: "Title" (Date)
        parts = row['raw_data'].split('(')
        title = parts[0].strip().strip('"')
        date_str = parts[1].strip(')')
        date = datetime.strptime(date_str, '%B %d, %Y')
        
        episodes.append({
            'title': title,
            'air_date': date.date(),
            'broadcast_month': date.month,
            'season': None,  # Will be added in transform step
            'episode_number': None  # Will be added in transform step
        })
    
    return pd.DataFrame(episodes)

def extract_colors():
    df = pd.read_csv('data/raw/joy-of-painting-colors-used.csv')
    return df

def extract_subjects():
    df = pd.read_csv('data/raw/joy-of-painting-subject-matter.csv')
    return df

def extract():
    episodes_df = extract_episodes()
    colors_df = extract_colors()
    subjects_df = extract_subjects()
    
    return episodes_df, colors_df, subjects_df