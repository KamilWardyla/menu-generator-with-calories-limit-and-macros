import pandas as pd
import math
from main import execute_sql

data = pd.read_csv("epi_r.csv", usecols=['title', 'calories', 'protein', 'fat'])
df = pd.DataFrame(data)

"""
COUNT CARBON AND ADD TO NEW COLUMN
"""

df2 = df.assign(carbon=lambda x: (x.calories - x.protein * 4 - x.fat * 9) / 4)

if __name__ == "__main__":
    execute_sql('''
        CREATE TABLE IF NOT EXISTS recipies(
            id SERIAL PRIMARY KEY,
            title varchar(200) UNIQUE,
            calories DOUBLE PRECISION NOT NULL,
            protein DOUBLE PRECISION NOT NULL,
            fat DOUBLE PRECISION NOT NULL,
            carbon DOUBLE PRECISION NOT NULL
        )
        ''')

    for row in df2.itertuples():
        if math.isnan(row.calories) or math.isnan(row.protein) or math.isnan(row.fat) or math.isnan(row.carbon):
            continue
        else:
            execute_sql('''
                INSERT INTO recipies(title, calories, protein, fat, carbon)
                    VALUES(%s, %s, %s, %s, %s) on conflict (title) do nothing;
                ''', row.title, row.calories, row.protein, row.fat, row.carbon)