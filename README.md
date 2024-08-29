# Doc Bill
A simple hospital billing system for small sized clinic/hospital for managing doctors, patients, bills and dashboard for bill analytics (developed in flask)

## Development

This app has been developed in flask using python.

## Deployment

### For Unix/MacOS

Clone the project

```bash
  git clone https://github.com/sundepkrv/docbill.git
```

Go to the project directory

```bash
  cd docbill
```

Create a virtual environment and install requirements

```bash
  python3 -m venv venv
  source ./venv/bin/activate
  pip install -r requirements.txt
```

Create database by running ```python3 createdb.py```. Run ```python3 createdb.py --nodata``` to create database without dummy data

Start the server for local deployment

```bash
  python3 docbill.py
```

Using gunicorn for production deployment

```bash
  gunicorn --workers:2 docbill:app
```

### For Windows

Clone the project

```bash
  git clone https://github.com/sundepkrv/docbill.git
```

Go to the project directory

```bash
  cd docbill
```

Create a virtual environment and install requirements

```bash
  python -m venv venv
  .\venv\Scripts\activate
  pip install -r requirements.txt
```

Create database by running ```python3 createdb.py```. Run ```python3 createdb.py --nodata``` to create database without dummy data

Start the server for local deployment

```bash
  python3 docbill.py
```

Using gunicorn for production deployment

```bash
  gunicorn --workers:2 docbill:app
```

### Running behind a proxy network
If you are trying to install the dependencies behind a proxy network, run the following - 

```bash
  pip --proxy:http://xxx.xxx.xxx.xxx:yyyy install -r requirements.txt
```

## Test Credentials

Username: ```clinic```
Password: ```clinic```

## Tech Stack

**Client:** HTML, Bootstrap, Datatables, Javascript, jQuery, ApexCharts

**Server:** Flask, SQLite3

## Errors

The app may run into errors and you can debug the same using references from error traceback calls.

## Feedback and contact

[@sundeepkrv](https://github.com/sundeepkrv)
