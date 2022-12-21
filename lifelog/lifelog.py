#! /usr/bin/env python

from src import android_activity, call_log
 
import tarfile
import errno, sys, os

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
                if tarfile.is_tarfile(dirty_file_path):
                    source_file = tarfile.open(name=dirty_file_path, mode='r', encoding='utf-8')
                    android_activity.generate_csv(source_file, clean_file_path)
            # Handle call log file
            elif 'calllogs_' in file and '.xml' in file:
                call_log.generate_csv(dirty_file_path, clean_file_path)
            else:
                pass
        
if __name__ == '__main__':
    main()
