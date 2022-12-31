import xmltodict
import csv
import os

import date

def _get_call_type(type: str) -> str:
    # Call types referenced from: https://developer.android.com/reference/android/provider/CallLog.Calls
    call_types = {
        '1': 'INCOMING',
        '2': 'OUTGOING',
        '3': 'MISSED',
        '4': 'VOICEMAIL',
        '5': 'REJECTED',
        '6': 'BLOCKED',
        '7': 'ANSWERED EXTERNALLY'
    }
    
    return call_types[type]

def generate_csv(source: str, destination: str) -> None:
    # Load the XML file
    with open(source, 'r', encoding='utf-8') as call_log_file:
        call_log_xml = call_log_file.read()
        call_log = xmltodict.parse(call_log_xml)

        # Get the date from the most recent call
        recent_date = date.epoch_to_iso(int(call_log['alllogs']['log'][0]['@date']) / 10.0E+2)

        # Process relevant data then export it into a CSV file
        with open(os.path.join(destination, 'call-log.csv'), 'w', newline='', encoding='utf-8') as call_log_csv:
            csv_writer = csv.writer(call_log_csv, quoting=csv.QUOTE_ALL)
            csv_writer.writerow(['Number', 'Date', 'CallType', 'CallDuration'])
            for log in call_log['alllogs']['log']:
                current_date = date.epoch_to_iso(float(log['@date']) / 10.0E+2)
                if date.within_six_months(recent_date, current_date):
                    csv_writer.writerow([
                        log['@number'],
                        date.iso_to_date(current_date),
                        _get_call_type(log['@type']),
                        log['@dur'],
                    ])
                else:
                    break
