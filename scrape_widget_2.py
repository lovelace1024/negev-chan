from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import time
from datetime import date, timedelta
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# URL of the page
ulpanlink = "https://ulpan.com/category/yddh-old/"
#yesterday = (date.today()-timedelta(1)).strftime('%B %d')
#before1 = (date.today()-timedelta(2)).strftime('%B %d')
#before2 = (date.today()-timedelta(3)).strftime('%B %d')
#print(yesterday)
class Ulpan:
    def __init__(self):
        self.service = Service("/snap/bin/geckodriver") # Replace with your Geckodriver path
        self.options = Options()
        self.options.add_argument("--headless") # Run in headless mode (no browser UI)
        self.driver = webdriver.Firefox(service=self.service, options=self.options)
    def ulpandaily1(self,url):
        try:
            # Open the URL in the browser
            self.driver.get(url)
            try:
                articles_container = self.driver.find_element(By.CLASS_NAME, "elementor-widget-container.hebrew-text")
                latestdate = articles_container.find_elements(
                    By.XPATH, "//span[@class='elementor-post-date']")[0]
                # Assume 'element' is the element you've already located
                article_element = latestdate.find_element(By.XPATH, "./ancestor::article")
        #        print("Found Article:", article_element.get_attribute("outerHTML"))
                # Locate the <a> tag within the <h3> tag of class "elementor-post__title"
                a_tag = article_element.find_element(
                    By.XPATH, ".//h3[@class='elementor-post__title']/a")
                # Retrieve the href attribute of the <a> tag
                a_href = a_tag.get_attribute("href")
                print("Link URL:", a_href)
            except Exception as e:
                print("Error retrieving latest articles:", e)
        except Exception as e:
            print("An error occurred:", e)
        finally:
            self.driver.quit()
            return a_href
    def ulpandaily(self,a_href):
        try:
            self.driver.get(a_href)
            block = self.driver.find_element(By.DATA_ELEMENTOR_TYPE, "single-post")
            print("Block:", block)
        finally:
            self.driver.quit()
u = Ulpan()
u.ulpandaily("https://ulpan.com/how-to-say-black-in-hebrew/")
