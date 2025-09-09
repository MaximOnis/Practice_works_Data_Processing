import pandas as pd
# Тестовий набір даних
data = {
    "1": [1, 4, -3, 5, 3, 8, 8, 3],
    "2": [6, 3, 7, 3, 4, 5, 3, 5],
    "3": [9, 4, 3, 7, 4, 2, 0, 1]
}
df = pd.DataFrame(data)

# Нормалізація колонки
def scale_column(column: pd.Series):
    max_val = column.max()
    min_val = column.min()
    diff = max_val - min_val
    if diff == 0:
        return column.apply(lambda x: 0)
    result = (column - min_val) / diff
    return result


# Глобальна нормалізація Dataframe
def scale(inp: pd.DataFrame):
    max_val = inp.max().max()
    min_val = inp.min().min()
    diff = max_val - min_val
    if diff == 0:
        return inp.apply(lambda x: x.apply(lambda y: 0))
    result = (inp - min_val) / diff
    return result


# Нормалізація першої колонки
print(scale_column(df["1"]))

# Глобальна нормалізація всіх колонок
print(scale(df))

# Нормалізація всіх колонок
x = df.apply(scale_column)
print(x)
