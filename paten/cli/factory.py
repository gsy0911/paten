import importlib
import subprocess
import sys

from paten import Paten
from paten.error import AzureFunctionsCoreToolsNotFoundError


class CliFactory:

    def __init__(self, function_app_dir: str):
        self.function_app_dir = function_app_dir

    def load_paten_app(self) -> Paten:
        if self.function_app_dir not in sys.path:
            sys.path.insert(0, self.function_app_dir)
        try:
            app = importlib.import_module('app')
            paten_app = getattr(app, 'app')
        except SyntaxError as e:
            message = (
                          'Unable to import your app.py file:\n\n'
                          'File "%s", line %s\n'
                          '  %s\n'
                          'SyntaxError: %s'
                      ) % (getattr(e, 'filename'), e.lineno, e.text, e.msg)
            raise RuntimeError(message)
        return paten_app

    @staticmethod
    def _check_required_library_installed():
        """
        `which` command returns 127, if specified command not found.

        Returns:
            None

        Raises:
            AzureFunctionsCoreToolsNotFoundError
        """
        check_command = ["which", "func"]
        try:
            _ = subprocess.run(
                check_command,
                check=True,
                stderr=subprocess.PIPE
            )
        except subprocess.CalledProcessError:
            raise AzureFunctionsCoreToolsNotFoundError("`Azure Functions Core Tools` is not found.")
