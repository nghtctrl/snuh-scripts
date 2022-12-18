# Python Scripts for [SNUH Biomedical Research Institute](http://en.bri.snuh.org/pub/_/singlecont/view.do)

## Documentation

This documentation assumes that you have a Python interpreter installed and properly configured in your system.

+ [Processing Lifelog Data](#lifelog)
+ [Concatenating PRISM WAVE Files](#prism)

## <a name='lifelog'>Processing Lifelog Data</a>

This is a cross-platform script used for processing lifelog data that has been collected for a machine learning research project at SNUH. 
The research defines lifelog data as a retroactive smartphone data that are extracted from 
[Google Takeout](https://takeout.google.com), 
[Samsung Privacy](https://privacy.samsung.com/), 
[Call Blocker & Call Logs Backup](https://play.google.com/store/apps/details?id=com.idea.backup.calllogs),
and possibly more. 
This scripts helps to automate the processing and cleaning of data that are collected from the aforementioned 
services so that they may be suitable for data analysis and modeling.

Raw lifelog data (also known as "dirty data") should be collected in a directory with the following structure:

```
dirty_data
├── research_id_0001
│   ├── takeout-XXXXXXXXXXXXXXXX-XXX.tgz
│   ├── calllogs_XXXXXXXXXXXXXX.xml
│   ...
│   └── ...
├── research_id_0002
│   ├── takeout-XXXXXXXXXXXXXXXX-XXX.tgz
│   ├── calllogs_XXXXXXXXXXXXXX.xml
│   ...
│   └── ...
├── research_id_0003
│   ├── takeout-XXXXXXXXXXXXXXXX-XXX.tgz
│   ├── calllogs_XXXXXXXXXXXXXX.xml
│   ...
│   └── ...
...
└── ...
```

For your convenience, please name the "dirty data" folder as `dirty_data`.

This script will generate a new directory with the following structure and contents:

```
clean_data
├── research_id_0001
│   ├── research_id_0001.xml
│   ├── google-lifelog-data
│   │   ├── android-activity-data
│   │   │   └── android_activity.csv
│   ├── call-log-data
│   │   └── call_log.csv
│   ...
│   └── ...
...
└── ...
```
### How to Use This Script
1. [Download](https://github.com/nghtctrl/snuh-scripts/archive/refs/heads/main.zip) this repository, then extract it in an appropriate location.
2. Copy and paste the `dirty_data` folder into the `lifelog` folder.
6. Install the dependencies by running `python -m pip install -r requirements.txt`
7. Run the script by running `python lifelog.py`
