import pandas as pd

# Load the dataset
data = pd.read_csv("data/sa_weather.csv")

# Show the first 5 rows
print("First 5 rows of the dataset:")
print(data.head())

# Check for missing values
print("\nMissing values per column:")
print(data.isnull().sum())

# Convert 'Date' to datetime format
data['Date'] = pd.to_datetime(data['Date'])

# Remove rows with missing values
data = data.dropna()

# Ensure 'Temperature_C' is numeric
data['Temperature_C'] = pd.to_numeric(data['Temperature_C'], errors='coerce')

# Remove rows where 'Temperature_C' couldn't be converted
data = data.dropna(subset=['Temperature_C'])

print("Cleaned Data:")
print(data.head())
