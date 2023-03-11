# fly-pg-backup

This script runs a Postgres backup for your fly.io Postgres app. 90% of the code is taken from [advantch's blog post](https://www.advantch.com/blog/automate-postgres-database-backups-on-fly-dot-io/) and is tweaked so that it runs as a CRON job.

Checkout `run.example.sh`, you will need a few environment variables. After you have set up your own `run.sh` you can add a CRON job like this using `crontab -e`:

```
0 12 * * * path/to/your/run.sh
```

After that, the script will run at 12 noon everyday (or you can choose your own schedule) and the backup will be placed in the same directory as the script.

## Notes

* We need to use a `run.sh` script in the CRON schedule (instead of running the Python script directly) because we do not have access to system wide environment variables (CRON jobs run in their own environment). So we first need to set the variables via a shell script and then execute the main Python script. The Python script should still work outside of a CRON environment.

* The script only creates one backup. That is, it won't keep previous backups of your database. When it creates a new backup it deletes the old backup, so there is only ever one backup. Maybe in the future I'll add different options but this is fine for now for my use cases.

* The [original blog post](https://www.advantch.com/blog/automate-postgres-database-backups-on-fly-dot-io/) goes even further and uploads the backups to an AWS S3 instance. Checkout the post if you want to do this for your own setup.
