import requests
import pandas as pd
from sqlalchemy import create_engine
import psycopg2


url = 'https://restcountries.com/v3.1/all?fields=name,region,subregion,population,area'

response = requests.get(url)

# python does not work in jason so need to change to something else
data = response.json()

# Step 2. Transform
records = []  # creating empty list to store data

for country in data:
    records.append(
        {
            'name': country.get('name', {}).get('common'),
            'region': country.get('region'),
            'subregion': country.get('subregion'),
            'population': country.get('population'),
            'area': country.get('area')

        }
    )

# print(records)

df = pd.DataFrame(records)

# Step 3. Load Data to the database
# Load liabries required
# create the engine
# push df to postgreSQL database


engine = create_engine(
    'postgresql+psycopg2://country_user:country_pass@localhost:5434/countries_db')

df.to_sql('Countries', engine, index=False)
