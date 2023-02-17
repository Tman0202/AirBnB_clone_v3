#!/usr/bin/python3
"""Testing file
"""
import json
import requests

if __name__ == "__main__":
    """ POST /api/v1/users/
    """
    r = requests.post("http://0.0.0.0:5000/api/v1/users/", data=json.dumps({ 'email': "f@f.com", 'first_name': "fnf", 'last_name': "lnf" }), headers={ 'Content-Type': "application/json" })
    print(r.status_code)
