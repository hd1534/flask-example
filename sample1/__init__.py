from flask import Flask

app = Flask(__name__)
app.url_map.strict_slashes = False

__import__('sample1.database')
__import__('sample1.resource')
__import__('sample1.upload')
__import__('sample1.jwt_auth')
__import__('sample1.handler')
