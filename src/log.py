import logging

# create logger
logger = logging.getLogger('log')
logger.setLevel(logging.INFO)

# create console handler and set level to debug
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)

# create formatter
formatter = logging.Formatter('{ "timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s" }')

# add formatter to ch
handler.setFormatter(formatter)

# add ch to logger
logger.addHandler(handler)
