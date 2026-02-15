import logging


def setup_masks_logger():
    masks_logger = logging.getLogger('masks')
    masks_logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler('logs/masks.log', 'w')
    file_formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s: %(message)s')
    file_handler.setFormatter(file_formatter)
    masks_logger.addHandler(file_handler)

    return masks_logger
