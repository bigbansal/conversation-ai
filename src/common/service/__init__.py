# Initialize the package
#Generate Code for - using importlib and pkgutil and importing logger, then imorting all the services in this folder
import importlib
import pkgutil
from src.common.util.log import LogHandler

# Initialize logger
logger = LogHandler().get_logger()

services = []

def import_all_services():
    paths = pkgutil.extend_path(list(__path__), __name__)
    for _, module, _ in pkgutil.iter_modules(paths, prefix= __name__ + "."):
        try:
            importlib.import_module(module)
            services.append(module)
            logger.info(f"Successfully imported module: {module}")
        except Exception as e:
            logger.error(f"Failed to import module: {module}. Error: {e}")
