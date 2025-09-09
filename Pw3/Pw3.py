from faker import Faker
import pandas as pd

fake = Faker('uk_UA')  # Українська локалізація

num_records = 20
consumer_types = ['Домогосподарство', 'Підприємство']

data = []

for _ in range(num_records):
    consumer_type = fake.random_element(elements=consumer_types)
    date = fake.date_between(start_date='-1y', end_date='today')
    
    # Споживання та генерація через Faker.random_int() з різними діапазонами для типів
    if consumer_type == 'Домогосподарство':
        consumption = fake.random_int(min=10, max=60)
        generation = fake.random_int(min=0, max=15)
    else:  # Підприємство
        consumption = fake.random_int(min=300, max=800)
        generation = fake.random_int(min=0, max=250)
    
    data.append({
        'Date': date,
        'ConsumerType': consumer_type,
        'Consumption_kWh': consumption,
        'Generation_kWh': generation,
    })

df = pd.DataFrame(data)
df.sort_values(by='Date', inplace=True)

print(df.to_string(index=False))
