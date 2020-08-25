from typing import Union, Optional


class Paten:

    def __init__(self, function_app_name: str):
        self.function_app_name = function_app_name
        # manage function list including bindings
        self.function_info_list = []
        # manage bindings
        self.function_bind_list = []

    def http_trigger(self, name, methods: Union[list, str], route: str, auth_level: str = "function"):
        def _wrapper(function):
            self.function_bind_list.append({
                "function_name": function.__name__,
                "values": {
                    "authLevel": auth_level,
                    "type": "httpTrigger",
                    "direction": "out",
                    "name": name,
                    "route": route,
                    "methods": methods
                }
            })

            self.function_info_list.append({
                "scriptFile": "__init__.py",
                "bindings": [d['values'] for d in self.function_bind_list if d['function_name'] == function.__name__]
            })
            return function
        return _wrapper

    def out_http(self, name: Optional[str] = None):
        def _wrapper(function):
            _name = name if name is not None else "$return"

            self.function_bind_list.append({
                "function_name": function.__name__,
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
                "function_name": function.__name__,
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
