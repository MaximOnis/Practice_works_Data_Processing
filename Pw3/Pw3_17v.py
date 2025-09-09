import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.covariance import EllipticEnvelope
from sklearn.metrics import classification_report

# Генерація випадкових фінансових транзакцій (часовий ряд)
# Генерація завжди однакових даних
np.random.seed(42)
# Створюємо масив з послідовних дат х кроком в 1 день на 200 днів
dates = pd.date_range(start="2023-01-01", periods=200)
# генеруємо дані про витрати щодня методом нормального розподілу
normal_values = np.random.normal(loc=1000, scale=50, size=200)

# Додаємо аномалії вручну в деякі точки
# Вибираємо 10 випадкових індексів
anomalies_indices = np.random.choice(range(200), size=10, replace=False)
# Копіюємо набір даних без аномалій
values_with_anomalies = normal_values.copy()
# Генеруємо додаткові витрати та додаємо до попередньо згенерованих значень, у випадкового вибраних індексах
values_with_anomalies[anomalies_indices] += np.random.normal(loc=500, scale=100, size=10)

# Створюємо DataFrame яких містить дату транзакції та її суму
df = pd.DataFrame({
    "Date": dates,
    "TransactionValue": values_with_anomalies
})
# Дата буде індексом
df.set_index("Date", inplace=True)

# Додаємо ground truth мітки (1 — нормально, -1 — аномалія)
true_labels = np.ones(200)
true_labels[anomalies_indices] = -1

# Виявлення аномалій за допомогою Isolation Forest
model = IsolationForest(contamination=0.06, random_state=42)
df['Anomaly'] = model.fit_predict(df[['TransactionValue']])

# Вивести лише аномалії
anomalies = df[df['Anomaly'] == -1]
print(anomalies)

# Оцінка точності
report = classification_report(true_labels, df['Anomaly'], target_names=["Normal", "Anomaly"], output_dict=True)
print(report)

# Побудова графіка
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['TransactionValue'], label='Transaction Value')
plt.scatter(df.index[df['Anomaly'] == -1], df['TransactionValue'][df['Anomaly'] == -1], color='red', label='Detected Anomaly')
plt.title("Фінансові транзакції з виявленими аномаліями")
plt.xlabel("Дата")
plt.ylabel("Сума транзакції")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
