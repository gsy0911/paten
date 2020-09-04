from inspect import signature
import json
import os
from typing import Union, Optional
from shutil import copyfile

from .error import ArgumentNameInvalidError


class Paten:

    def __init__(self, function_app_name: str):
        """
        set function-app-name for the Azure Functions.
        
        Args:
            function_app_name: A name for the Azure Functions to deploy.
        
        """
        self.function_app_name = function_app_name
        # manage function list including bindings
        self.function_info_list = []
        # manage bindings
        self.function_bind_list = []
        
    def _check_argument(function: callable, arg_name: str) -> None:
        """
        Check whether the `arg_name` in the parameter of the `function`.
        
        Args:
            function: function to check
            arg_name: argument name
        
        Raises:
            ArgumentNameInvalidError: When `arg_name` is not found in the paramater of the `function`
        
        """
        # check arguments
        sig = signature(function)
        if arg_name not in sig.parameters:
            raise ArgumentNameInvalidError(f"{arg_name} not in {function.__name__}")
        

    def http_trigger(self, name, methods: Union[list, str], route: str, auth_level: str = "function"):
        """
        Add HttpTrigger.
        
        Args:
            name: A name for the argument, usually `req`.
            methods: Accepted method name.
            route: Route name for the Function App.
            auth_level: Authentication level for the Function App, function, anonymous are acceptable.
        
        """
        def _wrapper(function):
            # check arguments
            self._check_argument(function=function, arg_name=name)

            self.function_bind_list.append({
                "function_name": str(function.__name__),
                "values": {
                    "authLevel": auth_level,
                    "type": "httpTrigger",
                    "direction": "in",
                    "name": name,
                    "route": route,
                    "methods": methods
                }
            })

            self.function_info_list.append({
                "function_name": str(function.__name__),
                "function_json": {
                    "scriptFile": "__init__.py",
                    "entryPoint": str(function.__name__),
                    "bindings": [d['values'] for d in self.function_bind_list if
                                 d['function_name'] == str(function.__name__)]
                }
            })
            return function

        return _wrapper

    def timer_trigger(self, name: str, schedule: str):
        """
        Add TimerTrigger.
        
        Args:
            name: A name for the argument, usually `timer`.
            schedule: The time when the Function App is invoked.
        
        """
        def _wrapper(function):
            # check arguments
            self._check_argument(function=function, arg_name=name)

            self.function_bind_list.append({
                "function_name": str(function.__name__),
                "values": {
                    "type": "timerTrigger",
                    "direction": "in",
                    "name": name,
                    "schedule": schedule
                }
            })

            self.function_info_list.append({
                "function_name": str(function.__name__),
                "function_json": {
                    "scriptFile": "__init__.py",
                    "entryPoint": str(function.__name__),
                    "bindings": [d['values'] for d in self.function_bind_list if
                                 d['function_name'] == str(function.__name__)]
                }
            })
            return function

        return _wrapper

    def queue_trigger(self, name: str, queue_name: str, connection: Optional[str] = None):
        """
        Add QueueTrigger.
        
        Args:
            name: A name for the argument, usually `msg`.
            queue_name: A name for the Queue Storage where the `msg` enqueue or dequeue.
            connection: A connection for the Queue Storage, by default `AzureWebJobsStorage`.
        
        """
        def _wrapper(function):
            # check arguments
            self._check_argument(function=function, arg_name=name)

            _connection = connection if connection is not None else "AzureWebJobsStorage"

            self.function_bind_list.append({
                "function_name": str(function.__name__),
                "values": {
                    "type": "queueTrigger",
                    "direction": "in",
                    "name": name,
                    "queueName": queue_name,
                    "connection": _connection
                }
            })

            self.function_info_list.append({
                "function_name": str(function.__name__),
                "function_json": {
                    "scriptFile": "__init__.py",
                    "entryPoint": str(function.__name__),
                    "bindings": [d['values'] for d in self.function_bind_list if
                                 d['function_name'] == str(function.__name__)]
                }
            })
            return function

        return _wrapper

    def blob_trigger(self, name: str, path: str, connection: Optional[str] = None):
        """
        Add BlobTrigger.
        
        Args:
            name: A name for the argument, usually `blob`.
            path: A path for the Blob Storage to invoke the Function App.
            connection: A connection for the Blob Storage, by default `AzureWebJobsStorage`.
        
        """
        def _wrapper(function):
            # check arguments
            self._check_argument(function=function, arg_name=name)

            _connection = connection if connection is not None else "AzureWebJobsStorage"

            self.function_bind_list.append({
                "function_name": str(function.__name__),
                "values": {
                    "name": name,
                    "type": "blobTrigger",
                    "direction": "in",
                    "path": path,
                    "connection": _connection
                }
            })

            self.function_info_list.append({
                "function_name": str(function.__name__),
                "function_json": {
                    "scriptFile": "__init__.py",
                    "entryPoint": str(function.__name__),
                    "bindings": [d['values'] for d in self.function_bind_list if
                                 d['function_name'] == str(function.__name__)]
                }
            })
            return function

        return _wrapper

    def out_http(self, name: Optional[str] = None):
        def _wrapper(function):
            _name = name if name is not None else "$return"

            self.function_bind_list.append({
                "function_name": str(function.__name__),
                "values": {
                    "type": "http",
                    "direction": "out",
                    "name": _name
                }
            })
            return function

        return _wrapper

    def out_queue(self, name: str, queue_name: str, connection: Optional[str] = None):
        def _wrapper(function):
            # check arguments
            self._check_argument(function=function, arg_name=name)

            _connection = connection if connection is not None else "AzureWebJobsStorage"

            self.function_bind_list.append({
                "function_name": str(function.__name__),
                "values": {
                    "type": "queue",
                    "direction": "out",
                    "name": name,
                    "queueName": queue_name,
                    "connection": _connection
                }
            })
            return function

        return _wrapper

    @staticmethod
    def _generate_function_json():
        return {
            "scriptFile": "__init__.py"
        }

    @staticmethod
    def _generate_host_json() -> dict:
        return {
            "version": "2.0",
            "extensionBundle": {
                "id": "Microsoft.Azure.Functions.ExtensionBundle",
                "version": "[1.*, 2.0.0)"
            }
        }

    @staticmethod
    def _generate_local_settings_json() -> dict:
        return {
            "IsEncrypted": False,
            "Values": {
                "AzureWebJobsStorage": "",
                "FUNCTIONS_WORKER_RUNTIME": "python"
            }
        }

    @staticmethod
    def _generate_proxies_json() -> dict:
        return {
            "$schema": "http://json.schemastore.org/proxies",
            "proxies": {}
        }

    def export(self):
        """
        Export files required for deploying Azure Functions.
        Export directory is `./.paten`.
        
        """
        file_parent_dir = f"./.paten"
        os.makedirs(file_parent_dir, exist_ok=True)

        # requirementsファイルの複製
        copyfile("requirements.txt", f"{file_parent_dir}/requirements.txt")

        with open(f"{file_parent_dir}/proxies.json", "w") as f:
            json.dump(self._generate_proxies_json(), f)

        with open(f"{file_parent_dir}/local.settings.json", "w") as f:
            json.dump(self._generate_local_settings_json(), f)

        with open(f"{file_parent_dir}/host.json", "w") as f:
            json.dump(self._generate_host_json(), f)

        for func in self.function_info_list:
            function_app_dir = f"{file_parent_dir}/{func['function_name']}"
            os.makedirs(function_app_dir, exist_ok=True)

            # function.jsonの取得と配置
            out: dict = func['function_json']
            with open(f'{function_app_dir}/function.json', 'w') as f:
                json.dump(out, f)

            # 関数ファイルの配置
            copyfile("app.py", f"{function_app_dir}/__init__.py")

    def plan(self) -> list:
        """
        Display function app to deploy.
        
        """
        output_list = ["app.py", "|"]
        for func in self.function_info_list:
            output_list.append(f"|-{func['function_name']}")
            for bindings in func['function_json']['bindings']:
                output_list.append(f"|  |-[{bindings['type']}] {bindings['name']}")
            output_list.append("|")

        return output_list
