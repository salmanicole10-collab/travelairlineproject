import requests

def get_country_by_name(name):
    if name.strip() == "":
        return None

    url = "https://restcountries.com/v3.1/name/" + name
    r = requests.get(url)

    if r.status_code != 200:
        return None

    data = r.json()
    return data[0]
