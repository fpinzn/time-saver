import requests
import os
from datetime import date
from datetime import timedelta
from datetime import datetime
from functools import reduce

ANALYTIC_DATA_ENPOINT = 'https://www.rescuetime.com/anapi/data'
ROW_HEADERS_STRING = "['Date', 'Time Spent (seconds)', 'Number of People', 'Activity', 'Category', 'Productivity']"
ACTIVITIES_TO_AVOID = ['netflix.com', 'imgur.com']
FILE_NAME = 'lostseconds'
SECONDS_TO_NOTIFY = 60 * 60 # 1 hour

def get_request_url():
    today = date.today()
    seven_days_ago =  today - timedelta(days=7)

    url = ( ANALYTIC_DATA_ENPOINT + '?'
            '&perspective=interval'
            '&interval=hour'
            '&format=json'
            f'&key={os.environ["RESCUETIME_API_KEY"]}'
            f'&restrict_begin={seven_days_ago.strftime("%Y-%m-%d")}'
            f'&restrict_end={today.strftime("%Y-%m-%d")}')

    return url

def get_rescue_time_info():
    r = requests.get(get_request_url())
    return r.json()

def get_lost_seconds(rescue_time_info):
    assert str(rescue_time_info['row_headers']) == ROW_HEADERS_STRING,'It seems the Rescue Time API has changed'

    # is_an_activity_to_avoid = lambda e: e[-1] == -2
    is_an_activity_to_avoid = lambda e: e[3] in ACTIVITIES_TO_AVOID
    entries = list(filter(is_an_activity_to_avoid, rescue_time_info['rows']))
    lost_seconds = sum(map(lambda e: e[1], entries))

    return lost_seconds


def get_saved_lost_seconds():
    saved_seconds = 0

    if os.path.exists(FILE_NAME):
        file = open(FILE_NAME, 'r')
        try:
            contents = file.read().split(',')
            last_time_checked = contents[0]
            saved_seconds = int(contents[1])
            file.close()
        except (ValueError, IndexError):
            print('The file with the saved information is corrupted')

    return saved_seconds, last_time_checked

def save_lost_seconds(lost_seconds):
    if (os.access(FILE_NAME, os.W_OK)):
        file = open(FILE_NAME, 'w')
        contents = str(datetime.now()) + ',' + str(lost_seconds)
        file.write(contents)
        file.close()
    else:
        print(f'Unable to write to the {FILE_NAME} file to store lost seconds')


def run ():
    api_response = get_rescue_time_info()
    lost_seconds =  get_lost_seconds(api_response)
    previously_lost_seconds, last_time_checked = get_saved_lost_seconds()

    save_lost_seconds(lost_seconds)

    if previously_lost_seconds + SECONDS_TO_NOTIFY < lost_seconds:
        subtitle = 'netflix and imgur hours last 7 days'
        title = str(timedelta(seconds=lost_seconds))
        os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(subtitle, title))



if __name__ == '__main__':
    run()
