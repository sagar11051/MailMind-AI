import logging

def setup_logger(log_file: str = 'outputs/sample_output.log'):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s'
    )
    return logging.getLogger() 