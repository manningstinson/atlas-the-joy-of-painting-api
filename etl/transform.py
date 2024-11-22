import pandas as pd

def transform_episodes(episodes_df):
    print("\nTransforming episodes...")
    episodes_df = episodes_df.sort_values('air_date')
    episodes_df['episode_number'] = range(1, len(episodes_df) + 1)
    episodes_df['season'] = ((episodes_df['episode_number'] - 1) // 13) + 1
    episodes_df['episode_number'] = ((episodes_df['episode_number'] - 1) % 13) + 1
    print(f"✓ Transformed {len(episodes_df)} episodes")
    print(f"Sample episodes:\n{episodes_df.head()}")
    return episodes_df

def transform_colors(colors_df):
    print("\nTransforming colors...")
    color_columns = [col for col in colors_df.columns if '_' in col]
    colors = []
    for col in color_columns:
        name = col.replace('_', ' ')
        colors.append({'name': name, 'code': None})
    colors_df = pd.DataFrame(colors)
    print(f"✓ Transformed {len(colors_df)} colors")
    print(f"Sample colors:\n{colors_df.head()}")
    return colors_df

def transform_subjects(subjects_df):
    print("\nTransforming subjects...")
    subject_columns = [col for col in subjects_df.columns if col not in ['EPISODE', 'TITLE']]
    subjects = [{'name': col.lower().replace('_', ' ')} for col in subject_columns]
    subjects_df = pd.DataFrame(subjects)
    print(f"✓ Transformed {len(subjects_df)} subjects")
    print(f"Sample subjects:\n{subjects_df.head()}")
    return subjects_df

def create_junction_tables(episodes_df, colors_df, subjects_df, colors_raw, subjects_raw):
    print("\nCreating junction tables...")
    episode_colors = []
    episode_subjects = []
    
    for idx, row in colors_raw.iterrows():
        episode_id = idx + 1
        color_columns = [col for col in colors_raw.columns if '_' in col]
        for col in color_columns:
            if row[col]:
                color_id = colors_df[colors_df['name'] == col.replace('_', ' ')].index[0] + 1
                episode_colors.append({'episode_id': episode_id, 'color_id': color_id})
    
    for idx, row in subjects_raw.iterrows():
        episode_id = idx + 1
        subject_columns = [col for col in subjects_raw.columns if col not in ['EPISODE', 'TITLE']]
        for col in subject_columns:
            if row[col]:
                subject_id = subjects_df[subjects_df['name'] == col.lower().replace('_', ' ')].index[0] + 1
                episode_subjects.append({'episode_id': episode_id, 'subject_id': subject_id})
    
    episode_colors_df = pd.DataFrame(episode_colors)
    episode_subjects_df = pd.DataFrame(episode_subjects)
    print(f"✓ Created {len(episode_colors_df)} episode-color relationships")
    print(f"✓ Created {len(episode_subjects_df)} episode-subject relationships")
    return episode_colors_df, episode_subjects_df

def transform(episodes_df, colors_df, subjects_df):
    print("\n=== Starting Transformations ===")
    episodes_transformed = transform_episodes(episodes_df)
    colors_transformed = transform_colors(colors_df)
    subjects_transformed = transform_subjects(subjects_df)
    
    episode_colors, episode_subjects = create_junction_tables(
        episodes_transformed, colors_transformed, subjects_transformed,
        colors_df, subjects_df
    )
    
    print("\n=== Transformation Complete ===")
    return (episodes_transformed, colors_transformed, subjects_transformed, 
            episode_colors, episode_subjects)