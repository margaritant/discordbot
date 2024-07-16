# discordbot
# Discord Bot for Website Monitoring

This project is a Discord bot that monitors a specific website for new announcements and posts updates to a designated Discord channel. The bot uses Selenium to scrape the website and BeautifulSoup to parse the HTML content. The bot is built using the `discord.py` library.

## Features

- Monitors a website for new announcements
- Posts new announcements to a designated Discord channel
- Responds to the `$news` command to fetch and display current announcements

## Installation

### Prerequisites

- Python 3.7+
- Discord bot token
- Chrome browser

### Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/margaritant/discordbot.git
    cd discordbot
    ```

2. Install the required packages:

    ```bash
    pip install discord.py selenium webdriver-manager beautifulsoup4
    ```

3. Set up your Discord bot and obtain the bot token and channel ID. Create a `bot_token.py` file with the following content:

    ```python
    class Token:
    def __init__(self):
        self.token =   '123451234512345'  # your bot token
        self.channel = 123451234512345  # your channel ID
    def get_token(self):
        return self.token

    def get_channel(self):
        return self.channel
    ```

4. Open the `website_monitor.py` file and ensure that the `headers` and `links` selectors match the structure of the website you want to monitor. Specifically, the following lines:

    ```python
    headers = soup.find_all('div', class_='views-field views-field-title')
    links = soup.find_all('div', class_='views-field views-field-view-node')
    ```

   These class names (`views-field views-field-title` and `views-field views-field-view-node`) are specific to the current structure of the monitored website. If the website's structure changes, or if you are monitoring a different website, you will need to update these selectors accordingly.

5. Run the bot:

    ```bash
    python bot.py
    ```

## Usage

- Start the bot and it will monitor the specified website for new announcements.
- Use the `$news` command in the Discord channel to fetch and display current announcements.

## License

This project is licensed under the MIT License.
