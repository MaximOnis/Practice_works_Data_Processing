from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from faker import Faker

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

# === Передумова: у тебе вже є df зі стовпцями:
# ['Date', 'ConsumerType', 'Consumption_kWh', 'Generation_kWh']

# Кодуємо тип споживача
df['ConsumerTypeEncoded'] = df['ConsumerType'].map({'Домогосподарство': 0, 'Підприємство': 1})

# Вибираємо ознаки для PCA
features = ['Consumption_kWh', 'Generation_kWh', 'ConsumerTypeEncoded']
X = df[features]

# Стандартизуємо
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# PCA до 2 компонент
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# Друк варіацій
print("Відсоток поясненої дисперсії кожною компонентою:")
print(pca.explained_variance_ratio_)

# Друк ваг компонент
print("\nВаги ознак у кожній головній компоненті:")
pca_components = pd.DataFrame(pca.components_, columns=features, index=['PC1', 'PC2'])
print(pca_components)

# Візуалізація PCA
plt.figure(figsize=(8,6))
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=df['ConsumerTypeEncoded'], cmap='viridis', alpha=0.7)
plt.xlabel('Головна компонента 1')
plt.ylabel('Головна компонента 2')
plt.title('PCA: Головні компоненти')
plt.colorbar(label='Тип споживача (0=домогосп., 1=підпр.)')
plt.grid(True)
plt.tight_layout()
plt.show()

# Кореляційна матриця
correlation_matrix = df[features].corr()

plt.figure(figsize=(6,5))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Кореляційна матриця")
plt.tight_layout()
plt.show()
