# swe1-app

[![Build Status](https://app.travis-ci.com/EAdibi/swe1-app.svg?branch=main)](https://app.travis-ci.com/EAdibi/swe1-app)
[![Coverage Status](https://coveralls.io/repos/github/EAdibi/swe1-app/badge.svg?branch=main)](https://coveralls.io/github/EAdibi/swe1-app?branch=main)

Django polls app (Django tutorial) deployed on AWS Elastic Beanstalk.

Live app: http://swe1-app-env.eba-ckhe2s5j.us-east-2.elasticbeanstalk.com/polls/

## CI

Every push and pull request runs on Travis CI:

- `black --check .` for formatting
- `flake8 .` for linting (max line length 88, matching black)
- `coverage run manage.py test`, with the result reported to Coveralls

Pushes to `main` that pass all checks deploy to Elastic Beanstalk.

## Run checks locally

```bash
pip install -r requirements.txt black flake8 coverage
black --check .
flake8 .
coverage run manage.py test && coverage report
```
