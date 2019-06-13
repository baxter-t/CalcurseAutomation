# CalcurseAutomation
A simple script to parse and send your calcurse appointments and todo tasks for today.

## Installation

Before starting ensure `crontab` is installed. For instructions visit [here](https://www.servernoobs.com/how-to-install-cron-crond-crontab/).

### Steps:
1. Download sendSchedule.py and take note of it's path.
2. Alter lines 21, 22, 25, 86 and 119. Comments on these lines detail what should be changed.
3. Run `crontab -e` to open the crontab editor.
4. Enter the following line to have the email sent at 9am each day: `0  9  *  *  *  path/to/python3 path/to/sendSchedule.py`.
5. Done!
