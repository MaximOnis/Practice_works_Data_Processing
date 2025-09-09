import pandas as pd
import random

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import matplotlib.pyplot as plt

# Генерація синтетичних даних
def generate_data(n_samples=1000):
    data = []
    for _ in range(n_samples):
        age = random.randint(18, 70)
        income = round(random.uniform(10000, 100000), 2)
        educated = random.choice([0, 1])
        family_members = random.randint(1, 6)
        employment_status = random.choice(['працевлаштований', 'безробітний', 'студент', 'пенсіонер'])

        # Кодування employment_status як число
        employment_code = {'працевлаштований': 3, 'безробітний': 0, 'студент': 1, 'пенсіонер': 2}[employment_status]
        # Генерація класу (наприклад, чи отримає кредит)
        # Просте логічне правило для прикладу
        will_get_credit = 1 if ((income > 45000 and employment_status in ['працевлаштований'] and educated == 1 and family_members < 5) or (income > 70000 and employment_status in ['безробітний', 'пенсіонер'] and age < 70) or (income > 55000 and ((employment_status in ['студент']) or (employment_status in ['працевлаштований'] and educated == 0))) and age < 18) else 0

        data.append([age, income, educated, family_members, employment_code, will_get_credit])

    columns = ['Age', 'Income', 'Educated', 'FamilyMembers', 'EmploymentStatus', 'Credit_status']
    return pd.DataFrame(data, columns=columns)

# Створення датафрейму
df = generate_data()
df.to_csv('socioeconomic_data.csv', index=False, encoding='utf-8-sig', sep=';')

# Розділення на ознаки та ціль
X = df.drop('Credit_status', axis=1)
y = df['Credit_status']

# Розділення на тренувальну і тестову вибірки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Тренування Random Forest
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Прогнозування
y_pred = model.predict(X_test)

# Оцінка моделі
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# Важливість ознак
"""
feature_importances = pd.Series(model.feature_importances_, index=X.columns)
feature_importances.sort_values(ascending=False).plot(kind='bar', figsize=(8,5))
plt.title('Feature Importance')
plt.tight_layout()
plt.show()
"""

# Ввід даних користувачем для прогнозування
answer = int(input("Задати дані?(Так - 1/Ні - 0):"))

while answer == 1:
    data = []

    answer = int(input('Введіть вік(0 - 80):'))
    data.append(answer)
    
    answer = int(input('Введіть дохід за місяць(0 - 100000):'))
    data.append(answer)
    
    answer = int(input('Має вищу освіту?(Так - 1/Ні - 0):'))
    data.append(answer)

    answer = int(input('Введіть кількість членів сім\'ї():'))
    data.append(answer)

    answer = input('Ваш статус(працевлаштований/безробітний/студент/пенсіонер):')
    employment_code = {'працевлаштований': 3, 'безробітний': 0, 'студент': 1, 'пенсіонер': 2}[answer]
    data.append(employment_code)

    print(data)
    columns = ['Age', 'Income', 'Educated', 'FamilyMembers', 'EmploymentStatus']

    user_data = pd.DataFrame([data], columns=columns)
    result = model.predict(user_data)
    if result == 1:
        print("Кредит Одобрено!")
    elif result == 0:
        print("В кредиті відмовлено!")
    answer = int(input("Ще раз?:"))

