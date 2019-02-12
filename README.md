# POLITICO-API

## Progress
[![Coverage Status](https://coveralls.io/repos/github/Paul-weqe/POLITICO-API/badge.svg?branch=develop)](https://coveralls.io/github/Paul-weqe/POLITICO-API?branch=develop)

[![Build Status](https://travis-ci.com/Paul-weqe/POLITICO-API.svg?branch=develop)](https://travis-ci.com/Paul-weqe/POLITICO-API)

<a href="https://codeclimate.com/github/Paul-weqe/POLITICO-API/maintainability"><img src="https://api.codeclimate.com/v1/badges/ad5d7bcf66ab6b32b852/maintainability" /></a>

## <a href="https://app.swaggerhub.com/apis-docs/POL231/POLITIC-API/1.0.0">SWAGGER API DOCUMENTATION</a>

## What is politico?

Politico is a government-like voting system. It allows for candidates to vie under political parties and allows for regular users to vote. 

This API allows for exposure of the data held by POLITICO. This reference guide shows you how you can be able to access the data inside the POLITICO system online. <a href="https://paul-weqe.github.io/POLITICO/UI/index.html">Our frontend</a>

## Setup guide

### creating the virtual environment
 ```
 virtualenv venv
 ```

### activating the virtual environment

While on linux
```
source venv/bin/activate
```

on Windows:
```
venv\Scripts\activate
```


### installing the requirements

All of the requirements will be installed through the requirements.txt file. Run the following command to install:

```
pip install -r requirements.txt
```

### running the application

To run the flask application, write the following command:

```
python run.py
```

### running tests on the application

The tests are contained in the *politico_api/tests/* folder. The tests can be run using the following command:

```
pytest politico/tests/
```

### getting coverage of the tests

To get the coverage of the tests, run:

```
pytest --cov=.
```

## where the API is hosted


http://paul-politico-api.herokuapp.com

| route | method | function | JSON fields |
| --- | --- | --- | --- |
| /api/v1/offices/ | POST | create a new office | "office_name": string, "office_type": string |
| /api/v1/offices/ | GET | get all offices | No json fields |
| /api/v1/offices/officeID | GET | gets a single office information | no json fields |
| /api/v1/parties/ | GET | gets all parties | no json field |
| /api/v1/parties/partyID/partyName | PATCH | edits a single party with ID partyID and sets its name to partyName | no json field |
| /parties/partyID | DELETE | deletes the party with ID partyID | no json field |
| /parties/partyID | GET | gets a single party with ID partyID | no json field |
| /parties/ | POST | creates a party | "party_name": string, "party_name": string, "party_hq_address": string, "party_logo_url": str, "party_motto": str, "party_members": int |
