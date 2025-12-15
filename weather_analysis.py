# sa_weather_dashboard.py

import os
import logging
import requests
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# -----------------------------
# Step 1: Fetch Live Weather Data
# -----------------------------
API_KEY = os.getenv("OPENWEATHER_API_KEY")
DEMO_MODE = not API_KEY

if DEMO_MODE:
    logger.warning("No API key found - running in DEMO MODE with sample data")
    logger.info("To use live data, set OPENWEATHER_API_KEY in your .env file")

    # Load sample data
    import json
    sample_data_path = os.path.join(os.path.dirname(__file__), 'sample_data.json')

    try:
        with open(sample_data_path, 'r') as f:
            weather_list = json.load(f)
        logger.info(f"Loaded sample data for {len(weather_list)} cities")
    except FileNotFoundError:
        logger.error("sample_data.json not found. Cannot run in demo mode.")
        raise ValueError("Please either set OPENWEATHER_API_KEY in .env or ensure sample_data.json exists")
else:
    logger.info("Running in LIVE MODE with OpenWeatherMap API")

    CITIES = [
        "Johannesburg", "Cape Town", "Durban", "Pretoria", "Port Elizabeth",
        "Bloemfontein", "East London", "Pietermaritzburg", "Nelspruit", "Kimberley",
        "Polokwane", "Rustenburg", "Middelburg", "George", "Richards Bay",
        "Vanderbijlpark", "Centurion", "Uitenhage", "Welkom", "Newcastle",
        "Vereeniging", "Krugersdorp", "Witbank", "Paarl", "Stellenbosch"
    ]
    REQUEST_TIMEOUT = 10

    weather_list = []

    for city in CITIES:
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city},ZA&units=metric&appid={API_KEY}"
            logger.info(f"Fetching weather data for {city}")
            res = requests.get(url, timeout=REQUEST_TIMEOUT)
            res.raise_for_status()
            data = res.json()

            # Make sure the response is valid
            if data.get("main") and data.get("weather"):
                weather_list.append({
                    "City": city,
                    "Temperature_C": data["main"]["temp"],
                    "Feels_Like_C": data["main"]["feels_like"],
                    "Humidity": data["main"]["humidity"],
                    "Pressure": data["main"]["pressure"],
                    "Wind_Speed": data["wind"].get("speed", 0),
                    "Condition": data["weather"][0]["description"].title()
                })
                logger.info(f"Successfully fetched data for {city}")
            else:
                logger.warning(f"Incomplete data received for {city}")
        except requests.exceptions.Timeout:
            logger.error(f"Timeout fetching data for {city}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get data for {city}: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error for {city}: {str(e)}")

# Convert to DataFrame
data = pd.DataFrame(weather_list)

# Validate that data
if data.empty:
    logger.error("No weather data retrieved. Cannot start dashboard.")
    raise ValueError("Failed to fetch weather data for any city. Please check your API key and internet connection.")

logger.info(f"Successfully loaded weather data for {len(data)} cities")

# -----------------------------
# Step 2: Static Plots with Matplotlib 
# -----------------------------
SAVE_STATIC_PLOTS = os.getenv("SAVE_STATIC_PLOTS", "false").lower() == "true"

if SAVE_STATIC_PLOTS:
    logger.info("Generating static plots...")

    plt.figure(figsize=(10, 6))
    plt.bar(data['City'], data['Temperature_C'], color='orange', alpha=0.7)
    plt.title("Current Temperature by City", fontsize=14, fontweight='bold')
    plt.ylabel("Temperature (°C)")
    plt.xlabel("City")
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('temperature_plot.png', dpi=300, bbox_inches='tight')
    logger.info("Saved temperature_plot.png")
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.bar(data['City'], data['Humidity'], color='blue', alpha=0.7)
    plt.title("Current Humidity by City", fontsize=14, fontweight='bold')
    plt.ylabel("Humidity (%)")
    plt.xlabel("City")
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('humidity_plot.png', dpi=300, bbox_inches='tight')
    logger.info("Saved humidity_plot.png")
    plt.close()

# -----------------------------
# Step 4: Dash Web App
# -----------------------------
app = Dash(__name__)

