import pandas as pd
from src.main import find_suitable_candidates

def test_find_suitable_candidates_orders_by_duration_when_just_travel_time_is_true():
    df = find_suitable_candidates(just_travel_time=True)
    assert df['Travel Time (mins)'].is_monotonic_increasing