#! /usr/bin/env python

import errno, sys, os
import tarfile, json, csv
import xmltodict
from dateutil import parser, relativedelta, utils
from datetime import datetime, timedelta

from pprint import pprint

def process_google_takeout(source_dir, destination_dir):
    if tarfile.is_tarfile(source_dir):
        source_file = tarfile.open(name=source_dir, mode='r')

        # Get the Android activity JSON file, if it exists
        try:
            # For Korean accounts
            android_activity_json = source_file.extractfile(
                source_file.getmember(
                    os.path.join('Takeout', '내 활동', 'Android', '내활동.json')
                )
            )
        except:
            # For English (U.S.) accounts
            try:
                android_activity_json = source_file.extractfile(
                    source_file.getmember(
                        os.path.join('Takeout', 'My Activity', 'Android', 'MyActivity.json')
                    )
                )
            except:
                # TODO: Handle other types of accounts, otherwise...
                pass
        
        android_activity = json.load(android_activity_json)
        
        # Get the date and time for the most recent Android activity
        present = parser.parse(android_activity[0]['time'])

        # Get the date and time for the Android activity from six months ago
        past = present + relativedelta.relativedelta(months=-6)

        # Get the number of days between those times
        num_days = abs(present - past).days
        
        # Process relevant data then export it into a CSV file
        with open(os.path.join(destination_dir, 'android_activity.csv'), 'w', newline='') as android_activity_csv:
            csv_writer = csv.DictWriter(android_activity_csv, fieldnames=['Application', 'Date'])
            csv_writer.writeheader()
            for i in range(len(android_activity)):
                # Get the time of the current activity
                current = parser.parse(android_activity[i]['time'])
                # Check if the current antivity is within the range of six months
                if utils.within_delta(present, current, timedelta(days=num_days)):
                    csv_writer.writerow({'Application' : android_activity[i]['header'], 'Date' : current})
                else:
                    break

def to_iso_format(epoch):
    return datetime.fromtimestamp(float(epoch[:10] + '.' + epoch[10:])).isoformat()

def process_call_log(source_dir, destination_dir):
    # Call type reference from: https://developer.android.com/reference/android/provider/CallLog.Calls
    call_type = ['incoming', 'outgoing', 'missed', 'voicemail', 'rejected', 'blocked', 'answered_externally']

    with open(source_dir, 'r', encoding='utf-8') as call_log_file:
        # Load the XML file
        call_log_xml = call_log_file.read()
        call_log = xmltodict.parse(call_log_xml)
        
        # Get the date and time for the most recent call
        present_iso = to_iso_format(call_log['alllogs']['log'][0]['@date'])
        present = parser.parse(present_iso)

        # Get the date and time for the call from six months ago
        past = present + relativedelta.relativedelta(months=-6)

        # Get the number of days between those times
        num_days = abs(present - past).days

        # Process relevant data then export it into a CSV file
        with open(os.path.join(destination_dir, 'call_log.csv'), 'w', newline='') as call_log_csv:
            csv_writer = csv.DictWriter(call_log_csv, fieldnames=['Number', 'Date', 'CallType', 'CallDuration'])
            csv_writer.writeheader()
            for log in call_log['alllogs']['log']:
                current = parser.parse(to_iso_format(log['@date']))
                if utils.within_delta(present, current, timedelta(days=num_days)):
                    csv_writer.writerow({
                        'Number' : str(log['@number']),
                        'Date' : current,
                        'CallType' : call_type[int(log['@type']) - 1],
                        'CallDuration' : log['@dur'],
                    })
                else:
                    break

def main():
    # Create a directory for clean data
    try:
        os.mkdir(os.path.join(os.curdir, 'clean_data'))
    except FileExistsError:
        # Ignore if the directory already exists
        pass

    # Get a list of research identifiers
    try:
        # Use the user specified directory name
        dirty_data_dir = sys.argv[1]
    except IndexError:
        # Otherwise, use the default directory name
        dirty_data_dir = 'dirty_data'
    finally:
        # Check if the directory actually exists
        if os.path.exists(os.path.join(os.curdir, dirty_data_dir)):
            r_id = os.listdir(os.path.join(os.curdir, dirty_data_dir))
        else:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), dirty_data_dir)

    for id in r_id:
        # Create a subdirectory in clean_data for the research identifier
        try:
            os.mkdir(os.path.join(os.curdir, 'clean_data', id))
        except FileExistsError:
            # Ignore if the directory already exists
            pass

        # Get a list of files contained in the research identifier in dirty data
        files = os.listdir(os.path.join(os.curdir, dirty_data_dir, id))

        clean_file_path = os.path.join(os.curdir, 'clean_data', id)

        for file in files:
            dirty_file_path = os.path.join(os.curdir, dirty_data_dir, id, file)

            # Handle Google Takeout lifelog data
            if 'takeout-' in file and ('.tgz' in file or '.gtar' in file):
                process_google_takeout(dirty_file_path, clean_file_path)
            # Handle call log file
            elif 'calllogs_' in file and '.xml' in file:
                process_call_log(dirty_file_path, clean_file_path)
            else:
                pass
        
if __name__ == '__main__':
    main()
