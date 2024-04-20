import streamlit as st
from bs4 import BeautifulSoup
import requests
import pandas as pd

st.title("company information scraper")
url = st.text_input("https://www.ycombinator.com/companies?batch=W24")

if st.button('scrape'):
    response = requests.get(url)

    if response.status_code==200:
        soup = BeautifulSoup(response.content,"html.parser")
        founders_names = soup.find_all('div', class_="font-bold")
        founders = len(founders_names) -1
        team_size_span = soup.find('span', text="Team Size:")
        Location_span = soup.find('span', text="Location:")

        st.write("Number of active founders:")
        st.write(founders)

        # Extract the number associated with team size
        team_size_number = None
        if team_size_span:
            next_sibling = team_size_span.find_next_sibling()
        if next_sibling:
            team_size_number = next_sibling.get_text(strip=True)

        # Display the team size number
        st.write("Team Size:")
        if team_size_number:
            st.write(team_size_number)
        else:
            st.write("Team size number not found")

        Location = None
        if Location_span:
            next_sibling = Location_span.find_next_sibling()
        if next_sibling:
            Location = next_sibling.get_text(strip=True)

        st.write("Location:")
        if Location:
            st.write(Location)
        else:
            st.write("Location not found")
        
        data = {'Attribute': ['Number of Active Founders', 'Team Size', 'Location'],'Value': [founders, team_size_number, Location]}
        df = pd.DataFrame(data)
        df['Value'] = df['Value'].astype(str)
        # Display DataFrame
        st.write("### Data Summary")
        st.write(df)

        # Visualize DataFrame
        st.write("### Visualization")
        st.bar_chart(df.set_index('Attribute').T)
    else:
        st.error("Failed to fetch data from the provided URL. Please check the URL and try again.")
        
        