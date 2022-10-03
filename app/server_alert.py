import requests
import logging
import json
from datetime import datetime
from traceback import format_exc
import pytz

# Module Settings
url_to_error_server = ''
api_token = ''
# The project ID set on the server
project_id = ''
# Link to documentation (optional)
link_to_doc = ''
# Link to git (optional)
link_to_git = ''
# Link to the developer (optional)
link_to_portainer = '.'
# Default error status
error_status_default = 3

# Module constants
header = {'Authorization': 'Token ' + api_token,
          'Content-Type': 'application/json'}
logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)