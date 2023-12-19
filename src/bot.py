import discord
import os
from discord import app_commands

from api.gemini import reply,rewrite_prompt
from api.bing import create_image
from urllib.parse import urlparse

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):
        # don't respond to ourselves
        if message.author == bot.user:
             return
        if bot.user in message.mentions:
            response = await reply(message=message.content, attachments=message.attachments)
            await message.channel.send(response)


@tree.command(name="bing-prompt", description="use bing create to create images")
@app_commands.describe(
    prompt='prompt for create images',
)
async def prompt_bing(interaction: discord.Interaction, prompt:str):
    image_list = create_image(prompt)
    parsed_url = urlparse(image_list[0])
    embeds = [discord.Embed(url=f'{parsed_url.scheme}://{parsed_url.netloc}').set_image(url=image) for image in image_list]
    interaction.response.send_message(embeds=embeds)


@tree.command(name="bing-prompt-pro", description="use gemini to enhance bing create to create better images")
@app_commands.describe(
    prompt='prompt for create images',
)
async def prompt_bing(interaction: discord.Interaction, prompt:str):
    prompt = rewrite_prompt(prompt)
    image_list = create_image(prompt)
    parsed_url = urlparse(image_list[0])
    embeds = [discord.Embed(url=f'{parsed_url.scheme}://{parsed_url.netloc}').set_image(url=image) for image in image_list]
    interaction.response.send_message(embeds=embeds)


def run():
    bot.run(os.getenv("DISCORD_TOKEN"))

if __name__ == "__main__":
    run()