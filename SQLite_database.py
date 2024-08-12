from sqlalchemy import create_engine

# Create SQLite engine
engine = create_engine('sqlite:///hotel_data.db')

# Connect to the engine and create the database and connect
with engine.connect() as connection:
    pass  # The database will be created automatically if it doesn't exist
