import json
import csv
import os

import date

def generate_csv(source: str, destination: str) -> None:
    # Load the JSON file
    try:
        # From Korean accounts
        android_activity_json = source.extractfile(
            source.getmember(
                os.path.join('Takeout', '내 활동', 'Android', '내활동.json')
            )
        )
    except KeyError:
        try:
            # From English (U.S.) accounts
            android_activity_json = source.extractfile(
                source.getmember(
                    os.path.join('Takeout', 'My Activity', 'Android', 'MyActivity.json')
                )
            )
        except KeyError:
            # TODO: Handle other types of accounts
            return
        except:
            # TODO: Fail silently for now
            return
    except:
        # TODO: Fail silently for now
        return

    android_activity = json.load(android_activity_json)

    # Get the date from the most recent activity
    recent_date = android_activity[0]['time']

    # Process relevant data then export it into a CSV file
    with open(os.path.join(destination, 'android-activity.csv'), 'w', newline='', encoding='utf-8') as android_activity_csv:
        csv_writer = csv.DictWriter(android_activity_csv, fieldnames=['Application', 'Date'])
        csv_writer.writeheader()
        for i in range(len(android_activity)):
            current_date = android_activity[i]['time']
            if date.within_six_months(recent_date, current_date):
                csv_writer.writerow({'Application': android_activity[i]['header'], 'Date': date.iso_to_date(current_date)})
            else:
                break
