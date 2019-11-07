import pytankerkoenig as api
from prometheus_client import start_http_server, Gauge, Enum
# import schedule
import time
import os

try:
    api_key = os.environ['API_KEY']
    station_id = os.environ['STATION_ID']
except KeyError:
    print('Please set API_KEY and STATION_ID as environment variables. Bye.')
    exit(1)

price_e5 = Gauge('price_e5', 'Current price for Super E5 Fuel')
price_e10 = Gauge('price_e10', 'Current price for Super E10 Fuel')
price_diesel = Gauge('price_diesel', 'Current price for Diesel Fuel')
fuel_station_open = Enum('fuel_station_open', 'Fuel station current open state', states=['open', 'closed']) # TODO: Better wording here


def update_metrics():
    data = api.getStationData(api_key, station_id)

    price_e5.set(data['station']['e5'])
    price_e10.set(data['station']['e10'])
    price_diesel.set(data['station']['diesel'])
    if data['station']['isOpen']:
        fuel_station_open.state('open')
    else:
        fuel_station_open.state('closed')


if __name__ == '__main__':
    # update_metrics()  # run once to start without null data
    start_http_server(8000)
    # schedule.every(5).minutes.do(update_metrics)

    while True:
        update_metrics()
        time.sleep(300)
    #     schedule.run_pending()
    #     time.sleep(1)
