import pandas as pd
import math
from db_utils import execute_sql

data = pd.read_csv("epi_r.csv", usecols=['title', 'calories', 'protein', 'fat'])
df = pd.DataFrame(data)

"""
COUNT CARBS AND ADD TO NEW COLUMN
"""
df2 = df.assign(carbs=lambda x: (x.calories - x.protein * 4 - x.fat * 9) / 4)

if __name__ == "__main__":
    execute_sql('''
        CREATE TABLE IF NOT EXISTS recipies(
            id SERIAL PRIMARY KEY,
            title varchar(200) UNIQUE,
            calories DOUBLE PRECISION NOT NULL,
            protein DOUBLE PRECISION NOT NULL,
            fat DOUBLE PRECISION NOT NULL,
            carbs DOUBLE PRECISION NOT NULL
        )
        ''')

    for row in df2.itertuples():
        if math.isnan(row.calories) or math.isnan(row.protein) or math.isnan(row.fat) or math.isnan(row.carbs):
            continue
        elif row.calories in range(0, 400) or row.calories > 1500:
            continue
        else:
            execute_sql('''
                INSERT INTO recipies(title, calories, protein, fat, carbs)
                    VALUES(%s, %s, %s, %s, %s) on conflict (title) do nothing;
                ''', row.title, row.calories, row.protein, row.fat, row.carbs)
