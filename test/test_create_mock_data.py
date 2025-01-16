from src.create_mock_data.get_london_postcodes import get_london_postcodes
from src.create_mock_data.create_data import generate_candidates, generate_employer

class TestGetLondonPostcodes:

    def test_postcode_format(self):
        postcode = get_london_postcodes(1)[0]
        assert postcode[0].isalpha()

        second_part = postcode.split()[1]
        assert second_part[0].isdigit()
        assert second_part[1:].isalpha()

    def test_returns_the_correct_number_of_postcodes(self):
        input = 3
        expected_length = 3
        assert len(get_london_postcodes(input)) == expected_length

        input = 12
        expected_length = 12
        assert len(get_london_postcodes(input)) == expected_length

class TestCreateData:

    def test_generates_correct_number_of_candidates(self):
        input = 3
        expected_length = 3
        assert len(generate_candidates(input)) == expected_length
    
        input = 12
        expected_length = 12
        assert len(generate_candidates(input)) == expected_length