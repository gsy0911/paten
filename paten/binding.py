"""
Classes to mange bindings for `function.json`.

"""


class BindigsRegisteration:
    def __init__(self):
        self.bindigs_list = []
    
    def register(self, bindings: Bindings):
        self.bindigs_list.append(bindings)
        
    def get_by_handler_name(handler_name: str) -> dict:
        return {
            "function_name": handler_name,
            "function_json": {
                "scriptFile": "__init__.py",
                "entryPoint": handler_name,
                "bindings": [bind.to_dict() for bind in self.bindings_list if
                             bind.handler_name == handler_name]
            }
        }

   
class Bindings:
    def __init__(self, handler_name: str, name: str, _type: str, direction: str, **kwargs):
        self.handler_name = handler_name
        self.name = name
        self.type = _type
        self.direction = direction
        self.kwargs = kwargs
    
    def to_dict(self):
        bind_info = {
            "name": self.name,
            "type": self.type,
            "direction": self.direction
        }
        bind_info.update(kwargs)
        
        return bind_info