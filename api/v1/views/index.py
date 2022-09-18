#!/usr/bin/python3
"""Index to check status"""

from flask import Flask
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def status():
    """Return status: OK"""
    return ("status": "OK")
