# Score Notifier for Tongji University
Inspired by [Tongji-GPA](https://github.com/wlh320/Tongji-GPA).

## Usage
Supposing you've modified the info in the script and save it at `/home/rimo/tju-score.py`, the simple usage is just like `python /home/rimo/tju-score.py`.

**Attention**: DO NOT delete `updated.txt`, because it tracks the ID of updated courses.

You can make a schedule by executing `crontab -e` and adding a new line like:
```
0,30 8-22 * * * python /home/rimo/tju-score.py > /dev/null
```
which means it will run at 8:00, 8:30, 9:00, ..., 22:30 on every single day. Feel free to modify the time, though.

After saving the crontab, don't forget to restart the cron by `service cron restart` or something similar.

If you'd like to save the log as well, try this instead:
```
0,30 8-22 * * * date >> /home/rimo/tju-score.log
0,30 8-22 * * * python /home/rimo/tju-score.py >> /home/rimo/tju-score.log
```