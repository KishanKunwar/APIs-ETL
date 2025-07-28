# peginated post(not get) requests

import requests
import pandas as pd
from sqlalchemy import create_engine
import psycopg2


url = 'https://api.spacexdata.com/v4/launches/query'

headers = {'Content-Type': 'application/json'}
# content type examples
# text/plain
# multipart/form-data
# application/x-www-form-urlencoded


payload = {
    'query': {},  # empty filter - meaning want all the data
    'options': {'limit': 100, 'page': 1}  # says start with page 1
}

all_launches = []

while True:  # its says hit api one page at once until all the pages is done
    res = requests.post(url, json=payload, headers=headers)
    output = res.json()

    docs = output.get("docs", [])

    for doc in docs:
        all_launches.append(
            {
                'name': doc.get('name'),
                'data_utc': doc.get('data_utc'),
                'success': doc.get('success'),
                'details': doc.get('details'),
                'rocket': doc.get('rocket', {})
            }
        )

    if not output.get('hasNextPage', False):
        break

    payload['options']['page'] += 1

# convert all_launches to a Dataframe

df = pd.DataFrame(all_launches)

# push it to the postgreSQL Database

engine = create_engine(
    'postgresql+psycopg2://country_user:country_pass@localhost:5434/countries_db'
)

df.to_sql('SpaceX', engine, index=False, if_exists='replace')


try:
    conn = psycopg2.connect(
        dbname='countries_db',
        user='country_user',
        password='country_pass',
        host='localhost',
        port='5434'
    )
    print("Connected successfully!")
except Exception as e:
    print(f"Connection failed: {e}")
