import requests

def get_country_by_name(name):
    if name.strip() == "":
        return None

    url = "https://restcountries.com/v3.1/name/" + name
    r = requests.get(url)

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

def show_country(country):

    print("--- COUNTRY INFO ---")

    official = country["name"]["official"]
    print("Official:", official)

    if "capital" in country:
        capital = country["capital"][0]
    else:
        capital = "N/A"
    print("Capital:", capital)

    if "region" in country:
        region = country["region"]
    else:
        region = "N/A"
    print("Region:", region)

    if "subregion" in country:
        subregion = country["subregion"]
    else:
        subregion = "N/A"
    print("Subregion:", subregion)

    if "population" in country:
        population = country["population"]
    else:
        population = "N/A"
    print("Population:", population)

    if "currencies" in country:
        currencies = country["currencies"]
        print("Currency:", ", ".join(currencies.keys()))
    else:
        print("Currency: N/A")

    if "languages" in country:
        languages = country["languages"]
        print("Languages:", ", ".join(languages.values()))
    else:
        print("Languages: N/A")

    if "cca2" in country and "cca3" in country:
        print("Code:", country["cca2"], "/", country["cca3"])
    else:
        print("Code: N/A")

    if "timezones" in country:
        print("Timezones:", ", ".join(country["timezones"]))
    else:
        print("Timezones: N/A")

    if "flags" in country and "png" in country["flags"]:
        print("Flag:", country["flags"]["png"])
    else:
        print("Flag: N/A")