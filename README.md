# esch2022
Data collection for Esch 2022 event

For automation of the data upload:
```
crontab -e
```
```
* * * * * $PYTHON_PATH$ $FILE_PATH$/main.py >> $FILE_PATH$/cron.log 2>&1
```
Each star stands for "minute hour day month year", so in this case it is every minute of every hour of every day of every month of every year.
Possibilty to use anacron if the computer shuts down.
