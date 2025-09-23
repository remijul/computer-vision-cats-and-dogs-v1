#!/bin/bash

python -m venv baseenv
source baseenv/bin/activate
pip install --upgrade pip
pip install -r requirements/base.txt
