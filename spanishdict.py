from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrape_widget_1 import Scraper
wotdlink = "https://www.spanishdict.com/wordoftheday"
base = "https://www.spanishdict.com/"
class SpanishDictScraper(Scraper):
    def favicon(self):
        try:
            self.driver.get(base)
            # Locate the <link> tag for the favicon
            favicon_link = self.driver.find_element(By.XPATH, "//link[@rel='icon']")  # For <link rel="icon">
            favicon_href = favicon_link.get_attribute("href")
            print("Favicon Href:", favicon_href)

        except Exception as e:
            print("Error retrieving favicon:", e)

    def daily(self): #, day
    #    day = kwargs.get('day',None)
        try:
            # Open the URL in the browser
            self.driver.get(wotdlink)
            # Wait for JavaScript to load the content
            time.sleep(3)
#            if not day == None:
#                calendar = self.driver.find_element(By.CLASS_NAME, "wotd-widget-header-date.hasDatepicker")
#                calendar.click()
                # Locate a specific date in the calendar
#                target_date = self.driver.find_element(
#                    By.XPATH, f"//td[@data-handler='selectDay']/a[text()='{day}']" # and @data-month='10' and @data-year='2024'
#                )
#                target_date.click()
            # Locate the div with text content "TODAY"
            today_div = self.driver.find_element(By.XPATH, "//div[normalize-space(text())='TODAY']")
            container = today_div.find_element(By.XPATH, "./parent::div")
            img_container = container.find_element(By.XPATH, "./parent::div")
            span_elements = container.find_elements(By.TAG_NAME, "span")
            image = img_container.find_element(By.TAG_NAME, "img")
            self.image_src = image.get_attribute("src")
            self.eng = image.get_attribute("alt")
            a_tag = container.find_element(
                By.XPATH, ".//a[contains(@href, '/translate/')]")
            self.a_href = a_tag.get_attribute("href")
            self.title = a_tag.text
            self.heb_list.append(span_elements[0].text)
            self.eng_list.append(span_elements[1].text)
            print("Word of the day:", self.title)
            print("Translation:", self.eng)
            print(self.heb_list, self.eng_list)
        finally:
            print("quitting driver 1")
            self.driver.quit()
#            scraper2 = SpanishDictScraper()
#            scraper2.scrape_daily(a_href)
        return self.title, self.eng, self.heb_list, self.eng_list, self.image_src, self.a_href
    def scrape_daily(self, a_href):
        try:
            print("Link: "+a_href)
            self.driver.get(a_href)
            # Retrieve image source
            try:
                translation = self.driver.find_element(By.ID, "quickdef1-es")
                word = translation.find_element(
                    By.XPATH, ".//a")
                self.eng = word.text
            except Exception as e:
                print("Error retrieving translation:", e)
            try:
                text_span = self.driver.find_element(By.CLASS_NAME, "wotd-widget-sentence-main-space-text")
                self.text_content = text_span.text
                print("Text Content:", self.text_content)
            except Exception as e:
                print("Error retrieving text:", e)
            try:
                # Locate the <a> tag with the target class
                audio_link = self.driver.find_element(By.CLASS_NAME, "wotd-widget-sentence-main-space-sound")
                # Extract the href attribute
                self.audio_href = audio_link.get_attribute("href")
                print("Audio File Href:", self.audio_href)
            except Exception as e:
                print("Error retrieving audio file href:", e)
            try:
                # Locate the parent div with the unique class
                parent_div = self.driver.find_element(By.CLASS_NAME, "wotd-widget-container-up-inner")

                # Locate the target nested div within the parent
                if language == "Hebrew":
                    title_r_div = parent_div.find_element(By.CLASS_NAME, "wotd-widget-sentence-quizmode-space-text.big.romanization")
                    title_v_div = parent_div.find_element(By.CLASS_NAME, "wotd-widget-sentence-quizmode-space-text.vowelled")
                    self.title_r_text = title_r_div.text
                    self.title_v_text = title_v_div.text
                    print("Title romanization Text:", self.title_r_text)
                    print("Title vowelled Text:", self.title_v_text)
                d_div = parent_div.find_element(By.CLASS_NAME, "wotd-widget-sentence-quizmode-space-text.big.english")
                article_div = parent_div.find_element(By.CLASS_NAME, "wotd-widget-sentence-quizmode-space-text.noun")
                # Retrieve the text content of the target div
                self.d_text = d_div.text
                self.article_text = article_div.text
                print("Definition:", self.d_text)
                print("Article of Speech:", self.article_text)
            except Exception as e:
                print("Error retrieving something in title div:", e)
            try:
                # Locate the parent div with the class "jspContainer"
                jsp_container = self.driver.find_element(By.CLASS_NAME, "jspContainer")

                # Find all <span> elements with the target class inside the "jspContainer" div
                if language == "Hebrew":
                    rom_elements = jsp_container.find_elements(By.CLASS_NAME, "wotd-widget-sentence-quizmode-space-text.big.romanization")
                    vow_elements = jsp_container.find_elements(By.CLASS_NAME, "wotd-widget-sentence-quizmode-space-text.vowelled")
                    self.rom_list = [span.get_attribute("innerText") for span in rom_elements]
                    self.vow_list = [span.get_attribute("innerText") for span in vow_elements]
                eng_elements = jsp_container.find_elements(By.CLASS_NAME, "wotd-widget-sentence-quizmode-space-text.big.english")
                l_elements = jsp_container.find_elements(By.CLASS_NAME, "wotd-widget-sentence-main-space-text")
                # Extract the text content from each <span> and store in a list
                self.l_list = [span.get_attribute("innerText") for span in l_elements]
                self.eng_list = [span.get_attribute("innerText") for span in eng_elements]
    #            for idx, span in enumerate(span_elements):
    #                print(f"Span {idx + 1} - Visible: {span.is_displayed()}, Text: {span.get_attribute('innerText')}")
                print(f"Examples - {language}:", self.l_list)
                print("Examples - English:", self.eng_list)
            except Exception as e:
                print("Error retrieving examples:", e)

        except Exception as e:
            print("An error occurred:", e)
s = SpanishDictScraper()
#s.favicon()
#s.daily()
