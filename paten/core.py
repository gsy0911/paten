import json
import os
from typing import Union, Optional


class Paten:

    def __init__(self, function_app_name: str, requirements: Optional[list] = None):
        self.function_app_name = function_app_name
        # manage function list including bindings
        self.function_info_list = []
        # manage bindings
        self.function_bind_list = []
        # requirements
        self.requirements = requirements

    def http_trigger(self, name, methods: Union[list, str], route: str, auth_level: str = "function"):
        def _wrapper(function):
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
            _connection = connection if connection is not None else "AzureWebJobsStorage"

            self.function_bind_list.append({
                "function_name": str(function.__name__),
                "values": {
                    "type": "queue",
                    "direction": "out",
                    "name": name,
                    "queueName": queue_name,
                    "connection": "AzureWebJobsStorage"
                }
            })
            return function
        return _wrapper

    @staticmethod
    def _generate_function_json():
        return {
            "scriptFile": "__init__.py"
        }

    def _generate_requirements_txt(self) -> list:
        if self.requirements is None:
            return []
        return self.requirements

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
        with open("./out/proxies.json", "w") as f:
            json.dump(self._generate_proxies_json(), f)

        with open("./out/local.settings.json", "w") as f:
            json.dump(self._generate_local_settings_json(), f)

        with open("./out/host.json", "w") as f:
            json.dump(self._generate_host_json(), f)

        with open("./out/requirements.txt", mode='w') as f:
            f.writelines('\n'.join(self._generate_requirements_txt()))

        for func in self.function_info_list:
            output_dir = f"./out/{func['function_name']}"
            os.makedirs(output_dir, exist_ok=True)
            out: dict = func['function_json']
            with open(f'{output_dir}/function.json', 'w') as f:
                json.dump(out, f)
