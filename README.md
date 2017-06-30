# Score Notifier for Tongji University
Inspired by [Tongji-GPA](https://github.com/wlh320/Tongji-GPA).

## Usage
Supposing you've modified the script and save it at `/home/rimo/tju-score.py`, simply run it with `python /home/rimo/tju-score.py`. If it failed, install the necessary components.

**Attention**: Do NOT delete `tju-score.txt`, because it tracks the ID of updated courses.

Add a schedule by `crontab -e` and add a new line with:
```
0,30 8-22 * * * python /home/rimo/tju-score.py > /dev/null
```
which means it will run at 8:00, 8:30, 9:00, ..., 22:30 on every single day. Feel free to modify the time.

After saving the crontab, remember to restart the cron by `service cron restart` or something like that.

If you'd like to save the log file, try this in your crontab instead:
```
0,30 8-22 * * * date >> /home/rimo/tju-score.log
0,30 8-22 * * * python /home/rimo/tju-score.py >> /home/rimo/tju-score.log
```