import datetime
import logging
import os


def get_current_time() -> datetime:
    delta = datetime.timedelta(hours=5, minutes=0)
    return datetime.datetime.now(datetime.timezone.utc) + delta


def write_file_requests(data):
    """ The function writes a new sequence number to the file 'customer.numbers.txt' """
    date = get_current_time()
    requests = open('requests.txt', 'a')
    requests.write(f'\nNew request from {date}:\n')
    for line in data:
        requests.write(f'\n{line}\n')
    requests.write(f'\n----------------------------\n')
    requests.close()


def clear_file_requests():
    os.system(r'nul>requests.txt')
    logging.info("The file 'requests.txt' is cleared")