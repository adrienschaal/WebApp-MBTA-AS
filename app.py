import requests
from flask import Flask, render_template, request
import mbta_helper
from config import weather_api_key, TICKETMASTER_API_KEY

app = Flask(__name__)

def get_weather_info():
    city = "Boston"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=imperial"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Extracting the temperature and weather description
        temperature = data['main']['temp']
        description = data['weather'][0]['description']
        print(temperature, description)
        return temperature, description
    else:
        return None, None
    
def get_events_info():
    city = "Boston"
    url = f"https://app.ticketmaster.com/discovery/v2/events.json?city={city}&apikey={TICKETMASTER_API_KEY}"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Check if '_embedded' exists in the response
        if '_embedded' in data:
            events = data['_embedded']['events']
            events_list = []
            for event in events:
                name = event['name']
                url = event.get('url', '#')  # Use .get for optional fields
                # Check if 'dates', 'start', and 'localDate' exist in the response
                start_date = event.get('dates', {}).get('start', {}).get('localDate', 'No Date')
                events_list.append({'name': name, 'url': url, 'start_date': start_date})
            return events_list
        else:
            print("No events found in the response.")
            return []
    else:
        print(f"Failed to fetch events. Status code: {response.status_code}")
        return []



@app.route("/")
def hello():
    # Get weather information
    temperature, weather_description = get_weather_info()
    
    # Get event information
    events = get_events_info()
    
    return render_template('index.html', temperature=temperature, weather_description=weather_description, events=events)

@app.route("/nearest_mbta", methods=['POST'])
def nearest_mbta():
    place_name = request.form['placeName']
    mbta_stop, accessible = mbta_helper.find_stop_near(place_name)

    # Get weather information
    temperature, weather_description = get_weather_info()

    # Get event information
    events = get_events_info()
    
    if mbta_stop:
        return render_template('mbta_station.html', mbta_stop=mbta_stop, accessible=accessible, temperature=temperature, weather_description=weather_description, events=events)
    else:
        return render_template('error.html', error_message="No MBTA stop found nearby. Please try another location.")

if __name__ == "__main__":
    app.run(debug=True)
