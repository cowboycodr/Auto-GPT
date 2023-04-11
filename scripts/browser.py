from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions

from llm_utils import create_chat_completion

class Browser:
    def __init__(self):
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--disable-gpu")  # Disable GPU

        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(driver=self.driver, timeout=10)

    @property
    def url(self):
        return self.driver.current_url
    
    @property
    def title(self):
        return self.driver.title

    def back(self):
        self.driver.back()

    def open(self, url):
        self.driver.get(url)

        return "Opened URL: " + url

    def click(self, selector):
        element = self.wait_for_element(selector)
        element.click()

        return "Clicked element: " + selector

    def fill_input(self, selector, text):
        element = self.wait_for_element(selector)
        element.clear()
        element.send_keys(text)

        return "Filled input: " + selector

    def _summarize_text(self, chunks):
        characters = 0
        for chunk in chunks:
            characters += len(chunk)

        print(f'Summarizing {characters} characters...')

        summaries = []
        for i, chunk in enumerate(chunks):
            print(f"Summarizing chunk ({i + 1}/{len(chunks)})")

            message = [{
                "role": "user",
                "content": f"\"\"\"{chunk}\"\"\" Summarize the text above"
            }]

            summary = create_chat_completion(
                messages=message,
                max_tokens=300,
                model="gpt-3.5-turbo"
            )

            summaries.append(summary)

        summary = '\n'.join(summaries)

        message = [{
            "role": "user",
            "content": f"\"\"\"{summary}\"\"\" Summarize the text above"
        }]

        summary = create_chat_completion(
            messages=message,
            max_tokens=300,
            model="gpt-3.5-turbo"
        )

        return summary

    def get_content(self):
        # Extract text content from web page
        body_element = self.driver.find_element(By.TAG_NAME, 'body')
        text = body_element.text

        # Split text into sections if they are more than 1 space apart
        sections = text.split('  ')

        # Split each section into chunks of 4096 characters or less
        chunks = []
        for section in sections:
            section_chunks = [section[i:i+4096] for i in range(0, len(section), 4096)]
            chunks.extend(section_chunks)

        return self._summarize_text(chunks)

    def get_interactive_elements(self):
        interactive_elements = []
        # Retrieve buttons, textareas, and input elements
        elements = self.driver.find_elements(By.XPATH, "//button | //textarea | //input | //a")
        for element in elements:
            tag_name = element.tag_name
            attributes = ''
            # Retrieve specific attributes for buttons, textareas, and input elements
            if tag_name == 'button':
                attributes += f' type="{element.get_attribute("type")}"'
            elif tag_name == 'textarea':
                attributes += f' rows="{element.get_attribute("rows")}" cols="{element.get_attribute("cols")}"'
            elif tag_name == 'input':
                attributes += f' type="{element.get_attribute("type")}" value="{element.get_attribute("value")}"'
            elif tag_name == 'a':
                attributes += f' href="{element.get_attribute("href")}"'
            content = element.text
            interactive_elements.append(f'<{tag_name}{attributes}>{content}</{tag_name}>')
        return interactive_elements

    def wait_for_element(self, selector, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
        )

    def close(self):
        self.driver.quit()


if __name__ == '__main__':
    browser = Browser()
    browser.open('https://github.com/cowboycodr?tab=repositories')
    contnet = browser.get_content()

    print(contnet)

    browser.close()