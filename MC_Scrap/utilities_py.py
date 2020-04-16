import os
from datetime import datetime, timezone

CURRENT_PATH = os.getcwd()
DOWNLOAD_DIR = os.path.join(CURRENT_PATH, 'WebsiteDownload')
ROOT_DIR = CURRENT_PATH #.replace('\\MC_Scrap', '')


def directory_create(DIR):
    """
    Creates Directory/Folder
    :param DIR: Name of the directory that needs to be created if it doesn't exists
    :return: None
    """
    if not os.path.exists(DIR):
        os.mkdir(DIR)
        print("Creating the directory", DIR)


def file_create(DIR, content):
    """
    Creates file at a specified path
    :param DIR: Path at which the file needs to be created(full path)
    :param content: content that needs to be written to the file
    :return: None
    """
    with open(DIR, 'w', encoding='utf-8') as f:
        f.write(content)


def remove_special_characters(data):
    """
    Removes special characters
    :param data: string/text from which the characters need to be removed
    :return: data without certain characters
    """
    return data.replace(' ', '').replace('/', '').replace("'", "").replace('\\', '').replace('//', '').replace(',', '')


def url_sanitizer(url):
    """
    Removes certain characters from URL
    :param url: URL to be cleaned
    :return: url with the characters replaced
    """
    return url.replace('https://', '').replace('/', '__').replace('\\', '')


def current_date_time(time_zone = None, format = "%Y_%m_%d %H_%M_%S"):
    """
    Returns DateTime
    :param time_zone: timezone
    :param format: date and time
    :return: date-time
    """
    if time_zone == 'utc':
        return datetime.now(timezone.utc).strftime(format)
    return datetime.now().strftime(format)


def current_date(time_zone = None, format = "%Y_%m_%d"):
    """
    Returns Date
    :param time_zone: timezone
    :param format: date
    :return: date
    """
    if time_zone == 'utc':
        return datetime.now(timezone.utc).strftime(format)
    return datetime.now().strftime(format)


def current_time(time_zone = None, format = "%H_%M_%S"):
    """
    Returns Time
    :param time_zone: timezone
    :param format: time
    :return: time
    """
    if time_zone == 'utc':
        return datetime.now(timezone.utc).strftime(format)
    return datetime.now().strftime(format)


directory_create(DOWNLOAD_DIR)