app.layout = html.Div([
    # Demo mode banner (only shown in demo mode)
    html.Div([
        html.Div([
            html.Span("ℹ️ DEMO MODE", style={'fontWeight': 'bold', 'marginRight': '10px'}),
            html.Span("Using sample data. "),
            html.A("Get a free API key", href="https://openweathermap.org/api",
                   target="_blank", style={'color': '#3498db', 'textDecoration': 'underline'}),
            html.Span(" to see live weather data.")
        ], style={
            'backgroundColor': '#fff3cd',
            'color': '#856404',
            'padding': '12px 20px',
            'borderRadius': '8px',
            'textAlign': 'center',
            'border': '1px solid #ffeaa7',
            'fontSize': '14px'
        })
    ], style={'marginBottom': '20px'}) if DEMO_MODE else html.Div(),

    html.Div([
        html.H1("South African Live Weather Dashboard",
                style={'textAlign': 'center', 'color': '#ffffff', 'marginBottom': '10px', 'fontSize': '42px', 'fontWeight': 'bold'}),
        html.P(f"{'Sample' if DEMO_MODE else 'Real-time'} weather data for {len(data)} South African cities",
               style={'textAlign': 'center', 'color': '#ecf0f1', 'fontSize': '18px'}),
    ], style={
        'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'padding': '30px',
        'borderRadius': '15px',
        'marginBottom': '30px',
        'boxShadow': '0 10px 30px rgba(0,0,0,0.2)'
    }),

    html.Div([
        html.Div([
            html.Div([
                html.H3("Hottest", style={'margin': '0', 'color': '#e74c3c', 'fontSize': '18px'}),
                html.H2(f"{data.loc[data['Temperature_C'].idxmax(), 'City']}",
                        style={'margin': '5px 0', 'fontSize': '24px', 'color': '#2c3e50'}),
                html.P(f"{data['Temperature_C'].max():.1f}°C",
                       style={'fontSize': '32px', 'fontWeight': 'bold', 'color': '#e74c3c', 'margin': '0'})
            ], style={
                'backgroundColor': '#fff',
                'padding': '20px',
                'borderRadius': '10px',
                'boxShadow': '0 4px 6px rgba(0,0,0,0.1)',
                'textAlign': 'center',
                'border': '3px solid #e74c3c'
            }),
        ], style={'flex': '1', 'margin': '0 10px'}),

        html.Div([
            html.Div([
                html.H3("Coolest", style={'margin': '0', 'color': '#3498db', 'fontSize': '18px'}),
                html.H2(f"{data.loc[data['Temperature_C'].idxmin(), 'City']}",
                        style={'margin': '5px 0', 'fontSize': '24px', 'color': '#2c3e50'}),
                html.P(f"{data['Temperature_C'].min():.1f}°C",
                       style={'fontSize': '32px', 'fontWeight': 'bold', 'color': '#3498db', 'margin': '0'})
            ], style={
                'backgroundColor': '#fff',
                'padding': '20px',
                'borderRadius': '10px',
                'boxShadow': '0 4px 6px rgba(0,0,0,0.1)',
                'textAlign': 'center',
                'border': '3px solid #3498db'
            }),
        ], style={'flex': '1', 'margin': '0 10px'}),

        html.Div([
            html.Div([
                html.H3("Most Humid", style={'margin': '0', 'color': '#1abc9c', 'fontSize': '18px'}),
                html.H2(f"{data.loc[data['Humidity'].idxmax(), 'City']}",
                        style={'margin': '5px 0', 'fontSize': '24px', 'color': '#2c3e50'}),
                html.P(f"{data['Humidity'].max():.0f}%",
                       style={'fontSize': '32px', 'fontWeight': 'bold', 'color': '#1abc9c', 'margin': '0'})
            ], style={
                'backgroundColor': '#fff',
                'padding': '20px',
                'borderRadius': '10px',
                'boxShadow': '0 4px 6px rgba(0,0,0,0.1)',
                'textAlign': 'center',
                'border': '3px solid #1abc9c'
            }),
        ], style={'flex': '1', 'margin': '0 10px'}),

        html.Div([
            html.Div([
                html.H3("Windiest", style={'margin': '0', 'color': '#95a5a6', 'fontSize': '18px'}),
                html.H2(f"{data.loc[data['Wind_Speed'].idxmax(), 'City']}",
                        style={'margin': '5px 0', 'fontSize': '24px', 'color': '#2c3e50'}),
                html.P(f"{data['Wind_Speed'].max():.1f} m/s",
                       style={'fontSize': '32px', 'fontWeight': 'bold', 'color': '#95a5a6', 'margin': '0'})
            ], style={
                'backgroundColor': '#fff',
                'padding': '20px',
                'borderRadius': '10px',
                'boxShadow': '0 4px 6px rgba(0,0,0,0.1)',
                'textAlign': 'center',
                'border': '3px solid #95a5a6'
            }),
        ], style={'flex': '1', 'margin': '0 10px'}),
    ], style={'display': 'flex', 'marginBottom': '30px', 'flexWrap': 'wrap'}),

    html.Div([
        dcc.Graph(
            id='all-cities-overview',
            figure=px.scatter(
                data,
                x='Temperature_C',
                y='Humidity',
                size='Wind_Speed',
                color='Temperature_C',
                hover_name='City',
                hover_data={
                    'Temperature_C': ':.1f',
                    'Humidity': ':.0f',
                    'Wind_Speed': ':.1f',
                    'Condition': True
                },
                labels={
                    'Temperature_C': 'Temperature (°C)',
                    'Humidity': 'Humidity (%)',
                    'Wind_Speed': 'Wind Speed (m/s)'
                },
                title='All Cities: Temperature vs Humidity (bubble size = wind speed)',
                color_continuous_scale='RdYlBu_r'
            ).update_layout(
                title_font_size=20,
                title_x=0.5,
                height=500,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
            )
        )
    ], style={'marginBottom': '30px'}),

    html.Div([
        html.H2("City Details", style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '20px'}),
        html.Label("Select a city:", style={'fontWeight': 'bold', 'fontSize': '16px', 'marginBottom': '10px'}),
        dcc.Dropdown(
            id='city-dropdown',
            options=[{'label': city, 'value': city} for city in sorted(data['City'])],
            value=data['City'].iloc[0],
            style={'marginBottom': '20px'}
        ),
    ], style={'maxWidth': '600px', 'margin': '0 auto', 'marginBottom': '30px'}),

    html.Div(id='weather-summary', style={'textAlign': 'center', 'marginBottom': '20px'}),

    dcc.Graph(id='city-weather-graph'),

    html.Div([
        html.P(f"Last updated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}",
               style={'textAlign': 'center', 'color': '#95a5a6', 'fontSize': '12px'})
    ])
], style={
    'maxWidth': '1400px',
    'margin': '0 auto',
    'padding': '20px',
    'fontFamily': 'Arial, sans-serif',
    'backgroundColor': '#f5f7fa',
    'minHeight': '100vh'
})

