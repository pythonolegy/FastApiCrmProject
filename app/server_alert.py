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


def send_alert_message(error_msg, error_status=error_status_default):
    request_data = {
        "project_id": project_id,
        "error_description": error_msg,
        "date_time": str(datetime.now(tz=pytz.timezone(''))),
        "error_status": error_status,

        # Optional fields
        "trace": format_exc(),
        "docs_link": link_to_doc,
        "git_link": link_to_git,
        "portainer_link": link_to_portainer
    }
    request_data_json = json.dumps(request_data)
    response = requests.post(url_to_error_server, data=request_data_json, headers=header)

    return response
