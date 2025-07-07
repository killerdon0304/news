import requests

access_token = 'EAAIHrIveBCMBOz5q6vd8MrtkXZArkMyAs7vZA4ZB3xiHGXwwRRqaJSlPkArZA3W4nOKyh3SldLeO47C5ZC0HE2SZCSDX9BeEYTcVEpMa3sUvUc0rRfPxRBsuDRSPOJUEgJZBVKfYZCtKZCPmCSDWsdgPGqoSHz4skVG2I2xrbFoy5le7kKw1q3UcZASlFY5kVEea4TeB3g6UtZA63N4GDdgg9l2pbkZD'

url = 'https://graph.facebook.com/debug_token'
params = {
    'input_token': access_token,
    'access_token': access_token
}

response = requests.get(url, params=params)

if response.status_code == 200:
    print(response.json()['data']['scopes'])
else:
    print('त्रुटि:', response.status_code)