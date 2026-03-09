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

def show_country(country):

    print("--- COUNTRY INFO ---")

    official = country["name"]["official"]
    print("Official:", official)

    if "capital" in country and len(country["capital"]) > 0:
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

    if "flags" in country and "png" in country["flags"]:
        print("Flag:", country["flags"]["png"])
    else:
        print("Flag: N/A")

def show_weather(country):

    print("--- WEATHER ---")

    lat = None
    lon = None

    if "latlng" in country:
        lat = country["latlng"][0]
        lon = country["latlng"][1]

    if lat == None or lon == None:
        print("Weather: N/A")
        return

    url = "https://api.open-meteo.com/v1/forecast?latitude=" + str(lat) + "&longitude=" + str(lon) + "&current_weather=true"

    try:
        r = requests.get(url)

        if r.status_code == 200:
            data = r.json()

            if "current_weather" in data:
                w = data["current_weather"]
                print("Temp:", w["temperature"], "C")
                print("Wind:", w["windspeed"])
            else:
                print("Weather: N/A")
        else:
            print("Weather: N/A")

    except:
        print("Weather: N/A")

def show_timezones(country):

    print("--- TIMEZONES ---")

    if "timezones" in country:
        print("Timezones:", ", ".join(country["timezones"]))
    else:
        print("Timezones: N/A")
    
def load_plans():
    try:
        f = open("plans.json", "r", encoding="utf-8")
        text = f.read()
        f.close()

        if text.strip() == "":
            return []

        plans = eval(text)
        return plans
    except:
        return []
    
def save_plans(plans):
    f = open("plans.json", "w", encoding="utf-8")
    f.write(str(plans))
    f.close()