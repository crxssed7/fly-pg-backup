cd "$(dirname "$0")";
CWD="$(pwd)"
echo $CWD
export FLY_API_TOKEN=<YOUR_FLY_API_TOKEN>
export PGPASSWORD=<YOUR_FLY_PG_PASSWORD>
export FLY_BIN=<YOUR_FLY_INSTALL_PATH>
export FLY_APP=<YOUR_FLY_PG_APP>
export FLY_DB_NAME=<YOUR_FLY_DB_NAME>
python3 cli.py fly-db-backup $FLY_APP $FLY_DB_NAME
