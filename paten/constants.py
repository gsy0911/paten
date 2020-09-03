TEMPLATE_APP = """
from paten import Paten

app = Paten('%s')


@app.http_trigger('req', methods=['GET'], route='/')
@app.out_http()
def example_function(req):
    pass


@app.http_trigger('req', methods=['GET'], route='/')
@app.out_queue('arg_name', queue_name='example_queue')
def example_function(req, arg_name):
    pass
"""


GITIGNORE = """
.paten/*
"""