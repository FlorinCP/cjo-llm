import json
import time
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape_site(id_value, binary_path):
    inner_start_time = time.time()

    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')

    try:
        driver = webdriver.Firefox(service=Service(binary_path), options=options)
    except:
        driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)

    url = f'https://portal.just.ro/2/Lists/Jurisprudenta/DispForm.aspx?ID={id_value}&ContentTypeId=0x010017854362C029DA4EB7A0C1650A0C0651'
    driver.get(url)

    try:
        wait = WebDriverWait(driver, 2)

        titlu = wait.until(EC.presence_of_element_located((By.XPATH,
                                                           "/html/body/form/div[8]/div/div[3]/div[2]/div[2]/div/div/div/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/div/span[1]/table[1]/tbody/tr[1]/td[2]")))
        speta = wait.until(EC.presence_of_element_located((By.XPATH,
                                                           "/html/body/form/div[8]/div/div[3]/div[2]/div[2]/div/div/div/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/div/span[1]/table[1]/tbody/tr[2]/td[2]")))
        domeniu = wait.until(EC.presence_of_element_located((By.XPATH,
                                                             "/html/body/form/div[8]/div/div[3]/div[2]/div[2]/div/div/div/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/div/span[1]/table[1]/tbody/tr[5]/td[2]")))
        content = wait.until(EC.presence_of_element_located((By.XPATH,
                                                             "/html/body/form/div[8]/div/div[3]/div[2]/div[2]/div/div/div/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/div/span[1]/table[1]/tbody/tr[6]/td[2]/div")))

        response_object = {
            "titlu": titlu.text,
            "speta": speta.text,
            "domeniu": domeniu.text,
            "content": content.text
        }

        return response_object

    except Exception as e:
        print(f"Error scraping page {id_value}:", e)
        return None

    finally:
        driver.quit()
        inner_end_time = time.time()
        print(f"Process duration for page {id_value}:", inner_end_time - inner_start_time, "seconds")


def main():
    start_time = time.time()
    metadata = GeckoDriverManager().driver_cache.get_metadata()
    binary_paths = [item["binary_path"] for item in metadata.values()]
    binary_path = binary_paths[0]

    with ThreadPoolExecutor(max_workers=16) as executor:
        results = executor.map(lambda id_value: scrape_site(id_value, binary_path), range(1, 1000))

    response_objects = [result for result in results if result is not None]

    with open("../data/scraped_data_Bucuresti_3.json", "w") as f:
        json.dump(response_objects, f, indent=4)

    end_time = time.time()
    total_time = end_time - start_time
    print("Total time for main:", total_time, "seconds")


if __name__ == "__main__":
    main()
