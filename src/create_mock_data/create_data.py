import random
import csv
from faker import Faker
from src.create_mock_data.get_london_postcodes import get_london_postcodes

fake = Faker()

def generate_candidates(num):
    candidates_names = [fake.name() for _ in range(num)]
    candidates_postcodes = get_london_postcodes(num)
    qualifications = [random.randint(3, 10) for _ in range(num)]
    communication = [random.randint(2, 5) for _ in range(num)]

    candidates = zip(candidates_names, candidates_postcodes, qualifications, communication)

    with open('data/mock_candidates.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Postcode', 'Qualifications', 'Communication'])
        writer.writerows(candidates)
    
generate_candidates(100)

def generate_company():
    company_name = fake.company()
    company_postcode = get_london_postcodes(1)[0]
    return company_name, company_postcode



