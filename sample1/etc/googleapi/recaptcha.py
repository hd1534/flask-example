import requests


def recaptcha(response):
    res = requests.post(
              'https://www.google.com/recaptcha/api/siteverify',
              data={
                'secret': 'HERE YOUR SECRET KEY',
                'response': response})

    return res.json()
