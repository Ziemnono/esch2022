# esch2022
Data collection for Esch 2022 event

For automation of the data upload:
```
crontab -e
```
```
* * * * * $PYTHON_PATH$ $FILE_PATH$/main.py >> $FILE_PATH$/cron.log 2>&1
```
