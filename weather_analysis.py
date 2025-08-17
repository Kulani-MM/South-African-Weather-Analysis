import pandas as pd
import matplotlib.pyplot as plt

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

# Summary statistics
print("Summary Statistics:")
print(data.describe())

# Group by city and calculate average temperature
city_avg_temp = data.groupby('City')['Temperature_C'].mean()
print("\nAverage Temperature by City:")
print(city_avg_temp)

# Group by date and calculate average temperature
date_avg_temp = data.groupby('Date')['Temperature_C'].mean()
print("\nAverage Temperature by Date:")
print(date_avg_temp)

# Plot average temperature by city
city_avg_temp.plot(kind='bar', title='Average Temperature by City')
plt.ylabel('Temperature (°C)')
plt.xlabel('City')
plt.tight_layout()
plt.savefig('images/city_avg_temp.png')
plt.show()

# Plot average temperature over time
date_avg_temp.plot(kind='line', title='Average Temperature Over Time')
plt.ylabel('Temperature (°C)')
plt.xlabel('Date')
plt.tight_layout()
plt.savefig('images/date_avg_temp.png')
plt.show()
