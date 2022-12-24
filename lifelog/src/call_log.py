import xmltodict
import csv
import os

import date

def _get_call_type(type: str) -> str:
    # Call types referenced from: https://developer.android.com/reference/android/provider/CallLog.Calls
    call_types = {
        '1': 'incoming',
        '2': 'outgoing',
        '3': 'missed',
        '4': 'voicemail',
        '5': 'rejected',
        '6': 'blocked',
        '7': 'answered-externally'
    }
    
    return call_types[type]

def generate_csv(source: str, destination: str) -> None:
    # Load the XML file
    with open(source, 'r', encoding='utf-8') as call_log_file:
        call_log_xml = call_log_file.read()
        call_log = xmltodict.parse(call_log_xml)

        # Get the date from the most recent call
        tmp = call_log['alllogs']['log'][0]['@date']
        recent_date = date.epoch_to_iso(tmp[:10] + '.' + tmp[10:])

        # Process relevant data then export it into a CSV file
        with open(os.path.join(destination, 'call-log.csv'), 'w', newline='', encoding='utf-8') as call_log_csv:
            csv_writer = csv.writer(call_log_csv)
            csv_writer.writerow(['Number', 'Date', 'CallType', 'CallDuration'])
            for log in call_log['alllogs']['log']:
                tmp = log['@date']
                current_date = date.epoch_to_iso(tmp[:10] + '.' + tmp[10:])
                if date.within_six_months(recent_date, current_date):
                    csv_writer.writerow([
                        str(log['@number']),
                        date.iso_to_date(current_date),
                        _get_call_type(log['@type']),
                        log['@dur'],
                    ])
                else:
                    break
