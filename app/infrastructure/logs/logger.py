import logging

# For more information about the implementation check this blog post link
# https://medium.com/@roy-pstr/fastapi-server-errors-and-logs-take-back-control-696405437983
# This is other article to set the below configs:
# https://www.codeschat.com/article/145.html

# Disable uvicorn access logger
uvicorn_access = logging.getLogger("uvicorn.access")
uvicorn_access.disabled = True
# Create Logger
logger = logging.getLogger("uvicorn")
logger.setLevel(logging.getLevelName(logging.INFO))
# Set Server Configuration Format
fh = logging.FileHandler(filename='./server.log')
formatter = logging.Formatter(
    "%(asctime)s - %(module)s - %(funcName)s - line:%(lineno)s - %(levelname)s - %(message)s"  # noqa
)
fh.setFormatter(formatter)
logger.addHandler(fh)  # Exporting logs to a file
