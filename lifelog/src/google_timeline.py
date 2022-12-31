import json
import csv
import os
import calendar

import date

# Used to convert month names into its numeric value
MONTH_NAMES = tuple(m.upper() for m in calendar.month_name)

def _xor(p: bool, q: bool) -> bool:
    return (not p and q) or (p and not q)

def _sort(files: list) -> list:
    # Associate each file names with the numeric value for the date on the file name
    unsorted_files = [[f, _get_date(f)] for f in files]
    # Return the sorted copy of the file names
    return [f[0] for f in sorted(unsorted_files, key=lambda date: date[1], reverse=True)]

def _get_date(file_name: str) -> tuple:
    # Extract the date from the file name
    year_month = file_name.split(os.path.sep)[-1][:-5]
    # Separate year and month from the date from the file name
    year, month = year_month.split('_')
    # Return the numeric value each
    return int(year), MONTH_NAMES.index(month)

def generate_csv(source: str, destination: str) -> None:
    valid_path = [
        # From Korean accounts
        os.path.join('Takeout', '위치 기록', 'Semantic Location History'),
        # From English (U.S.) accounts
        os.path.join('Takeout', 'Location History', 'Semantic Location History')
    ]

    # Get all the file names from the source TAR file
    source_files = source.getnames()

    # Extract all the JSON files located under the Semantic Location History directory
    unsorted_files = [f for f in source_files if _xor(valid_path[0] in f, valid_path[1] in f)]

    if len(unsorted_files) > 0:
        # Process relevant data then export it into a CSV file
        with open(os.path.join(destination, 'location-history.csv'), 'w', newline='', encoding='utf-8') as location_history_csv:
            csv_writer = csv.writer(location_history_csv, quoting=csv.QUOTE_ALL)
            csv_writer.writerow([
                'ActivityType', 
                'Distance', 
                'StartTimestamp', 
                'EndTimestamp', 
                'StartLatitude', 
                'StartLongitude', 
                'EndLatitude', 
                'EndLongitude'
            ])
            sorted_files = _sort(unsorted_files) # Sort the JSON files
            month_count = 0
            for sorted_file in sorted_files:
                # Limit the data extracted within six months
                if month_count < 6:
                    location_history_json = source.extractfile(source.getmember(sorted_file))
                    location_history = json.load(location_history_json)
                    for obj in location_history['timelineObjects']:
                        if 'activitySegment' in obj:
                            csv_writer.writerow([
                                obj['activitySegment']['activityType'],                                     # Activity Type
                                obj['activitySegment']['distance'],                                         # Distance (in meters)
                                date.iso_to_date(obj['activitySegment']['duration']['startTimestamp']),     # Start Timestamp
                                date.iso_to_date(obj['activitySegment']['duration']['endTimestamp']),       # End Timestamp
                                float(obj['activitySegment']['startLocation']['latitudeE7']) / 10.0E+6,     # Start Latitude
                                float(obj['activitySegment']['startLocation']['longitudeE7']) / 10.0E+6,    # Start Longitude
                                float(obj['activitySegment']['endLocation']['latitudeE7']) / 10.0E+6,       # End Latitude
                                float(obj['activitySegment']['endLocation']['longitudeE7']) / 10.0E+6       # End Longitude
                            ])
                        else:
                            csv_writer.writerow([
                                'PLACE_VISIT',                                                              # Activity Type
                                0,                                                                          # Distance (in meters)
                                date.iso_to_date(obj['placeVisit']['duration']['startTimestamp']),          # Start Timestamp
                                date.iso_to_date(obj['placeVisit']['duration']['endTimestamp']),            # End Timestamp
                                float(obj['placeVisit']['location']['latitudeE7']) / 10.0E+6,               # Start Latitude
                                float(obj['placeVisit']['location']['longitudeE7']) / 10.0E+6,              # Start Longitude
                                float(obj['placeVisit']['location']['latitudeE7']) / 10.0E+6,               # End Latitude
                                float(obj['placeVisit']['location']['longitudeE7']) / 10.0E+6               # End Longitude
                            ])
                    month_count = month_count + 1
                else:
                    break
    else:
        return
