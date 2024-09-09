import logging

def setup_logging():
    logging.basicConfig(filename='app.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    
def log_action(action):
    logging.info(f"Action: {action}")
    
def log_error(error):
    logging.error(f"Error: {error}")
