from logging import INFO, basicConfig

from .env_config import LOG_FILENAME

basicConfig(
    filename=LOG_FILENAME,
    format="[%(levelname)8s AT %(asctime)s IN %(filename)s:%(lineno)d] %(message)s",
    level=INFO,
)
