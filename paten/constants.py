TEMPLATE_APP = """
from paten import Paten

app = Paten('%s')


@app.http_trigger('req', methods=['GET'], route='/')
@app.out_http()
def example_http_function(req):
    pass


@app.http_trigger('req', methods=['GET'], route='/')
@app.out_queue('arg_name', queue_name='example_queue')
def example_http_queue_function(req, arg_name):
    pass
"""


GITIGNORE = """
.paten/*
"""


WELCOME_PROMPT = r"""

 _____             _______  ______  _   _
|  __ \     /\    |__   __||  ____|| \ | |
| |__) |   /  \      | |   | |__   |  \| |
|  ___/   / /\ \     | |   |  __|  | . ` |
| |      / ____ \    | |   | |____ | |\  |
|_|     /_/    \_\   |_|   |______||_| \_|


Welcome PATEN.
Your function app `%s` is generated
"""