# POLITICO-API

## Progress
[![Coverage Status](https://coveralls.io/repos/github/Paul-weqe/POLITICO-API/badge.svg?branch=develop)](https://coveralls.io/github/Paul-weqe/POLITICO-API?branch=develop)

[![Build Status](https://travis-ci.com/Paul-weqe/POLITICO-API.svg?branch=develop)](https://travis-ci.com/Paul-weqe/POLITICO-API)

<a href="https://codeclimate.com/github/Paul-weqe/POLITICO-API/maintainability"><img src="https://api.codeclimate.com/v1/badges/ad5d7bcf66ab6b32b852/maintainability" /></a>


## Setup guide

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

