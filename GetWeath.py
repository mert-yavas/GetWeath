import requests
import os
from dotenv import load_dotenv
from prettytable import PrettyTable
import datetime
from datetime import timezone

# Hiding api key with dotenv library
load_dotenv()
api_key = os.getenv("api_key")


def main():
    city = get_city_from_user()
    unit_choise_func(city)


# function to receive input from the user
def get_city_from_user():
    return input("What's the weather?\nEnter city name: ")


# the program outputs the results here in metric or imperial, divided into two.
def unit_choise_func(city):
    unit_choise = input("Which unit? (1 for Metric / 2 for Imperial): ")
    if unit_choise == "1":
        table_data = metric_units(city)
        table_forecast_data = metric_forecast(city)
        if isinstance(table_data, list) and isinstance(table_forecast_data, list):
            table_GetWeath(table_data)
            table_forecast(table_forecast_data)
        else:
            print(table_data)
            main()

    elif unit_choise == "2":
        table_data_imp = imperial_units(city)
        table_forcast_data_imp = imperial_forecast(city)
        if isinstance(table_data_imp, list) and isinstance(
            table_forcast_data_imp, list
        ):
            table_GetWeath_imperial(table_data_imp)
            table_forcast_imp(table_forcast_data_imp)
        else:
            print(table_data_imp)
            main()
    else:
        print("Invalid choice. Please select 1 or 2.")
        unit_choise_func(city)


