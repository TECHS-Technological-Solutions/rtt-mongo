# rtt-mongo
A simple async framework built on Starlette and using mongodb oplog as
real time database.

### examples

Start server and client

#### server
```bash
$  pipenv run uvicorn rttmongo.examples.server:app --host 0.0.0.0 --port 8000
```

#### client
```bash
$  pipenv run python -m rttmongo.examples.client
```

Next enter into mongo and add sth to rtt-mongo.users