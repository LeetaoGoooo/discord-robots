import discord
import os
from discord import app_commands

from api.gemini import explain_word, reply, rewrite_prompt
from api.bing import create_image
from urllib.parse import urlparse

# your own server guild
MY_GUILD = discord.Object(id=os.getenv("GUILD"))


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


intents = discord.Intents.default()
intents.message_content = True

bot = MyClient(intents=intents)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.event
async def on_message(message):
    # don't respond to ourselves
    if message.author == bot.user:
        return
    if bot.user in message.mentions:
        reply_message = await message.channel.send("I'm is thinking...")
        response = await reply(message=message.content, attachments=message.attachments)
        await reply_message.edit(content=response)


@bot.tree.command(name="bing-prompt", description="use bing create to create images")
@app_commands.describe(
    prompt='prompt for create images',
)
async def prompt_bing(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer()
    image_list = create_image(prompt)
    parsed_url = urlparse(image_list[0])
    embeds = [discord.Embed(
        url=f'{parsed_url.scheme}://{parsed_url.netloc}').set_image(url=image) for image in image_list]
    await interaction.followup.send(content=prompt,
                                    embeds=embeds)


@bot.tree.command(name="bing-prompt-pro", description="use gemini to enhance bing create to create better images")
@app_commands.describe(
    prompt='prompt for create images',
)
async def prompt_bing(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer()
    prompt = rewrite_prompt(prompt)
    image_list = create_image(prompt)
    parsed_url = urlparse(image_list[0])
    embeds = [discord.Embed(
        url=f'{parsed_url.scheme}://{parsed_url.netloc}').set_image(url=image) for image in image_list]
    await interaction.followup.send(content=f'gemini rewrite:{prompt}',
                                    embeds=embeds)

@bot.tree.command(name="eudic-word", description="query word and save word in notebook ")
@app_commands.describe(
    prompt='query word in eudic',
)
async def query_word(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer()
    content = explain_word(prompt)
    try:
        await interaction.followup.send(content=content)
    except:
        await interaction.followup.send(content="Failed, please try again")

def run():
    bot.run(os.getenv("DISCORD_TOKEN"))


if __name__ == "__main__":
    run()
