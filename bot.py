
import discord
from bot_token import Token
import asyncio
from website_monitor import WebsiteMonitor

class GetToken:
  def __init__(self):
    self.secret = Token()  # Initialize self.secret correctly
    self.now_token = self.secret.get_token()  # Retrieve the token in the constructor

class ChannelID:
  def __init__(self):
    self.secret = Token()  # Initialize self.secret correctly
    self.now_channel = self.secret.get_channel()  # Retrieve the token in the constructor

class MyClient(discord.Client):
  def __init__(self, monitor,channel_id, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.monitor = monitor
    self.channel_id = channel_id

  async def on_ready(self):
    print(f'Logged on as {self.user}')
    print(f'Channel ID: {self.channel_id}')

    channel = self.get_channel(self.channel_id)
    if channel:
      await self.monitor.initialize_last_announcements(channel)
      await channel.send("Hello! The bot is now online.")

    # Start the task to check for updates
    self.loop.create_task(self.check_for_updates())

  async def on_message(self, message):
    if message.author == self.user:
      return

    if message.content.startswith('$news'):
      content = self.monitor.fetch_website_content()
      if content:
        new_announcements = self.monitor.parse_announcements(content)
        if new_announcements:
          response = "\n".join(new_announcements)
          await message.channel.send(f"Announcements:\n{response}")
        else:
          await message.channel.send("No new announcements.")

  async def check_for_updates(self):
    await self.wait_until_ready()
    while not self.is_closed():
      content = self.monitor.fetch_website_content()
      if content:
        new_announcements = self.monitor.check_for_new_announcements(content)
        if new_announcements:
          await self.send_update_notification(new_announcements)
      await asyncio.sleep(300)  # Wait for an hour before checking again

  async def send_update_notification(self, new_announcements):
    channel = self.get_channel(self.channel_id)
    if channel:
      for announcement in new_announcements:
        await channel.send(f"New announcement: {announcement}")


intents = discord.Intents.default()
intents.message_content = True

monitor = WebsiteMonitor("https://info.asep.gr/announcements-list")

# Create an instance of GetToken and retrieve the ChannelID
get_channel_instance = ChannelID()
channel_id = get_channel_instance.now_channel

client = MyClient(monitor=monitor, channel_id=channel_id, intents=intents)

# Create an instance of GetToken and retrieve the token
get_token_instance = GetToken()
client.run(get_token_instance.now_token)  # Use the token retrieved from the GetToken instance