# pg-health-check

Postgres HTTP health check endpoint for Consul wirtten in Python.

## Usage

```
./pghealthcheck.py [-h] -U USER [-P PASSWORD] -H HOST [-p PORT] [-w WSPORT]
```

Arguments:

```
  -h, --help            show this help message and exit
  -U USER, --user USER  Username to connect to the database.
  -P PASSWORD, --password PASSWORD
                        User password to connect to the database (optional).
  -H HOST, --host HOST  Postgres server or directory for the Unix-domain socket. Default Unix-domain socket directory.
  -p PORT, --port PORT  TCP port or local Unix-domain socket file extension on which the Postgres server is listening for connections. Default 5432
  -w WSPORT, --wsport WSPORT
                        TCP port where the web server is listening for connections. Default 5000.
```
