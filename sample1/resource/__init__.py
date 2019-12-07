from sample1 import app
from flask_restplus import Api, Resource

from sample1.loader import resource_load

from flask import url_for
from flask_cors import CORS

app.config['ERROR_INCLUDE_MESSAGE'] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 30  # 캐시 컨트롤 시간을 30초로

CORS(app)


@property
def specs_url(self):
    return url_for(self.endpoint('specs'), _external=True, _scheme='https')


# Only for production mode
if app.debug is False:
    Api.specs_url = specs_url

api = Api(
    app,
    title='sample1 API',
    version='1.0',
    description="sample1 Api Document System"
)


__import__('sample1.handler')

resource_load(
    'sample1'
)
