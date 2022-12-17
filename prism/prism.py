from natsort import natsorted
import soundfile as sf
import numpy as np
import zipfile
import sys, os
import wave
import shutil

for i in range(1, len(sys.argv)):
    if zipfile.is_zipfile(sys.argv[i]):
        with zipfile.ZipFile(sys.argv[i], 'r') as zip_file:
            zip_file.extractall('./temp')

        tmp_dir = os.listdir('temp/' + sys.argv[i][:-4])        

        dir_dict = {}
        
        for tmp_file in tmp_dir:
            study_id = tmp_file[:10]
            if study_id not in dir_dict:
                dir_dict[study_id] = {'base':[], '2m':[], '4m':[], '8m':[], '12m':[]}

        study_id_list = natsorted(list(dir_dict.keys()))

        for tmp_file in tmp_dir:
            for study_id in study_id_list:
                if (study_id + ' base_') in tmp_file:
                    dir_dict[study_id]['base'].append(tmp_file)
                elif (study_id + ' 2m_') in tmp_file:
                    dir_dict[study_id]['2m'].append(tmp_file)
                elif (study_id + ' 4m_') in tmp_file:
                    dir_dict[study_id]['4m'].append(tmp_file)
                elif (study_id + ' 8m_') in tmp_file:
                    dir_dict[study_id]['8m'].append(tmp_file)
                elif (study_id + ' 12m_') in tmp_file:
                    dir_dict[study_id]['12m'].append(tmp_file)

        os.mkdir('./' + sys.argv[i][:-4])

        log_file = open('./' + sys.argv[i][:-4] + '/log.txt', 'w')
        log_file.write(sys.argv[i] + ' was extracted and analyzed.\n')

        for study_id in study_id_list:
            dir_dict[study_id]['base'] = natsorted(dir_dict[study_id]['base'])
            dir_dict[study_id]['2m'] = natsorted(dir_dict[study_id]['2m'])
            dir_dict[study_id]['4m'] = natsorted(dir_dict[study_id]['4m'])
            dir_dict[study_id]['8m'] = natsorted(dir_dict[study_id]['8m'])
            dir_dict[study_id]['12m'] = natsorted(dir_dict[study_id]['12m'])

        time_intervals = ['base', '2m', '4m', '8m', '12m']

        for study_id in study_id_list:
            wave_data = []
            for time in time_intervals:
                wave_files = dir_dict[study_id][time]
                if len(wave_files):
                    for wf in wave_files:
                        wave_file_path = './temp/' + sys.argv[i][:-4] + '/' + wf
                        wave_data.append(sf.read(wave_file_path, dtype='float32'))
                    waves_to_be_concatenated = []
                    for wave in wave_data:
                        waves_to_be_concatenated.append(wave[0])
                    concatenated_wave_data = np.concatenate(waves_to_be_concatenated)
                    concatenated_wave_path = './' + sys.argv[i][:-4] + '/' + study_id + ' ' + time + '.wav'
                    sf.write(concatenated_wave_path, concatenated_wave_data, 22050)
                else:
                    log_file.write('WAVE files for ' + study_id + ' ' + time + ' does not exist.\n')

        shutil.rmtree('./temp')
        log_file.close()
