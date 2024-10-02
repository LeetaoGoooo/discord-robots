from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
import datetime
from pathlib import Path
import time

work_dir = Path.cwd()


def html2img_with_selector(html_str:str, id_selector:str) -> Path:
    chrome_options = webdriver.FirefoxOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--disable-setuid-sandbox")
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=chrome_options)

    file_name = int(datetime.datetime.now().timestamp())
    file_path = work_dir.joinpath(f'{file_name}.html')
    screen_shoot_path = work_dir.joinpath(f'{file_name}.png')
    try:
        with open(file_path,'w+', encoding='utf-8') as f:
            f.write(html_str)
        driver.get(f"file://{file_path}")
        time.sleep(6) # TODO 优化
        element = driver.find_element(By.ID, id_selector)
        element.screenshot(screen_shoot_path.name)
        # file_path.unlink(missing_ok=True)
        return screen_shoot_path
    except Exception as e:
        print(f"Screenshot failed: {e}")
        return
    finally:
        driver.quit()