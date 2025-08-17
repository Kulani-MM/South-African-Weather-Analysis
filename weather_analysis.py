import pandas as pd

# Load the dataset
data = pd.read_csv("data/sa_weather.csv")

# Show the first 5 rows
print("First 5 rows of the dataset:")
print(data.head())

# Check for missing values
print("\nMissing values per column:")
print(data.isnull().sum())
