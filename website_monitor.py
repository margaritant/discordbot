from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

class WebsiteMonitor:
    def __init__(self, url):
        self.url = url
        self.last_announcements = set()  # To store the last fetched announcements
        self.driver = self.setup_driver()

    def setup_driver(self):
        options = Options()
        options.headless = True  # Run in headless mode
        service = ChromeService(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        return driver

    def fetch_website_content(self):
        try:
            self.driver.get(self.url)
            return self.driver.page_source
        except Exception as e:
            print(f"Error fetching {self.url}: {e}")
        return None

    def parse_announcements(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        announcements = set()
        headers = soup.find_all('div', class_='views-field views-field-title')
        links = soup.find_all('div', class_='views-field views-field-view-node')

        # Assuming headers and links are in the same order
        for header, link_div in zip(headers, links):
            header_text = header.get_text(strip=True)
            link_tag = link_div.find('a')
            if link_tag:
                link = link_tag['href']
                full_link = link if link.startswith('http') else f'{self.url}/{link}'
                announcements.add((header_text, full_link))
        return announcements

    def check_for_new_announcements(self, content):
        current_announcements = self.parse_announcements(content)
        new_announcements = current_announcements - self.last_announcements
        self.last_announcements = current_announcements
        return new_announcements

    async def initialize_last_announcements(self, channel):
        """Fetch previous messages in the channel and initialize last_announcements."""
        async for message in channel.history(limit=100):  # Adjust limit as needed
            if message.author == channel.guild.me:  # Only consider messages sent by the bot
                content = message.content.replace("New announcement: ", "").strip()
                if "(" in content and ")" in content:
                    text, link = content.rsplit(" (", 1)
                    link = link[:-1]  # Remove the trailing ')'
                    self.last_announcements.add((text.strip(), link.strip()))

    def __del__(self):
        self.driver.quit()  # Ensure the driver quits when the object is deleted
