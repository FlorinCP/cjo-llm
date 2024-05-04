from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time


def scrape_site(id_value=1):

    options = Options()
    options.headless = True
    driver = webdriver.Firefox(
        service=webdriver.firefox.service.Service(GeckoDriverManager().install()),
        options=options)

    inner_start_time = time.time()

    url = f'https://portal.just.ro/85/Lists/Jurisprudenta/DispForm.aspx?ID={id_value}&ContentTypeId=0x010017854362C029DA4EB7A0C1650A0C0651'
    driver.get(url)

    try:

        wait = WebDriverWait(driver, 1)

        titlu = wait.until(
            EC.presence_of_element_located((By.XPATH, "/html/body/form/div[8]/div/div[3]/div[2]/div[2]/div/div/div/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/div/span[1]/table[1]/tbody/tr[1]/td[2]"))
        )
        speta = wait.until(
            EC.presence_of_element_located((By.XPATH,
                                            "/html/body/form/div[8]/div/div[3]/div[2]/div[2]/div/div/div/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/div/span[1]/table[1]/tbody/tr[2]/td[2]"))
        )
        domeniu = wait.until(
            EC.presence_of_element_located((By.XPATH,
                                            "/html/body/form/div[8]/div/div[3]/div[2]/div[2]/div/div/div/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/div/span[1]/table[1]/tbody/tr[5]/td[2]"))
        )
        content = wait.until(
            EC.presence_of_element_located((By.XPATH,
                                            "/html/body/form/div[8]/div/div[3]/div[2]/div[2]/div/div/div/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/div/span[1]/table[1]/tbody/tr[6]/td[2]/div"))
        )

        response_object = {
            "titlu": titlu.text,
            "speta": speta.text,
            "domeniu": domeniu.text,
            "content": content.text
        }

        with open(f'response_objects_Sibiu_{id_value}.json', 'w') as json_file:
            json.dump(response_object, json_file)

    except Exception as e:
        print("Failed to find the element by full XPath:", e)

    driver.quit()
    inner_end_time = time.time()
    duration = inner_end_time - inner_start_time
    print("Process duration:", duration, "seconds")


start_time = time.time()

for i in range(1, 10):
    scrape_site(i)

end_time = time.time()
total_time = end_time - start_time
print("Total duration:", total_time, "seconds")

