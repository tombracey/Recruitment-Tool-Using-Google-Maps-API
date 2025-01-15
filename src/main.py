from dotenv import load_dotenv
import os
from datetime import datetime
import pandas as pd
import googlemaps
from create_mock_data.create_data import generate_candidates, generate_company

load_dotenv()
api_key = os.getenv("API_KEY")
maps = googlemaps.Client(key=api_key)

company = generate_company()
candidates_csv_path = 'data/mock_candidates.csv'

def find_suitable_candidates(company=company, candidates_csv=candidates_csv_path, just_travel_time=False):
    company_postcode = company[1]
    departure_time = datetime(2025, 1, 15, 8, 0)

    df = pd.read_csv(candidates_csv)

    travel_times = []
    
    for candidate_postcode in df['Postcode']:
        try:
            request = maps.directions(candidate_postcode, company_postcode, mode="transit", departure_time=departure_time)
            travel_time = request[0]['legs'][0]['duration']['text']
            travel_times.append(travel_time)
        except:
            travel_times.append("null")

    for i in range(len(travel_times)):
        t = travel_times[i]
        if t != "null":
            mins = 0
            if 'hour' in t:
                mins += int(t[0]) * 60
            if 'min' in t:
                mins += int(t.split('min')[0].strip().split()[-1])
            travel_times[i] = mins
            
    df['Travel Time (mins)'] = travel_times
    df = df[df['Travel Time (mins)'] != 'null']

    if just_travel_time:
        df = df.sort_values(by='Travel Time (mins)')
    else:
        df['Overall Suitability'] = ((df['Qualifications'] + df['Communication'] + (60-df['Travel Time (mins)'])/4)/30 * 100)
        df = df.sort_values(by='Overall Suitability', ascending=False)
        df['Overall Suitability'] = df['Overall Suitability'].astype(int).apply(lambda x: f"{x}%")

    with open('data/results.md', 'w') as f:
        f.write(f"Company name: {company[0]}\n\n")
        f.write(f"Company address: {company[1]}\n\n")
        f.write(f"Candidate analysis:\n\n")
        f.write(df.to_markdown(index=False))

find_suitable_candidates(company=('Kirbys AFX', 'W7 3QP'))