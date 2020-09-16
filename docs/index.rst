.. paten documentation master file, created by
   sphinx-quickstart on Sat Jun 27 16:18:45 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Paten
=====

code status

.. image:: https://github.com/gsy0911/paten/workflows/pytest/badge.svg
    :target: https://github.com/gsy0911/paten/actions?query=workflow%3Apytest

.. image:: https://codecov.io/gh/gsy0911/paten/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/gsy0911/paten
    :alt: codecov

.. image:: https://img.shields.io/lgtm/grade/python/g/gsy0911/paten.svg?logo=lgtm&logoWidth=18
    :target: https://lgtm.com/projects/g/gsy0911/paten/context:python
    :alt: lgtm

.. image:: https://readthedocs.org/projects/paten/badge/?version=latest
   :target: https://paten.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

package status

.. image:: https://img.shields.io/badge/python-3.7|3.8-blue.svg
   :target: https://www.python.org/downloads/release/python-377/

.. image:: https://img.shields.io/pypi/v/paten.svg
    :target: https://pypi.org/project/paten/

.. image:: https://pepy.tech/badge/paten
   :target: https://pepy.tech/project/paten

**Paten** is a framework for azure functions written in Python.

Paten provides:

* A command line tool for creating, building, deploying azure functions.
* A decorator based API integrated with in/out bindings.

Installation
============

**Paten** can be installed from pip.

.. code-block:: shell

   pip install paten

In addition, ``Azure CLI`` and ``Azure Functions Core Tools`` are required.
See below to install the libraries.

* `Azure CLI <https://docs.microsoft.com/ja-jp/cli/azure/install-azure-cli?view=azure-cli-latest>`_
* `Azure Functions Core Tools <https://docs.microsoft.com/ja-jp/azure/azure-functions/functions-run-local?tabs=macos%2Cpython%2Cbash>`_


Usage
=====

In your project directory, type below.

.. code-block:: shell

   $ paten new-app {function_app_name}


Directory ``{function_app_name}`` and example python scripts like below are created.


.. code-block:: python

   import azure.functions as func
   from paten import Paten

   app = Paten('{function_app_name}')


   @app.http_trigger('req', methods=['GET'], route='/')
   @app.out_http()
   def example_http_function(req: func.HttpRequest) -> func.HttpResponse:
       name = req.params.get('name')

       # response
       return func.HttpResponse(name)


Before deploying to azure functions, you can test your functions on local with the command below.


.. code-block:: shell

   $ paten local

Finally, to deploy to azure functions, type below in the directory ``{function_app_name}``.
The files are generated in ``./{function_app_name}/.paten`` and your function app is deployed to azure.


.. code-block:: shell

   $ paten deploy


The User Guid
=============

Tutorial
---------

To get started, it is recommended to follow the document below.

.. toctree::
   :maxdepth: 2

   sources/tutorial


API Documentation
-----------------

.. toctree::
   :maxdepth: 2

   sources/api

.. toctree::
   :maxdepth: 1

   sources/release_history

GitHub
------

**Paten** repository is `here <https://github.com/gsy0911/paten>`_.

References
----------

* `Azure CLI <https://docs.microsoft.com/ja-jp/cli/azure/install-azure-cli?view=azure-cli-latest>`_
* `Azure Functions Core Tools <https://docs.microsoft.com/ja-jp/azure/azure-functions/functions-run-local?tabs=macos%2Cpython%2Cbash>`_

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
