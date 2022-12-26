import json
import csv
import os

import date

from pprint import pprint

def generate_csv(source: str, destination: str) -> None:
    try:
        location_history_records_json = source.extractfile(
            source.getmember(
                os.path.join('Takeout', '위치 기록', 'Records.json')
            )
        )
    except KeyError:
        pass
    except:
        return

    location_history_records = json.load(location_history_records_json)['locations']
    location_history_records.reverse()

    recent_timestamp = location_history_records[0]['timestamp']
    
    location_history = {
        'locationHistory': []
    }

    with open(os.path.join(destination, 'location-history.json'), 'w', encoding='utf-8') as location_history_json:
        for record in location_history_records:
            current_timestamp = record['timestamp']
            if date.within_six_months(recent_timestamp, current_timestamp):
                location_history['locationHistory'].append({
                    
                })
            else:
                break

    # for a in activity:
    #     tmplst = []
    #     for b in a['activity']:
    #         tmplst.append(b)
    #     pprint(max(tmplst, key=lambda x: x['confidence'])['type'])
    #     print()
