# Paten

Paten is a framework for azure functions written in Python. Paten provides:

* A command line tool for creating, building azure functions.
* A decorator based API integrated with in/out bindings.

## install

```shell script
$ pip install paten
```

## Quickstart

In your project directory, type below.
Directory {project_name} and example python scripts are created.

```shell script
$ paten new-project {project_name}
```

Then, modify `app.py`, like below.

```python
import azure.functions as func
from paten import Paten

app = Paten('{project_name}')


@app.http_trigger('req', methods=['GET'], route='/')
@app.out_http()
def example_http_function(req: func.HttpRequest) -> func.HttpResponse:
    name = req.params.get('name')
    
    # response
    return func.HttpResponse(name)

```

Finally, to generate files which are ready to deploy azure functions, type below in the directory `{project_name}`.
The files are generated in `./{project_name}/.paten`

```shell script
$ paten build
```
