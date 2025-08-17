# sa_weather_dashboard.py

import requests
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# -----------------------------
# Step 1: Fetch Live Weather Data
# -----------------------------
API_KEY = "54f3a4b1646dd767f790a606911f1608"
CITIES = ["Johannesburg", "Cape Town", "Durban", "Pretoria", "Port Elizabeth"]

weather_list = []

for city in CITIES:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},ZA&units=metric&appid={API_KEY}"
    res = requests.get(url).json()
    
    # Make sure the response is valid
    if res.get("main"):
        weather_list.append({
            "City": city,
            "Temperature_C": res["main"]["temp"],
            "Humidity": res["main"]["humidity"],
            "Condition": res["weather"][0]["description"]
        })
    else:
        print(f"Failed to get data for {city}: {res.get('message')}")

# Convert to DataFrame
data = pd.DataFrame(weather_list)

# -----------------------------
# Step 2: Static Plots with Matplotlib
# -----------------------------
plt.figure(figsize=(8,5))
plt.bar(data['City'], data['Temperature_C'], color='orange')
plt.title("Current Temperature by City")
plt.ylabel("Temperature (°C)")
plt.xlabel("City")
plt.tight_layout()
plt.show()

plt.figure(figsize=(8,5))
plt.bar(data['City'], data['Humidity'], color='blue')
plt.title("Current Humidity by City")
plt.ylabel("Humidity (%)")
plt.xlabel("City")
plt.tight_layout()
plt.show()

# -----------------------------
# Step 3: Interactive Plots with Plotly
# -----------------------------
fig_temp = px.bar(
    data,
    x='City',
    y='Temperature_C',
    color='Temperature_C',
    color_continuous_scale='OrRd',
    title='Current Temperature by City'
)
fig_temp.show()

fig_humidity = px.bar(
    data,
    x='City',
    y='Humidity',
    color='Humidity',
    color_continuous_scale='Blues',
    title='Current Humidity by City'
)
fig_humidity.show()

# -----------------------------
# Step 4: Dash Web App
# -----------------------------
app = Dash(__name__)

app.layout = html.Div([
    html.H1("South African Live Weather Dashboard"),
    html.P("Select a city to see current temperature and humidity:"),
    
    dcc.Dropdown(
        id='city-dropdown',
        options=[{'label': city, 'value': city} for city in data['City']],
        value=data['City'][0]
    ),
    
    dcc.Graph(id='city-weather-graph')
])

@app.callback(
    Output('city-weather-graph', 'figure'),
    Input('city-dropdown', 'value')
)
def update_graph(selected_city):
    city_data = data[data['City'] == selected_city]
    
    fig = px.bar(
        city_data,
        x=['Temperature (°C)', 'Humidity (%)'],
        y=[city_data['Temperature_C'].values[0], city_data['Humidity'].values[0]],
        color=['Temperature (°C)', 'Humidity (%)'],
        color_discrete_map={'Temperature (°C)': 'orange', 'Humidity (%)': 'blue'},
        title=f"Weather in {selected_city}"
    )
    return fig

# -----------------------------
# Step 5: Run the App
# -----------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
