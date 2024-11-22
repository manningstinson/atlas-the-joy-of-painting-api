from extract import extract
from transform import transform
from load import load
import os
from dotenv import load_dotenv

def run_etl():
    print("=== Starting ETL Process ===")
    
    # Load environment variables
    load_dotenv()
    
    db_config = {
        'dbname': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'port': 25060,
        'sslmode': 'verify-full',
        'sslrootcert': '../ca-certificate.crt'  # Updated path
    }
    
    try:
        # Extract
        print("\nExtracting data...")
        episodes_df, colors_df, subjects_df = extract()
        
        # Transform
        print("\nTransforming data...")
        (episodes_transformed, colors_transformed, subjects_transformed,
         episode_colors, episode_subjects) = transform(episodes_df, colors_df, subjects_df)
        
        # Load
        print("\nLoading data...")
        load(episodes_transformed, colors_transformed, subjects_transformed,
             episode_colors, episode_subjects, db_config)
        
        print("\n=== ETL Process Complete ===")
        
    except Exception as e:
        print(f"\n❌ ETL process failed!")
        print(f"Error: {str(e)}")
        raise

if __name__ == "__main__":
    run_etl()