# API queries return values such as temperature, wind direction and speed,
# humidity, weather, pressure, country in metric units.
def metric_units(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data_metric = response.json()
        temperature_metric = data_metric["main"]["temp"]
        humidity_metric = data_metric["main"]["humidity"]
        pressure_metric = data_metric["main"]["pressure"]
        weather_metric = data_metric["weather"][0]["description"]
        country_metric = data_metric["sys"]["country"]
        wind_metric = data_metric["wind"]["speed"]
        wind_deg_metric = data_metric["wind"]["deg"]

        return [
            city,
            country_metric,
            temperature_metric,
            humidity_metric,
            wind_metric,
            wind_deg_metric,
            pressure_metric,
            weather_metric,
        ]
    elif response.status_code == 404:
        return "City not found.Please check the city name."
    else:
        return "Something went wrong 😱. Please try again later."


# returns five days of weather and temperature forecast values in metric units.
def metric_forecast(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?units=metric&appid={api_key}&q={city}"
    response = requests.get(url)

    # Check the status code of the response
    if response.status_code == 200:
        data = response.json()

        # check for the existence of the 'list' key
        if "list" in data:
            filtered_data = []
            for item in data["list"]:
                if item["dt_txt"].endswith("12:00:00"):
                    timestamp = item["dt"]
                    formatted_date = datetime.datetime.fromtimestamp(timestamp, timezone.utc).strftime('%d-%m-%Y')
                    temperature_forecast = item["main"]["temp"]
                    weather_description = item["weather"][0]["description"]
                    filtered_data.append(
                        [
                            formatted_date,
                            temperature_type_metric(temperature_forecast),
                            precipitation(weather_description),
                        ]
                    )
            return filtered_data
        else:
            return "Data format error: 'list' key not found."

    elif response.status_code == 404:
        return "City not found.Please check the city name."

    else:
        return "Something went wrong 😱. Please try again later."


# API queries return values such as temperature, wind direction and speed,
# humidity, weather, pressure, country in imperial units.
def imperial_units(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&appid={api_key}"
    response = requests.get(url)
    # Check the status code of the response
    if response.status_code == 200:
        data_imperial = response.json()
        temperature_imperial = data_imperial["main"]["temp"]
        humidity_imperial = data_imperial["main"]["humidity"]
        pressure_imperial = data_imperial["main"]["pressure"]
        weather_imperial = data_imperial["weather"][0]["description"]
        country_imperial = data_imperial["sys"]["country"]
        wind_imperial = data_imperial["wind"]["speed"]
        wind_deg_imperial = data_imperial["wind"]["deg"]

        return [
            city,
            country_imperial,
            temperature_imperial,
            humidity_imperial,
            wind_imperial,
            wind_deg_imperial,
            pressure_imperial,
            weather_imperial,
        ]
    elif response.status_code == 404:
        return "City not found.Please check the city name."
    else:
        return "Something went wrong 😱. Please try again later."


# returns five days of weather and temperature forecast values in imperial units.
def imperial_forecast(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?units=imperial&appid={api_key}&q={city}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        # check for the existence of the 'list' key
        if "list" in data:
            filtered_data_imp = []
            for item in data["list"]:
                if item["dt_txt"].endswith("12:00:00"):
                    timestamp = item["dt"]
                    formatted_date_imp = datetime.datetime.fromtimestamp(timestamp, timezone.utc).strftime('%m-%d-%Y')
                    temperature_forecast_imperial = item["main"]["temp"]
                    weather_description_imperial = item["weather"][0]["description"]
                    filtered_data_imp.append(
                        [
                            formatted_date_imp,
                            temperature_type_imperial(temperature_forecast_imperial),
                            precipitation(weather_description_imperial),
                        ]
                    )

            return filtered_data_imp
        else:
            return "Data format error: 'list' key not found."

    elif response.status_code == 404:
        return "City not found.Please check the city name."

    else:
        return "Something went wrong 😱. Please try again later."


# In general, temperatures below 0°C are considered cold air and
# temperatures above 30°C are considered hot air.
# Considering this situation, it is aimed to regulate emoji.
def temperature_type_metric(temperature):
    if temperature >= 30:
        return f"{temperature}°C 🌡️"
    elif temperature <= 0:
        return f"{temperature}°C 🥶"
    else:
        return f"{temperature}°C"


# 0°C = 32°F
# 30°C = 86°F
# intended to return similar values
def temperature_type_imperial(temperature):
    if temperature >= 86:
        return f"{temperature}°F 🌡️"
    elif temperature <= 32:
        return f"{temperature}°F 🥶"
    else:
        return f"{temperature}°F"


# In Json data, the wind direction is given in degrees.
# Using these degrees, the compass is arranged according to the corresponding direction.
def wind_way(wind_deg):
    if 11.25 <= wind_deg < 33.75:
        return "NNE"
    elif 33.75 <= wind_deg < 56.25:
        return "NE"
    elif 56.25 <= wind_deg < 78.75:
        return "ENE"
    elif 78.75 <= wind_deg < 101.25:
        return "E"
    elif 101.25 <= wind_deg < 123.75:
        return "ESE"
    elif 123.75 <= wind_deg < 146.25:
        return "SE"
    elif 146.25 <= wind_deg < 168.75:
        return "SSE"
    elif 168.75 <= wind_deg < 191.25:
        return "S"
    elif 191.25 <= wind_deg < 213.75:
        return "SSW"
    elif 213.75 <= wind_deg < 236.25:
        return "SW"
    elif 236.25 <= wind_deg < 258.75:
        return "WSW"
    elif 258.75 <= wind_deg < 281.25:
        return "W"
    elif 281.25 <= wind_deg < 303.75:
        return "WNW"
    elif 303.75 <= wind_deg < 326.25:
        return "NW"
    elif 326.25 <= wind_deg < 348.75:
        return "NNW"
    else:
        return "N"


# In Json data, wind speed is given in m/sec.
# To make the wind speed more understandable, the m/sec value has been converted to km/h.
# 1 m/s = 3.6 km/h.
def wind_speed_convert(wind):
    converted_wind_speed = wind * 3.6
    return f"{converted_wind_speed:.1f} km/h"


# In order to beautify the output of the code we write, the emoji adjusted
# according to the weather conditions are transformed in this function.
def precipitation(weather):
    if "thunderstorm" in weather:
        return f"⛈️ {weather}".title()
    elif "rain" in weather:
        return f"☔ {weather}".title()
    elif "clouds" in weather:
        return f"☁ {weather}".title()
    elif "drizzle" in weather:
        return f"🌦️ {weather}".title()
    elif "mist" in weather:
        return f"🌫️ {weather}".title()
    elif "snow" in weather:
        return f"❄️ {weather}".title()
    elif "sun" in weather or "clear" in weather:
        return f"☀ {weather}".title()


# The outputs we get using the PrettyTable library are shown in the terminal with pretty tables.
# The four functions below also convert the generated outputs into a table.
def table_GetWeath(table_data):
    table = PrettyTable()
    table.field_names = [
        "City",
        "Country",
        "Temperature",
        "Humidity",
        "Wind Speed",
        "Wind Direction",
        "Pressure",
        "Weather Conditions",
    ]

    table.add_row(
        [
            table_data[0].capitalize(),
            table_data[1],
            temperature_type_metric(table_data[2]),
            f"% {table_data[3]}",
            wind_speed_convert(table_data[4]),
            wind_way(table_data[5]),
            f"{table_data[6]} hPa",
            precipitation(table_data[7]),
        ]
    )
    print(table)


def table_GetWeath_imperial(table_data_imp):
    table = PrettyTable()
    table.field_names = [
        "City",
        "Country",
        "Temperature",
        "Humidity",
        "Wind Speed",
        "Wind Direction",
        "Pressure",
        "Weather Conditions",
    ]

    table.add_row(
        [
            table_data_imp[0].capitalize(),
            table_data_imp[1],
            temperature_type_imperial(table_data_imp[2]),
            f"% {table_data_imp[3]}",
            f"{table_data_imp[4]} mph",
            wind_way(table_data_imp[5]),
            f"{table_data_imp[6]} hPa",
            precipitation(table_data_imp[7]),
        ]
    )
    print(table)


def table_forcast_imp(table_forcast_data_imp):
    table = PrettyTable()
    table.title = "Weather Forecast"
    table.field_names = ["Date", "Temperature", "Weather Conditions"]
    table.align["Weather Conditions"] = "l"

    for row in table_forcast_data_imp:
        table.add_row(row)

    print(table)


def table_forecast(table_forecast_data):
    table = PrettyTable()
    table.title = "Weather Forecast"
    table.field_names = ["Date", "Temperature", "Weather Conditions"]
    table.align["Weather Conditions"] = "l"

    for row in table_forecast_data:
        table.add_row(row)

    print(table)


if __name__ == "__main__":
    main()
