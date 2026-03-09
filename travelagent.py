import requests

def get_country_by_name(name):
    if name.strip() == "":
        return None

    url = "https://restcountries.com/v3.1/name/" + name

    try:
        response = requests.get(url)

        if response.status_code == 200:
            info = response.json()
            return info[0]
        else:
            print("Error:", response.status_code)
            return None

    except Exception as e:
        print("Error:", e)
        return None
