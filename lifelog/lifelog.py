#! /usr/bin/env python

import errno, sys, os
import tarfile, json, csv
import xml.dom.minidom
from dateutil import parser, relativedelta, utils
from datetime import timedelta

def process_google_takeout(source_dir, destination_dir):
    if tarfile.is_tarfile(source_dir):
        source_file = tarfile.open(name=source_dir, mode='r')
        
        # Google Takeout data directory path
        data_path = os.path.join(destination_dir, 'google-lifelog-data')
        
        # Create a directory for Google Takeout data
        try:
            os.mkdir(data_path)
        except FileExistsError:
            # Ignore if the directory already exists
            pass

        # For keeping track of available data
        status = {
            'android_activity_data' : '1'
        }

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
                # Android activity data does not exist
                status['android_activity_data'] = '0'
        
        # Handle Android activity data, if it exists
        if int(status['android_activity_data']):
            android_activity = json.load(android_activity_json)
            
            # Get the date and time for the most recent Android activity
            present = parser.parse(android_activity[0]['time'])

            # Get the date and time for the Android activity from six months ago
            past = present + relativedelta.relativedelta(months=-6)

            # Get the number of days between those times
            num_days = abs(present - past).days
            
            csv_file_path = os.path.join(data_path, 'android-activity-data')

            # Create a directory for the CSV file to be generated
            try:
                os.mkdir(csv_file_path)
            except FileExistsError:
                # Ignore if the directory already exists
                pass
            
            # Export the name of the application and the time accessed into a CSV file
            with open(os.path.join(csv_file_path, 'android_activity.csv'), 'w', newline='') as android_activity_csv:
                csv_writer = csv.DictWriter(android_activity_csv, fieldnames=['application', 'time_accessed'])
                csv_writer.writeheader()
                for i in range(len(android_activity)):
                    # Get the time of the current activity
                    current = parser.parse(android_activity[i]['time'])
                    # Check if the current antivity is within the range of six months
                    if utils.within_delta(present, current, timedelta(days=num_days)):
                        csv_writer.writerow({'application' : android_activity[i]['header'], 'time_accessed' : current})
                    else:
                        break

        # Write and return the status for the XML document
        xml = '<google_takeout_lifelog_data'
        for s in list(status.keys()):
            xml = xml + ' ' + s + '=' + f'"{status[s]}"'
        else:
            xml = xml + ' />'
        return xml

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

        # Create an XML document for keeping track of avaliable data
        id_xml = f'<{id}>'

        for file in files:
            # Handle Google Takeout lifelog data
            if 'takeout-' in file and ('.tgz' in file or '.gtar' in file):
                id_xml = id_xml + process_google_takeout(
                    os.path.join(os.curdir, dirty_data_dir, id, file), 
                    os.path.join(os.curdir, 'clean_data', id),
                )
            # Handle call log file
            elif 'calllogs_' in file and '.xml' in file:
                pass
            else:
                pass
        else:
            id_xml = id_xml + f'</{id}>'

            # Generate the XML document
            with open(os.path.join(os.curdir, 'clean_data', id, id + '.xml'), 'wb') as xml_file:
                # Pretty-print the XML document before writing
                xml_file.write(
                    xml.dom.minidom.parseString(id_xml).toprettyxml(encoding='utf-8')
                )
        
if __name__ == '__main__':
    main()
