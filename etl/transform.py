import pandas as pd

def transform_episodes(episodes_df):
    # Add season and episode numbers based on chronological order
    episodes_df = episodes_df.sort_values('air_date')
    episodes_df['episode_number'] = range(1, len(episodes_df) + 1)
    episodes_df['season'] = ((episodes_df['episode_number'] - 1) // 13) + 1
    episodes_df['episode_number'] = ((episodes_df['episode_number'] - 1) % 13) + 1
    return episodes_df

def transform_colors(colors_df):
    # Extract unique colors and their codes
    color_columns = [col for col in colors_df.columns if '_' in col]
    colors = []
    for col in color_columns:
        name = col.replace('_', ' ')
        # You'd want to add actual color codes here
        colors.append({'name': name, 'code': None})
    return pd.DataFrame(colors)

def transform_subjects(subjects_df):
    # Get unique subjects from boolean columns
    subject_columns = [col for col in subjects_df.columns if col not in ['EPISODE', 'TITLE']]
    subjects = [{'name': col.lower().replace('_', ' ')} for col in subject_columns]
    return pd.DataFrame(subjects)

def create_junction_tables(episodes_df, colors_df, subjects_df, colors_raw, subjects_raw):
    episode_colors = []
    episode_subjects = []
    
    # Create episode-color relationships
    for idx, row in colors_raw.iterrows():
        episode_id = idx + 1
        color_columns = [col for col in colors_raw.columns if '_' in col]
        for col in color_columns:
            if row[col]:
                color_id = colors_df[colors_df['name'] == col.replace('_', ' ')].index[0] + 1
                episode_colors.append({'episode_id': episode_id, 'color_id': color_id})
    
    # Create episode-subject relationships
    for idx, row in subjects_raw.iterrows():
        episode_id = idx + 1
        subject_columns = [col for col in subjects_raw.columns if col not in ['EPISODE', 'TITLE']]
        for col in subject_columns:
            if row[col]:
                subject_id = subjects_df[subjects_df['name'] == col.lower().replace('_', ' ')].index[0] + 1
                episode_subjects.append({'episode_id': episode_id, 'subject_id': subject_id})
                
    return pd.DataFrame(episode_colors), pd.DataFrame(episode_subjects)

def transform(episodes_df, colors_df, subjects_df):
    episodes_transformed = transform_episodes(episodes_df)
    colors_transformed = transform_colors(colors_df)
    subjects_transformed = transform_subjects(subjects_df)
    
    episode_colors, episode_subjects = create_junction_tables(
        episodes_transformed, colors_transformed, subjects_transformed,
        colors_df, subjects_df
    )
    
    return (episodes_transformed, colors_transformed, subjects_transformed, 
            episode_colors, episode_subjects)