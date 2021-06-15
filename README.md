# Esch2022
Traffic road data collection for Esch 2022 event

This program has been built for downloading a xml file giving road traffic information
in Luxembourg. Then relevant features can be extracted into a xlsx file for post-treatment.

# Deployment on Ubuntu 20.04.2 LTS, 64-bit, Python 3.8.5 

Prerequisite: Installation of Python 3 environment:
To download the requirements
```
pip3 install -r requirements.txt
```
Then to run the programm:
```
python3 main.py
```

The tasks can be run automatically through crontab:
```
crontab -e
```
```
* * * * * $PYTHON_PATH$ $FILE_PATH$/main.py >> $FILE_PATH$/cron.log 2>&1
```
Each star stands for "minute hour day month year", so in this case it is every minute of every hour of every day of every month of every year.
Possibilty to use anacron if the computer shuts down.

Contact: ziemnono@gmail.com

Funding: This work was supported by the European Union’s Horizon 2020 research and innovation programme under the Marie Sklodowska-Curie grant agreement No. 764644.
