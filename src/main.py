from dotenv import load_dotenv
import logging
import os
from datetime import datetime
import pandas as pd
import googlemaps
from src.create_mock_data.create_data import generate_candidates, generate_employer

logging.basicConfig(level=logging.INFO)

load_dotenv()
api_key = os.getenv("API_KEY")
maps = googlemaps.Client(key=api_key)

employer = generate_employer()
candidates_csv_path = 'data/mock_candidates.csv'

def find_suitable_candidates(employer=employer, candidates_csv=candidates_csv_path):
    function_start_time = datetime.now()
    employer_postcode = employer[1]
    departure_time = datetime(2025, 1, 15, 8, 0)

    df = pd.read_csv(candidates_csv)

    travel_times = []
    
    for candidate_postcode in df['Postcode']:
        try:
            request = maps.directions(candidate_postcode, employer_postcode, mode="transit", departure_time=departure_time)
            travel_time = request[0]['legs'][0]['duration']['text']
            travel_times.append(travel_time)
        except:
            travel_times.append("null")
            logging.warning(f"{candidate_postcode} could not be located.")
    
    for i in range(len(travel_times)):
        t = travel_times[i]
        if t != "null":
            mins = 0
            if 'hour' in t:
                mins += int(t[0]) * 60
            if 'min' in t:
                mins += int(t.split()[-2])
            travel_times[i] = mins
            
    df['Travel Time (mins)'] = travel_times
    df = df[df['Travel Time (mins)'] != 'null']

    if 'Qualifications/10' in df.columns and 'Communication/5' in df.columns:
        df['Overall Suitability'] = ((df['Qualifications/10'] + df['Communication/5'] + (60-df['Travel Time (mins)'])/4)/30 * 100)
        df = df.sort_values(by='Overall Suitability', ascending=False)
        df['Overall Suitability'] = df['Overall Suitability'].astype(int).apply(lambda x: f"{x}%")
    else:
        df = df.sort_values(by='Travel Time (mins)')

    function_end_time = datetime.now()
    elapsed = round((function_end_time - function_start_time).total_seconds(), 3)

    with open('data/final_table.md', 'w') as f:
        f.write(f"### Employer name: {employer[0]}\n\n")
        f.write(f"**Employer address: {employer[1]}**\n\n")
        f.write(f"**Candidates analysed in {elapsed} seconds:**\n\n")
        f.write(df.to_markdown(index=False))
    
    return df

find_suitable_candidates()