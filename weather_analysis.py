import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
data = pd.read_csv("data/sa_weather.csv")

# --- Data Cleaning ---
data['Date'] = pd.to_datetime(data['Date'])  # Convert Date to datetime
data['Temperature_C'] = pd.to_numeric(data['Temperature_C'], errors='coerce')  # Ensure numeric
data = data.dropna()  # Remove rows with missing values

# --- Summary Stats ---
print("First 5 rows:")
print(data.head())
print("\nMissing values per column:")
print(data.isnull().sum())
print("\nSummary Statistics:")
print(data.describe())

# --- Average Temperature by City ---
city_avg_temp = data.groupby('City')['Temperature_C'].mean().sort_values(ascending=False)
print("\nAverage Temperature by City:")
print(city_avg_temp)

# --- Average Temperature Over Time ---
date_avg_temp = data.groupby('Date')['Temperature_C'].mean()
print("\nAverage Temperature by Date:")
print(date_avg_temp)

# --- Plot: Average Temperature by City ---
plt.figure(figsize=(10,6))
bars = plt.bar(city_avg_temp.index, city_avg_temp.values, color='orange')
plt.title('Average Temperature by City', fontsize=16)
plt.ylabel('Temperature (°C)')
plt.xlabel('City')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Highlight hottest & coldest
bars[0].set_color('red')       # hottest city
bars[-1].set_color('blue')     # coldest city

plt.tight_layout()
plt.savefig('images/city_avg_temp.png')
plt.show()

# --- Plot: Average Temperature Over Time ---
plt.figure(figsize=(12,6))
plt.plot(date_avg_temp.index, date_avg_temp.values, color='orange', linewidth=2)
plt.title('Average Temperature Over Time', fontsize=16)
plt.ylabel('Temperature (°C)')
plt.xlabel('Date')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('images/date_avg_temp.png')
plt.show()


# --- Seasonal Analysis ---

# Add Month and Year columns
data['Month'] = data['Date'].dt.month
data['Year'] = data['Date'].dt.year

# Average temperature by month (all years combined)
monthly_avg = data.groupby('Month')['Temperature_C'].mean()
print("\nAverage Temperature by Month:")
print(monthly_avg)

# Plot: Average Temperature by Month
plt.figure(figsize=(10,6))
plt.plot(monthly_avg.index, monthly_avg.values, marker='o', color='orange', linewidth=2)
plt.title('Average Temperature by Month', fontsize=16)
plt.xlabel('Month')
plt.ylabel('Temperature (°C)')
plt.xticks(range(1,13))
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('images/monthly_avg_temp.png')
plt.show()

# Top 5 hottest cities overall
top_cities = city_avg_temp.head(5)
print("\nTop 5 Hottest Cities:")
print(top_cities)

# Bottom 5 coldest cities overall
bottom_cities = city_avg_temp.tail(5)
print("\nTop 5 Coldest Cities:")
print(bottom_cities)

# Plot: Top 5 Hottest Cities
plt.figure(figsize=(8,5))
plt.bar(top_cities.index, top_cities.values, color='red')
plt.title('Top 5 Hottest Cities', fontsize=16)
plt.ylabel('Temperature (°C)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('images/top_5_hottest.png')
plt.show()

# Plot: Top 5 Coldest Cities
plt.figure(figsize=(8,5))
plt.bar(bottom_cities.index, bottom_cities.values, color='blue')
plt.title('Top 5 Coldest Cities', fontsize=16)
plt.ylabel('Temperature (°C)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('images/top_5_coldest.png')
plt.show()
