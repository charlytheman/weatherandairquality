import streamlit as st
import requests
import datetime

api_key = "3908999f-bd56-455a-b5c2-b778c948d895"
current_date = datetime.date.today()

st.title("Weather and Air Quality Web App")
st.header("Streamlit and AirVisual API")


@st.cache_data
def map_creator(latitude, longitude):
    from streamlit_folium import folium_static
    import folium

    m = folium.Map(location=[latitude, longitude], zoom_start=10)
    folium.Marker([latitude, longitude], popup="Station", tooltip="Station").add_to(m)
    folium_static(m)



@st.cache_data
def generate_list_of_countries():
    countries_url = f"https://api.airvisual.com/v2/countries?key={api_key}"
    countries_dict = requests.get(countries_url).json()
    # st.write(countries_dict)
    return countries_dict

@st.cache_data
def generate_list_of_states(country_selected):
    states_url = f"https://api.airvisual.com/v2/states?country={country_selected}&key={api_key}"
    states_dict = requests.get(states_url).json()
    # st.write(states_dict)
    return states_dict

@st.cache_data
def generate_list_of_cities(state_selected,country_selected):
    cities_url = f"https://api.airvisual.com/v2/cities?state={state_selected}&country={country_selected}&key={api_key}"
    cities_dict = requests.get(cities_url).json()
    # st.write(cities_dict)
    return cities_dict


category = st.selectbox("Choose a category",
                        options=["By City, State, and Country", "By Nearest City (IP Address)",
                                 "By Latitude and Longitude"])

if category == "By City, State, and Country":
    countries_dict = generate_list_of_countries()
    if countries_dict["status"] == "success":
        countries_list = []
        for i in countries_dict["data"]:
            countries_list.append(i["country"])
        countries_list.insert(0, "")

        country_selected = st.selectbox("Select a country", options=countries_list)
        if country_selected:
            states_dict = generate_list_of_states(country_selected)
            states_list = [state["state"] for state in states_dict["data"]]
            state_selected = st.selectbox("Select a state", options=states_list)

            if state_selected:
                cities_dict = generate_list_of_cities(state_selected, country_selected)
                cities_list = [city["city"] for city in cities_dict["data"]]
                city_selected = st.selectbox("Select a city", options=cities_list)

                if city_selected:
                    aqi_data_url = f"https://api.airvisual.com/v2/city?city={city_selected}&state={state_selected}&country={country_selected}&key={api_key}"
                    aqi_data_dict = requests.get(aqi_data_url).json()

                    if aqi_data_dict["status"] == "success":

                        latitude = aqi_data_dict["data"]["location"]["coordinates"][1]
                        longitude = aqi_data_dict["data"]["location"]["coordinates"][0]
                        map_creator(latitude, longitude)
                        # Display the weather and air quality data
                        st.subheader("Weather Information")
                        st.info(f"Today is {current_date}")
                        st.info(f"Temperature: {aqi_data_dict['data']['current']['weather']['tp']}°C")
                        st.info(f"Humidity is {aqi_data_dict['data']['current']['weather']['hu']}%")
                        st.info(
                            f"The air quality index is currently {aqi_data_dict['data']['current']['pollution']['aqius']}")

                    else:
                        st.warning("No data available for this location.")
                else:
                    st.warning("No stations available, please select another state.")
            else:
                st.warning("No stations available, please select another country.")
    else:
        st.error("Too many requests. Wait for a few minutes before your next API call.")

elif category == "By Nearest City (IP Address)":
    url = f"https://api.airvisual.com/v2/nearest_city?key={api_key}"
    aqi_data_dict = requests.get(url).json()

    if aqi_data_dict["status"] == "success":

        latitude = aqi_data_dict["data"]["location"]["coordinates"][1]
        longitude = aqi_data_dict["data"]["location"]["coordinates"][0]
        map_creator(latitude, longitude)

        # Display the weather and air quality data
        st.subheader("Weather Information")
        st.info(f"Today is {current_date}")
        st.info(f"Temperature: {aqi_data_dict['data']['current']['weather']['tp']}°C")
        st.info(f"Humidity is {aqi_data_dict['data']['current']['weather']['hu']}%")
        st.info(f"The air quality index is currently {aqi_data_dict['data']['current']['pollution']['aqius']}")

    else:
        st.warning("No data available for this location.")


elif category == "By Latitude and Longitude":
    latitude = st.text_input("Enter latitude, e.g. 38.89511")
    longitude = st.text_input("Enter longitude, e.g.  -77.03637")

    if latitude and longitude:
        url = f"https://api.airvisual.com/v2/nearest_city?lat={latitude}&lon={longitude}&key={api_key}"
        aqi_data_dict = requests.get(url).json()

        if aqi_data_dict["status"] == "success":

            latitude = aqi_data_dict["data"]["location"]["coordinates"][1]
            longitude = aqi_data_dict["data"]["location"]["coordinates"][0]
            map_creator(latitude, longitude)

            # Display the weather and air quality data
            st.subheader("Weather Information")
            st.info(f"Today is {current_date}")
            st.info(f"Temperature: {aqi_data_dict['data']['current']['weather']['tp']}°C")
            st.info(f"Humidity is {aqi_data_dict['data']['current']['weather']['hu']}%")
            st.info(f"The air quality index is currently {aqi_data_dict['data']['current']['pollution']['aqius']}")

        else:
            st.warning("No data available for this location.")
