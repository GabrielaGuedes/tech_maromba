#!/bin/bash
export LANG=C.UTF-8
export LC_ALL=C.UTF-8
export FLASK_APP=endpoints.py
flask run --host=0.0.0.0 &