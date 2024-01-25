import requests


def test():
    data = {
        "card_number": "4046804185457499",
        "weather_station": "d42efb47-9078-4ec6-897c-d65bf2b71134",
    }
    response = requests.post(
        "http://192.168.0.156:8000//api/check_employee_card/", data=data
    )
    print(response.status_code)
    
test()