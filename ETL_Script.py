import pandas as pd
from sqlalchemy import create_engine
import os

# Create SQLite engine
engine = create_engine('sqlite:///hotel_data.db')

# Ensure the summary folder exists
summary_folder = 'summary'
os.makedirs(summary_folder, exist_ok=True)

# Revenue and Occupancy by Room Type
room_summary_query = """
SELECT
    r.STAY_DATE,
    p.REPORT_NAME AS PROPERTY,
    r.ROOM_CATEGORY,
    COUNT(r.RESERVATION_ID) AS Rooms_Sold,
    SUM(r.ROOM_RATE) AS Room_Revenue,
    (COUNT(r.RESERVATION_ID) * 1.0 / pi.INVENTORY) * 100 AS Occupancy_Percentage
FROM
    reservations r
JOIN
    property_inventory pi ON r.PROPERTY_CODE = pi.PROPERTY_CODE AND r.STAY_DATE = pi.BUSINESS_DATE
JOIN
    dim_property p ON r.PROPERTY_CODE = p.PROPERTY_CODE
GROUP BY
    r.STAY_DATE, p.REPORT_NAME, r.ROOM_CATEGORY;
"""

# Ancillary Revenue
ancillary_summary_query = """
SELECT
    DATE(a.CHECK_DATETIME) AS Date,
    p.REPORT_NAME AS Property,
    rc.LOB,
    SUM(a.CHECK_TOTAL) AS Total_Revenue,
    (SUM(a.CHECK_TOTAL) / COUNT(DISTINCT a.CHECK_ID)) AS RevPOR,
    (SUM(a.CHECK_TOTAL) / pi.INVENTORY) AS RevPAR
FROM
    ancillary_data a
JOIN
    dim_property p ON a.LOCATION_ID = p.POS_PROPERTY_CODE
JOIN
    dim_revenue_center rc ON a.REVENUECENTER_ID = rc.CODE
JOIN
    property_inventory pi ON p.PROPERTY_CODE = pi.PROPERTY_CODE AND DATE(a.CHECK_DATETIME) = pi.BUSINESS_DATE
GROUP BY
    Date, Property, LOB;

"""

# Execute queries and load results into DataFrames
room_summary_df = pd.read_sql(room_summary_query, engine)
print(room_summary_df)
ancillary_summary_df = pd.read_sql(ancillary_summary_query, engine)
print(ancillary_summary_df)

# Save the results to CSV files in the summary folder
room_summary_df.to_csv(f'{summary_folder}/room_summary.csv', index=False)
ancillary_summary_df.to_csv(f'{summary_folder}/ancillary_summary.csv', index=False)
