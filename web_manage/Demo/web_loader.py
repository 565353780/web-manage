import platform
from web_manage.Module.web_loader import WebLoader


def demo():
    driver_path = None
    if platform.system().lower() == 'windows':
        driver_path = '../Chrome/115/chromedriver.exe'
    elif platform.system().lower() == 'linux':
        driver_path = '/usr/local/bin/chromedriver'
    url_key = '1'
    teacher = '刘利刚'
    page_num = 6

    web_loader = WebLoader(driver_path, url_key)
    web_loader.autoRun(teacher, page_num)
    return True
