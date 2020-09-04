"""
Classes to mange bindings for `function.json`.

"""


class BindingManager:
    """
    Manage bindings and function list to generate `function.json`
    
    Example:
        >>> binding_manager = BindingManager()
        >>> binding = Binding(handler_name="some_function", name="req", _type="httpTrigger", direction="in")
        >>> binding_manager.register_binding(binding)
    
    """
    def __init__(self):
        # manage function list including bindings
        self.function_app_list = []
        # manage bindings
        self.binding_list = []
    
    def register_binding(self, binding: Binding):
        self.bindig_list.append(binding)

    def register_function_app(self, handler_name: str):
        function_app_dict = self.get_binding_by_handler_name(handler_name)
        self.function_app_list.append(function_app_dict)

    def get_binding_by_handler_name(handler_name: str) -> dict:
        return {
            "function_name": handler_name,
            "function_json": {
                "scriptFile": "__init__.py",
                "entryPoint": handler_name,
                "bindings": [bind.to_dict() for bind in self.binding_list if
                             bind.handler_name == handler_name]
            }
        }

   
class Binding:
    """
    Mange simple one binding.
    
    """
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