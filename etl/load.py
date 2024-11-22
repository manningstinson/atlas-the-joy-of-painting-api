import psycopg2
from psycopg2.extras import execute_values

def load_table(conn, df, table_name, columns):
    cursor = conn.cursor()
    # Convert numpy types to Python native types
    values = [tuple(x.item() if hasattr(x, 'item') else x for x in row) 
             for row in df[columns].values]
    
    query = f"""
        INSERT INTO {table_name} ({','.join(columns)})
        VALUES %s
        ON CONFLICT DO NOTHING
    """
    
    execute_values(cursor, query, values)
    conn.commit()
    cursor.close()

def load(episodes_df, colors_df, subjects_df, episode_colors_df, episode_subjects_df, db_config):
    conn = psycopg2.connect(**db_config)
    
    try:
        # Load main tables
        load_table(conn, episodes_df, 'episodes', 
                  ['title', 'air_date', 'broadcast_month', 'season', 'episode_number'])
        
        load_table(conn, colors_df, 'colors', 
                  ['name', 'code'])
        
        load_table(conn, subjects_df, 'subjects',
                  ['name'])
        
        # Load junction tables
        load_table(conn, episode_colors_df, 'episode_colors',
                  ['episode_id', 'color_id'])
        
        load_table(conn, episode_subjects_df, 'episode_subjects',
                  ['episode_id', 'subject_id'])
        
        print("✅ All data loaded successfully!")
        
    except Exception as e:
        print(f"❌ Error loading data: {str(e)}")
        raise
    finally:
        conn.close()