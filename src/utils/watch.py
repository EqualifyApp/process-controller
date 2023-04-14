import logging


class FlaskOutputHandler(logging.Handler):
    def __init__(self, output_list):
        super().__init__()
        self.output_list = output_list

    def emit(self, record):
        msg = self.format(record)
        self.output_list.append(msg)



def setup_custom_logger(output_list=None):
    logger = logging.getLogger("A11y🪵")
    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(name)s - [%(levelname)s] - %(message)s')

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        if output_list is not None:
            fh = FlaskOutputHandler(output_list)
            fh.setLevel(logging.INFO)
            fh.setFormatter(formatter)
            logger.addHandler(fh)

    return logger


logger = setup_custom_logger()


def configure_logger(output_list=None):
    global logger
    logger = setup_custom_logger(output_list)
