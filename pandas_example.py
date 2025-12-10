import pandas as pd

data = {
    'Name': ['Alice', 'Bob', 'charlie', 'David'],
    'Age': [24,27,22,32],
    'City': ['New York', 'Los Angeles', 'Chicago', 'Houston']
}

df = pd.DataFrame(data)


print("Original DataFrame:")
print(df)

print("People older than 25:")
print(df[df["Age"]>25])
