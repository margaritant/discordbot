
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
    self.secret = Token()  # # Initialize the Token instance
    self.now_channel = self.secret.get_channel()  # # Retrieve the channel ID

class MyClient(discord.Client):
  def __init__(self, monitor,channel_id, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.monitor = monitor   # WebsiteMonitor instance to monitor website changes
    self.channel_id = channel_id  # Discord channel ID to send messages to

  async def on_ready(self):
    # This method is called when the bot is ready and connected to Discord
    print(f'Logged on as {self.user}')
    print(f'Channel ID: {self.channel_id}')

    # Get the channel object using the channel ID
    channel = self.get_channel(self.channel_id)
    if channel:
      await self.monitor.initialize_last_announcements(channel) # Initialize announcements from previous messages
      await channel.send("Hello! The bot is now online.")  # Send a greeting message

    # Start the task to check for website updates periodically
    self.loop.create_task(self.check_for_updates())

  async def on_message(self, message):
    # This method is called when a message is received
    if message.author == self.user:
      return  # Ignore messages sent by the bot itself

    if message.content.startswith('$news'):
      content = self.monitor.fetch_website_content()  # Fetch the website content
      if content:
        new_announcements = self.monitor.parse_announcements(content)  # Parse announcements from the content
        if new_announcements:
          # Format and send new announcements
          response = "\n".join([f"{text} ({link})" for text, link in new_announcements])
          await message.channel.send(f"Announcements:\n{response}")
        else:
          await message.channel.send("No new announcements.")

  async def check_for_updates(self):
    # Periodically check for new announcements
    await self.wait_until_ready()
    while not self.is_closed():
      content = self.monitor.fetch_website_content()  # Fetch the website content
      if content:
        new_announcements = self.monitor.check_for_new_announcements(content)  # Check for new announcements
        if new_announcements:
          await self.send_update_notification(new_announcements)    # Send update notification if there are new announcements
      await asyncio.sleep(3600)  # Wait for an hour before checking again

  async def send_update_notification(self, new_announcements):
    # Send new announcements to the specified channel
    channel = self.get_channel(self.channel_id)
    if channel:
      for text, link in new_announcements:
        await channel.send(f"New announcement: {text} ({link})")

# Set up Discord client with appropriate intents
intents = discord.Intents.default()
intents.message_content = True

# Create WebsiteMonitor instance with the target URL
monitor = WebsiteMonitor("https://info.asep.gr/announcements-list")

# Retrieve the channel ID from the Token instance
get_channel_instance = ChannelID()
channel_id = get_channel_instance.now_channel

# Create and run the Discord client
client = MyClient(monitor=monitor, channel_id=channel_id, intents=intents)


# Retrieve the bot token from the Token instance
get_token_instance = GetToken()
client.run(get_token_instance.now_token)