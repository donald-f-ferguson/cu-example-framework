# Columbia University Courses Framework

## Overview

See the dffframework/dffframework/README.md for information
about the framework.

This is just the top-level readme for the GIT project.

## Installation

This installs from a local [devpi](https://devpi.net/docs/devpi/devpi/latest/+doc/index.html) server.

My local install commands are:
- One time: ```pip install -U devpi-web devpi-client```
- This assumes that the devpi server is installed and running. My local project
for the server is ```dev_pi```
  - ```devpi login testuser --password=123```
  - ```cd dffframework```
  - ```devpi index -c bases=root/pypi```
  - ```devpi use testuser/dev```
  - ```devpi use```

