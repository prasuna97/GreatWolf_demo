from sqlalchemy import create_engine, text

# Create SQLite engine
engine = create_engine('sqlite:///hotel_data.db')

# SQL commands to create the tables
create_tables = [
    """
    CREATE TABLE IF NOT EXISTS dim_property (
        PROPERTY_ID INT PRIMARY KEY,
        REPORT_NAME VARCHAR(255),
        PROPERTY_CODE VARCHAR(255),
        POS_PROPERTY_CODE INT,
        OPEN_DATE DATE,
        ADDRESS VARCHAR(255),
        CITY VARCHAR(255),
        STATE VARCHAR(50),
        ZIP VARCHAR(10),
        LATITUDE DECIMAL(10, 6),
        LONGITUDE DECIMAL(10, 6)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS property_inventory (
        INVENTORY_ID INT PRIMARY KEY,
        BUSINESS_DATE DATE,
        PROPERTY_CODE VARCHAR(255),
        PROPERTY_NAME VARCHAR(255),
        INVENTORY INT
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS reservations (
        RESERVATION_ID INT PRIMARY KEY,
        CUSTOMER_ID INT,
        BOOKING_DATE DATE,
        STAY_DATE DATE,
        PROPERTY_CODE VARCHAR(255),
        ROOM_CATEGORY VARCHAR(255),
        ROOM_RATE DECIMAL(10, 2)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS dim_revenue_center (
        CODE INT PRIMARY KEY,
        LOC_OUTLET_NAME VARCHAR(255),
        OUTLET_NAME VARCHAR(255),
        LOB_SEGMENT VARCHAR(255),
        LOB VARCHAR(255)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS ancillary_data (
        CHECK_ID INT PRIMARY KEY,
        CHECK_DATETIME DATETIME,
        LOCATION_ID INT,
        REVENUECENTER_ID INT,
        CHECK_TOTAL DECIMAL(10, 2),
        FOREIGN KEY (LOCATION_ID) REFERENCES dim_property(PROPERTY_ID),
        FOREIGN KEY (REVENUECENTER_ID) REFERENCES dim_revenue_center(CODE)
    );
    """
]

# Execute each table creation statement one by one
with engine.connect() as connection:
    for create_table in create_tables:
        connection.execute(text(create_table))
