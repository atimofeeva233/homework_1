import logging


def setup_utils_logger():
    utils_logger = logging.getLogger('utils')
    utils_logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler('logs/utils.log', 'w')
    file_formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s: %(message)s')
    file_handler.setFormatter(file_formatter)
    utils_logger.addHandler(file_handler)

    return utils_logger
