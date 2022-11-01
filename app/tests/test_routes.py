from flask import Flask

from app.handlers.routes import configure_routes


def test_base_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/'

    response = client.get(url)

    assert response.status_code == 200


def test_predict_route():

    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()

    # predict has no inputs
    url = '/predict'
    response = client.get(url)
    assert response.status_code == 400 
    assert b"Please provide valid input" in response.data

    # has all valid inputs 
    validUrl = '/predict?G1=18&G2=19&studytime=2&failures=3'
    response = client.get(validUrl)
    assert response.status_code == 200 
    assert b"Applicant is likely to succeed" in response.json['returnMsg'] or b"Applicant is unlikely to succeed" in response.json['returnMsg']
    assert b"Variables G1, G2, studytime, and failures used to predict." in response.json['variablesUsed']
    
    # missing input
    badUrl = '/predict?G1=18&G2=19&studytime=2'
    response = client.get(badUrl)
    assert response.status_code == 400 
    assert b"Please provide valid input" in response.data

    # inputs out of range
    rangeUrl = '/predict?G1=100&G2=19&studytime=2&failure=20'
    response = client.get(rangeUrl)
    assert response.status_code == 400 
    assert b"Please provide valid input" in response.data

    # misspelled input
    misspelledUrl = '/predict?G1=100&G2=19&studtime=2&failure=1'
    response = client.get(misspelledUrl)
    assert response.status_code == 400 
    assert b"Please provide valid input" in response.data

    # additional parameters given
    additionalUrl = '/predict?G1=18&G2=19&studytime=2&failures=3&age=19'
    response = client.get(additionalUrl)
    assert response.status_code == 200 
    assert b"Applicant is likely to succeed" in response.json['returnMsg'] or b"Applicant is unlikely to succeed" in response.json['returnMsg']
    assert b"Variables G1, G2, studytime, and failures used to predict." in response.json['variablesUsed']

    # inputs given in different order
    diffOrderUrl = '/predict?G1=18&G2=19&failures=3&studytime=2'
    response = client.get(validUrl)
    assert response.status_code == 200 
    assert b"Applicant is likely to succeed" in response.json['returnMsg'] or b"Applicant is unlikely to succeed" in response.json['returnMsg']
    assert b"Variables G1, G2, studytime, and failures used to predict." in response.json['variablesUsed']
