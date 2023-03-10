import os
import time
from pathlib import Path
from datetime import datetime

import sh
import typer
from rich import print as rprint


# create a typer app
app = typer.Typer()


@app.command()
def fly_db_connect(app_name="app-name", bg: int = 0):
    """
    Connect to the database
    :param app_name: The name of the app
    :param bg: Run in the background (0-false, 1-true)
    """
    rprint(f"[green]Connecting to {app_name}, {bg}")
    _bg = bg == 1
    rprint(f"[green]Connecting to the database: Running in the background: {_bg}")
    try:
        return sh.fly("proxy", "5433:5432", app=app_name, _out=rprint, _bg=_bg)
    except sh.ErrorReturnCode as e:
        rprint(e)


@app.command()
def fly_db_backup(
    app_name: str,
    password=None,
    db_name="tankobon",
    port=5433,
    user="postgres",
    host="localhost",
):
    """Connect to fly.io and backup the database"""
    password = password or os.getenv("TANKOBON_PG_PASSWORD")
    db_connection = None
    try:
        rprint("[green] Backing up the database")
        # start timer
        start = time.time()
        db_connection = fly_db_connect(app_name=app_name, bg=1)
        # wait for the connection here
        time.sleep(3)
        
        filename = f"tankobon-backup-{datetime.now().timestamp()}.sql"
        rprint(f"[green]Backing up the database to {filename}, please wait...")
        process = sh.pg_dump(
            "-h",
            host,
            "-p",
            port,
            "-U",
            user,
            "-f",
            filename,
            db_name,
            _out=rprint,
            _in=password,
            _bg=False,
        )
        rprint(process)

        # end timer
        end = time.time()
        rprint(f"[green] Total runtime of the program is [red] {end - start}")
        db_connection.terminate()

    except sh.ErrorReturnCode as e:
        rprint(e)
        if db_connection:
            db_connection.terminate()

if __name__ == "__main__":
    app()