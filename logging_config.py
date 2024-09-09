import logging
import os

def setup_logging():
    # Create 'logs' directory if it doesn't exist
    logs_dir = os.path.join(os.getcwd(), 'logs')
    os.makedirs(logs_dir, exist_ok=True)

    # Define the log file path
    log_file_path = os.path.join(logs_dir, 'system.log')

    # Set up logging configuration
    logging.basicConfig(
        filename=log_file_path,
        filemode='a',  # Append to the log file
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    # Log that the logging system is set up
    logging.info("Logging system initialized.")

def log_action(message):
    # Log informational messages
    logging.info(message)

def log_error(message):
    # Log error messages
    logging.error(message)
