import psycopg2
from faker import Faker
import random

fake = Faker()
conn = psycopg2.connect(
    host="localhost", port= "5433", database="dot_operations", user="dot_admin", password="dot_password"
)
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS regions (
        region_id SERIAL PRIMARY KEY,
        region_name VARCHAR(50),
        state_code VARCHAR(2)
    );
    CREATE TABLE IF NOT EXISTS assets (
        asset_id SERIAL PRIMARY KEY,
        asset_type VARCHAR(50),
        region_id INT REFERENCES regions(region_id),
        install_date DATE,
        condition_rating INT
    );
    CREATE TABLE IF NOT EXISTS maintenance_logs (
        log_id SERIAL PRIMARY KEY,
        asset_id INT REFERENCES assets(asset_id),
        work_type VARCHAR(50),
        cost NUMERIC(10, 2),
        completed_at TIMESTAMP
    );
""")

regions = [('Northeast District', 'CT'), ('Mid-Atlantic District', 'NJ'), ('Southeast District', 'NC')]
cur.executemany("INSERT INTO regions (region_name, state_code) VALUES (%s, %s) ON CONFLICT DO NOTHING;", regions)

asset_types = ['Bridge', 'Highway Guardrail', 'Traffic Signal', 'Overpass', 'Culvert']
for _ in range(200):
    cur.execute(
        "INSERT INTO assets (asset_type, region_id, install_date, condition_rating) VALUES (%s, %s, %s, %s);",
        (random.choice(asset_types), random.randint(1, 3), fake.date_between(start_date='-20y', end_date='-1y'), random.randint(1, 10))
    )

work_types = ['Inspection', 'Paving', 'Structural Repair', 'Electrical Fix', 'Emergency Clearing']
for _ in range(5000):
    cur.execute(
        "INSERT INTO maintenance_logs (asset_id, work_type, cost, completed_at) VALUES (%s, %s, %s, %s);",
        (random.randint(1, 200), random.choice(work_types), round(random.uniform(500.0, 75000.0), 2), fake.date_time_between(start_date='-1y', end_date='now'))
    )

conn.commit()
cur.close()
conn.close()
print("DOT Legacy OLTP Database seeded successfully!")
