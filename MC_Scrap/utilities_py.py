import os, shutil
from datetime import datetime, timezone

CURRENT_PATH = os.getcwd()
DOWNLOAD_DIR = os.path.join(CURRENT_PATH, 'WebsiteDownload')
ROOT_DIR = CURRENT_PATH #.replace('\\MC_Scrap', '')
DOWNLOAD_DIR_PRE_PATH = os.path.join(CURRENT_PATH, 'WebsiteDownloadInfo')
DOWNLOAD_DIR_PROCESSED = os.path.join(CURRENT_PATH, 'WebsiteDownloadProcessed')

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


def list_files(DIR=None):
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(DIR):
        for dir in d:
            for r1, d1, f1 in os.walk(os.path.join(r, dir)):
                for dir1 in f1:
                    files.append(os.path.join(r1, dir1))
    return files


def stocks_info_mapping(data_dict = {}, symbol=None):
    if symbol and len(data_dict):
        tags_mapping = {'Open Price': 'open_price', 'High Price': 'high_price', 'Low Price': 'low_price', 'Prev. Close': 'prev_close_price',
                        'Average Price': 'average_price', 'No. of Contracts Traded': 'no_of_contracts_traded', 'Turnover (Rs. In Lakhs)': 'turnover_in_lakhs',
                        'Market Lot': 'market_lot', 'Open Interest': 'open_interest', 'Open Interest Change': 'open_interest_change',
                        'Open Interest Change %': 'open_interest_change_percent', 'date': 'date'}
        temp = {}
        for key, value in data_dict.items():
            temp[tags_mapping[key]] = value.replace(",","")
        temp['date'] = datetime.strptime(temp['date'], '%Y:%m:%d %H:%M:%S').date()
        return temp


def move_file(SOURCE_DIR_FILE = None, DEST_DIR = None):
    for f in SOURCE_DIR_FILE:
        shutil.move(f, DEST_DIR)
    return


directory_create(DOWNLOAD_DIR)
directory_create(DOWNLOAD_DIR_PRE_PATH)
directory_create(DOWNLOAD_DIR_PROCESSED)