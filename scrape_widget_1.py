from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# URL of the widget page
hpwidgetlink = "https://www.innovativelanguage.com/widgets/wotd/embed.php?language=Hebrew&type=large&bg=url%28/widgets/wotd/skin/images/large/Mountains.png%29%20no-repeat%200%200&content=%23000&header=%2388A1B6&highlight=%2388A1B6&opacity=.25&scrollbg=%23323E47&sound=%239A958C&text=%23353B1A&quiz=N"
podlink1 = "https://www.innovativelanguage.com/widgets/wotd/embed.php?language="
podlink2 = "&type=large&bg=url%28/widgets/wotd/skin/images/large/Mountains.png%29%20no-repeat%200%200&content=%23000&header=%2388A1B6&highlight=%2388A1B6&opacity=.25&scrollbg=%23323E47&sound=%239A958C&text=%23353B1A&quiz=N"
# Set up Selenium with Firefox and Geckodriver
#options = Options()
#options.add_argument("--headless")
#service = Service("/snap/bin/geckodriver")
class Scraper:
    def __init__(self):
        self.service = Service("/snap/bin/geckodriver") # Replace with your Geckodriver path
        self.options = Options()
        self.options.add_argument("--headless") # Run in headless mode (no browser UI)
        self.driver = webdriver.Firefox(service=self.service, options=self.options)

        self.image_src = ""
        self.text_content = ""
        self.title_r_text = ""
        self.title_v_text = ""
        self.d_text = ""
        self.article_text = ""
        self.heb_list = []
        self.rom_list = []
        self.eng_list = []
        self.vow_list = []
    def scrape_link(self, language, day):
    #    day = kwargs.get('day',None)
        try:
            # Open the URL in the browser
            self.driver.get(podlink1+language+podlink2)
            # Wait for JavaScript to load the content
            time.sleep(3)
            if not day == None:
                calendar = self.driver.find_element(By.CLASS_NAME, "wotd-widget-header-date.hasDatepicker")
                calendar.click()
                # Locate a specific date in the calendar
                target_date = self.driver.find_element(
                    By.XPATH, f"//td[@data-handler='selectDay']/a[text()='{day}']" # and @data-month='10' and @data-year='2024'
                )
                target_date.click()

                # Wait for the page or content to load (adjust selector to ensure the data is ready)
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "wotd-widget-sentence-main-space-text"))
                )
            # Retrieve image source
            try:
                image_div = self.driver.find_element(By.CLASS_NAME, "wotd-widget-container-images-space")
                image = image_div.find_element(By.TAG_NAME, "img")
                self.image_src = image.get_attribute("src")
                print("Image Source:", self.image_src)
            except Exception as e:
                print("Error retrieving image:", e)

            # Retrieve text content
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
        if language == "Hebrew":
            return self.image_src, self.text_content, self.title_r_text, self.title_v_text, self.d_text, self.article_text, self.l_list, self.rom_list, self.eng_list, self.vow_list
        else:
            return self.image_src, self.text_content, self.d_text, self.article_text, self.l_list, self.eng_list
        def close(self):
            # Close the browser
            self.driver.quit()
#scrape_link(hpwidgetlink,day=5)
