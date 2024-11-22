import pandas as pd
from datetime import datetime
import os

def extract_episodes():
   print("Extracting episodes data...")
   try:
       with open('../data/raw/joy-of-painting-episdode-dates.csv', 'r') as file:
           lines = file.readlines()
       
       print(f"✅ Successfully loaded episodes file. Found {len(lines)} episodes.")
       
       episodes = []
       for line in lines:
           try:
               title_part = line.split('(')[0].strip().strip('"')
               date_part = line.split('(')[1].split(')')[0].strip()
               date = datetime.strptime(date_part, '%B %d, %Y')
               
               episodes.append({
                   'title': title_part,
                   'air_date': date.date(),
                   'broadcast_month': date.month,
                   'season': None,
                   'episode_number': None
               })
               
           except Exception as e:
               print(f"❌ Error processing line: {line.strip()}")
               print(f"Error: {str(e)}")
       
       episodes_df = pd.DataFrame(episodes)
       print(f"✅ Successfully processed {len(episodes_df)} episodes")
       print("\nFirst few episodes:")
       print(episodes_df.head())
       return episodes_df
   
   except Exception as e:
       print("❌ Failed to extract episodes data!")
       print(f"Error: {str(e)}")
       raise

def extract_colors():
   print("Extracting colors data...")
   try:
       df = pd.read_csv('../data/raw/joy-of-painting-colors-used.csv')
       print(f"✅ Successfully loaded colors file. Found {len(df)} rows and {len(df.columns)} colors.")
       return df
   except Exception as e:
       print("❌ Failed to extract colors data!")
       print(f"Error: {str(e)}")
       raise

def extract_subjects():
   print("Extracting subjects data...")
   try:
       df = pd.read_csv('../data/raw/joy-of-painting-subject-matter.csv')
       print(f"✅ Successfully loaded subjects file. Found {len(df)} rows and {len(df.columns)} columns.")
       return df
   except Exception as e:
       print("❌ Failed to extract subjects data!")
       print(f"Error: {str(e)}")
       raise

def extract():
   print("\n=== Starting Data Extraction ===\n")
   
   episodes_df, colors_df, subjects_df = None, None, None
   
   try:
       episodes_df = extract_episodes()
       print("\nEpisodes Preview:")
       print(episodes_df.head())
       print("\nEpisodes Info:")
       print(episodes_df.info())
       
       colors_df = extract_colors()
       print("\nColors Preview:")
       print(colors_df.head())
       print("\nColors Info:")
       print(colors_df.info())
       
       subjects_df = extract_subjects()
       print("\nSubjects Preview:")
       print(subjects_df.head())
       print("\nSubjects Info:")
       print(subjects_df.info())
       
       print("\n✅ All data extracted successfully!")
       return episodes_df, colors_df, subjects_df
   
   except Exception as e:
       print("\n❌ Extract process failed!")
       print(f"Error: {str(e)}")
       raise

if __name__ == "__main__":
   extract()