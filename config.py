import logging

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(name)s - %(filename)s:%(lineno)d - "
    "%(funcName)s() - %(message)s"
)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)

logging.basicConfig(level=logging.DEBUG, handlers=[handler])
