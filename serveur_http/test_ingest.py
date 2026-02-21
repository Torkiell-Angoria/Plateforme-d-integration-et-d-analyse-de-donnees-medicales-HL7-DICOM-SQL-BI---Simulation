import requests

payload = {
    "metadata": {
        "messageControlId": "MSG00001",
        "messageType": "ADT",
        "triggerEvent": "A01",
        "sourceSystem": "SPIROMETER",
        "messageTimestamp": "202602111200"
    },
    "patient": {
        "externalId": "12345",
        "firstName": "John",
        "lastName": "Doe",
        "birthDate": "19960101",
        "gender": "M"
    },
    "exam": {
        "type": "spirometry",
        "performedAt": "202602111200",
        "observations": [
            {
                "code": "FEV1",
                "label": "Forced Expiratory Volume",
                "value": 2.9,
                "unit": "L",
                "referenceRange": "2.5-3.5",
                "interpretation": "N"
            }
        ]
    }
}

r = requests.post("http://127.0.0.1:8000/ingest", json=payload)
print("Status:", r.status_code)
print("Response:", r.text)


