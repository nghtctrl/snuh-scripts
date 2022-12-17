#! /usr/bin/env python

# This script should be run in the dirty_data directory:
# ..
#  └─ dirty_data
#     ├─ research_id_0001
#     ├─ research_id_0002
#     └─ ...

import sys, os

import tarfile

import xml.etree.ElementTree as ET
import xml.dom.minidom as MD

def clean_google_takeout(source, destination, xml_root):
    if tarfile.is_tarfile(source):
        source_file = tarfile.open(name=source, mode='r')

        # For keeping track of available data
        status = {}

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

                # Android activity data is likely unavailable
                status['android_activity_data'] = '0'
        
        status['android_activity_data'] = '1'

        xml_root.append(ET.Element('google_takeout_data', status))

def main():
    # Create a directory for cleaned data
    try:
        os.mkdir(os.path.join(os.pardir, 'clean_data'))
        print('Created clean_data directory.')
    except FileExistsError:
        # Ignore if the directory already exists
        pass

    # Get a list of research identifiers
    r_id = os.listdir(os.path.join(os.pardir, 'dirty_data'))

    # Exclude this script from the list of research identifiers
    script_name = str(sys.argv[0])
    r_id.remove(script_name[2:] if './' in script_name else script_name)

    for id in r_id:
        # Create a subdirectory for each research identifiers
        try:
            os.mkdir(os.path.join(os.pardir, 'clean_data', id))
            print('Created subdirectory for ' + id + ' inside clean_data.')
        except FileExistsError:
            # Ignore if the directory already exists
            pass

        # Get a list of files contained in the current research identifier
        files = os.listdir(os.path.join(os.pardir, 'dirty_data', id))

        # Create an XML document for keeping track of avaliable data
        root = ET.Element(id)

        for file in files:
            # Handle Google Takeout files
            if 'takeout-' in file and ('.tgz' in file or '.gtar' in file):
                clean_google_takeout(
                    os.path.join(os.pardir, 'dirty_data', id, file), 
                    os.path.join(os.pardir, 'clean_data', id),
                    root
                )
            # Handle call log file
            elif 'calllogs_' in file and '.xml' in file:
                pass
            else:
                pass
        else:
            # Generate the XML document
            with open(os.path.join(os.pardir, 'clean_data', id, id + '.xml'), 'wb') as xml_file:
                # Pretty-print the XML document before writing
                xml_file.write(
                    MD.parseString(ET.tostring(root)).toprettyxml(encoding='utf-8')
                )
        
# Usage: python clean.py
# Alternative usage for Linux: ./clean.py
if __name__ == '__main__':
    main()