@app.callback(
    [Output('city-weather-graph', 'figure'),
     Output('weather-summary', 'children')],
    Input('city-dropdown', 'value')
)
def update_graph(selected_city):
    city_data = data[data['City'] == selected_city].iloc[0]

    # Create weather summary
    summary = html.Div([
        html.H3(f"{selected_city}", style={'margin': '0', 'color': '#2c3e50'}),
        html.P(f"Condition: {city_data['Condition']}",
               style={'fontSize': '18px', 'color': '#34495e', 'margin': '5px 0'}),
        html.P(f"Temperature: {city_data['Temperature_C']:.1f}°C (Feels like: {city_data['Feels_Like_C']:.1f}°C)",
               style={'fontSize': '16px', 'color': '#7f8c8d', 'margin': '5px 0'})
    ])

    # Prepare data for visualization
    metrics_data = pd.DataFrame({
        'Metric': ['Temperature (°C)', 'Feels Like (°C)', 'Humidity (%)', 'Pressure (hPa)', 'Wind Speed (m/s)'],
        'Value': [
            city_data['Temperature_C'],
            city_data['Feels_Like_C'],
            city_data['Humidity'],
            city_data['Pressure'],
            city_data['Wind_Speed']
        ],
        'Category': ['Temperature', 'Temperature', 'Humidity', 'Pressure', 'Wind']
    })

    fig = px.bar(
        metrics_data,
        x='Metric',
        y='Value',
        color='Category',
        color_discrete_map={
            'Temperature': '#e74c3c',
            'Humidity': '#3498db',
            'Pressure': '#9b59b6',
            'Wind': '#1abc9c'
        },
        title=f"Weather Metrics for {selected_city}",
        labels={'Value': 'Measurement'}
    )

    fig.update_layout(
        showlegend=False,
        title_font_size=18,
        title_x=0.5,
        xaxis_title="",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )

    fig.update_traces(marker_line_color='rgb(8,48,107)', marker_line_width=1.5, opacity=0.8)

    return fig, summary

# -----------------------------
# Step 5: Run the App
# -----------------------------
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8050))
    debug_mode = os.getenv("DEBUG", "false").lower() == "true"

    logger.info(f"Starting dashboard on http://0.0.0.0:{port}")
    logger.info(f"Debug mode: {debug_mode}")

    app.run(host="0.0.0.0", port=port, debug=debug_mode)
