import requests as re
from datetime import datetime, timedelta


def stations_near_auto():
    station_data = []
    station_url = "http://environment.data.gov.uk/flood-monitoring/id/stations"
    get_data = re.get(station_url)
    get_data.raise_for_status()
    analysis = get_data.json()
    items = analysis["items"]
    for i in range(len(items)):
        try:
            station_data.append(dict(
                label=items[i]["label"],
                lat=items[i]["lat"],
                long=items[i]["long"],
                id=items[i]["@id"], ))
        except:
            pass
    return station_data


def measures(station_id):
    measures_url = str(station_id) + "/measures"
    measures_data = re.get(measures_url)
    measures_data.raise_for_status()
    analysis = measures_data.json()
    items = analysis["items"]
    return items


def reading(url):
    values = []
    now = datetime.today()
    at_24h_earlier = now - timedelta(days=1)
    reading_url = url + "/readings?_sorted&_limit=500"
    reading_data = re.get(reading_url)
    reading_data.raise_for_status()
    data = reading_data.json()
    value_data = data["items"]
    for i in range(len(value_data)):
        date = datetime.strptime(value_data[i]["dateTime"], "%Y-%m-%dT%H:%M:%SZ")
        if date > at_24h_earlier:
            values.append(dict(
                timestamp=date,
                elevation=value_data[i]["value"]
            ))
    return values
