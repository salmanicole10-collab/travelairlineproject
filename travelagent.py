import requests
from datetime import datetime, timedelta

saved_plans = []

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

    if "capitalInfo" in country and "latlng" in country["capitalInfo"]:
        lat = country["capitalInfo"]["latlng"][0]
        lon = country["capitalInfo"]["latlng"][1]

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

def show_local_time(country):

    print("--- LOCAL TIME ---")

    lat = None
    lon = None

    if "capitalInfo" in country and "latlng" in country["capitalInfo"]:
        lat = country["capitalInfo"]["latlng"][0]
        lon = country["capitalInfo"]["latlng"][1]


    elif "latlng" in country:
        lat = country["latlng"][0]
        lon = country["latlng"][1]

    if lat == None or lon == None:
        print("Local time: N/A")
        return

    url = "https://api.open-meteo.com/v1/forecast?latitude=" + str(lat) + "&longitude=" + str(lon) + "&current_weather=true&timezone=auto"

    try:
        r = requests.get(url)

        if r.status_code == 200:
            data = r.json()

            if "timezone" in data:
                print("Timezone:", data["timezone"])
            else:
                print("Timezone: N/A")

            if "current_weather" in data and "time" in data["current_weather"]:
                raw_time = data["current_weather"]["time"]

                try:
                    nice_time = datetime.strptime(raw_time, "%Y-%m-%dT%H:%M")
                    print("Local time:", nice_time.strftime("%Y-%m-%d %H:%M"))
                except:
                    print("Local time:", raw_time)
            else:
                print("Local time: N/A")
        else:
            print("Local time: N/A")

    except:
        print("Local time: N/A")
    
def show_visa_info(country):

    print("--- VISA INFO ---")

    print("Visa requirements depend on nationality.")
    print("Please check the embassy website before traveling.")

def show_timezones(country):

    print("--- TIMEZONES ---")

    if "timezones" in country:
        print("Timezones:", ", ".join(country["timezones"]))
    else:
        print("Timezones: N/A")

def estimate_cost(stops):
    total = 0

    # estadia 100 por dia
    for s in stops:
        total = total + (s["days"] * 100)

    # transportation 200 entre paises
    if len(stops) > 1:
        total = total + (len(stops) - 1) * 200

    # feee 
    total = total + 50

    return total

def valid_date(text):
    try:
        return datetime.strptime(text, "%Y-%m-%d")
    except:
        return None 
    
def ask_days():
    while True:

        text = input("Days: ")

        if text.isdigit():
            days = int(text)

            if days > 0:
                return days

        print("Invalid days. Enter a positive number.")

def ask_dates(days):

    while True:

        start = input("Start date (YYYY-MM-DD): ")
        start_obj = valid_date(start)

        end = input("End date (YYYY-MM-DD): ")
        end_obj = valid_date(end)

        if start_obj == None or end_obj == None:
            print("Invalid date format.")
            continue

        if end_obj < start_obj:
            print("End date cannot be before start date.")
            continue

        diff = (end_obj - start_obj).days

        if diff != days:
            print("Dates do not match number of days.")
            continue

        return start, end

def create_plan(stops):

    global saved_plans

    print("--- CREATE PLAN ---")

    client = input("Client name: ")
    notes = input("Notes: ")

    plan = {}
    plan["client"] = client
    plan["notes"] = notes
    plan["stops"] = stops
    plan["total_cost"] = estimate_cost(stops)

    saved_plans.append(plan)

    print("Plan saved!")
    print("Total cost:", plan["total_cost"])


def view_plans():

    global saved_plans

    print("--- SAVED PLANS ---")

    if len(saved_plans) == 0:
        print("No plans saved.")
        return

    i = 0
    while i < len(saved_plans):

        plan = saved_plans[i]

        print("\nPlan", i)
        print("Client:", plan["client"])
        print("Notes:", plan["notes"])
        print("Total cost:", plan["total_cost"])
        print("Stops:")

        j = 0
        while j < len(plan["stops"]):

            stop = plan["stops"][j]

            print(" ", j + 1, "-", stop["country"])
            print("    Days:", stop["days"])
            print("    Start:", stop["start"])
            print("    End:", stop["end"])

            j = j + 1

        i = i + 1


while True:

    print("===== LMS TRAVEL AGENCY =====")
    print("Pricing Rules:")
    print("Accommodation: $100 per day per country")
    print("Transportation between countries: $200")
    print("Agency service fee: $50")
    print("Paolo included after a year of travel")

    print("Menu:")
    print("1 - Search Country")
    print("2 - Create Travel Plan")
    print("3 - View Saved Plans")
    print("0 - Exit")

    op = input("Option: ")

    if op == "1":

        name = input("Country name: ")
        c = get_country_by_name(name)

        if c == None:
            print("Country not found")
        else:
            show_country(c)
            show_weather(c)
            show_local_time(c)
            show_visa_info(c)
            show_timezones(c)
            
    elif op == "2":

        stops = []

        while True:

            name = input("Add country or press enter to finishh): ")

            if name.strip() == "":
                break

            c = get_country_by_name(name)

            if c == None:
                print("Country not found")
                continue

            show_country(c)
            show_weather(c)
            show_local_time(c)
            show_visa_info(c)
            show_timezones(c)

            days = ask_days()

            start, end = ask_dates(days)

            stop = {}
            stop["country"] = c["name"]["official"]
            stop["days"] = days
            stop["start"] = start
            stop["end"] = end

            stops.append(stop)

        if len(stops) == 0:
            print("No stops added")
        else:
            create_plan(stops)

    elif op == "3":
        view_plans()

    elif op == "0":
        break

    else:
        print("Invalid option")