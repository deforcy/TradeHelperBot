import json

file = 'settings.json'

def check(f):
    try:
        open(f)
    except:
        return False
    else:
        return True

def check2(f):
    try:
        json.load(open(f))
    except:
        return False
    else:
        return True

while check(file) == False and check2(file) == False:
    file = input("Warning! Settings file wasn't found. Type file name with .json at the end to search:")
if check2(file) == False:
    print(f"Warning! {file} file was broken. Change settings file and restart programm")
    exit('Broken settings file')

with open(file) as data:
    settings = json.load(data)

def status_check(status):
    if status == 0:
        return discord.Status.offline
    if status == 1:
        return discord.Status.online
    if status == 2:
        return discord.Status.dnd
    if status == 3:
        return discord.Status.idle
    return discord.Status.online

import discord
import interactions

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
bot_id = settings["bot_id"]
access_role = settings["access_role"]
mention_role = settings["mention_role"]
allowed_channels = settings["allowed_channels_id"]
colors = [
    settings["colors"]["active_deal"],
    settings["colors"]["good_deal"],
    settings["colors"]["bad_deal"],
    settings["colors"]["nothing_deal"]
]
status_message = settings["status_message"]
status = status_check(settings["status"])

@client.event
async def on_ready():
    
    print(f'Bot is loaded successfully')
    await client.change_presence(status=status,activity=discord.CustomActivity(name=status_message))

@client.event
async def on_message(message):
    if access_role in [str(y.id) for y in message.author.roles] and str(message.channel.id) in allowed_channels:
        data = message.content.split()
        if len(data) > 0 and data[0] == f'<@{bot_id}>': #it is a bot id for tagging it in channel
            data.pop(0)
            if len(message.attachments) > 0:
                img = message.attachments[0].url
            else:
                img = False
            for i in range(len(data)):
                data[i] = data[i].replace('-',' ')
            if data[0] == data[0].upper():
                
                trade = discord.Embed(title=data[0], color=int(colors[0],16))
                trade.add_field(name=settings["localization"]["en"]["labels"]["ep"], value=data[1], inline=False)
                trade.add_field(name=settings["localization"]["en"]["labels"]["tp"], value=data[2], inline=False)
                trade.add_field(name=settings["localization"]["en"]["labels"]["sl"], value=data[3], inline=False)

                class trade_view(discord.ui.View):
                    def __init__(self):
                        super().__init__(timeout=None)
                            
                    @discord.ui.button(label=settings["localization"]["en"]["buttons"]["tp1"], custom_id="button-1", style=discord.ButtonStyle.green)
                    async def b1_click(self, button : discord.ui.Button, interaction: discord.Interaction) -> None:
                            trade.color = int(colors[1],16)
                            await interaction.response.edit_message(content=settings["localization"]["en"]["buttons"]["tp2"], view=None, embed = trade)
                            
                    @discord.ui.button(label=settings["localization"]["en"]["buttons"]["sl1"], custom_id="button-2", style=discord.ButtonStyle.red)
                    async def b2_click(self, button : discord.ui.Button, interaction: discord.Interaction) -> None:
                            trade.color = int(colors[2],16)
                            await interaction.response.edit_message(content=settings["localization"]["en"]["buttons"]["sl2"], view=None, embed = trade)

                    @discord.ui.button(label=settings["localization"]["en"]["buttons"]["er1"], custom_id="button-3", style=discord.ButtonStyle.grey)
                    async def b3_click(self, button : discord.ui.Button, interaction: discord.Interaction) -> None:
                            trade.color = int(colors[3],16)
                            await interaction.response.edit_message(content=settings["localization"]["en"]["buttons"]["er2"], view=None, embed = trade)
                            
                if len(message.attachments) > 0:
                    file = await message.attachments[0].to_file()
                    file.filename = 'image.png'
                    await message.channel.send(content = f"<@&{mention_role}>", file = file, embed = trade, view = trade_view())
                else:
                    await message.channel.send(content = f"<@&{mention_role}>", embed = trade, view = trade_view())

                await message.delete()
            
client.run(settings['bot_token'])
print("Bot stopped")
