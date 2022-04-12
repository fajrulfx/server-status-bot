import discord
import requests
import datetime
import pytz
from mcstatus import MinecraftServer
from mcstatus import MinecraftBedrockServer

javaserver = "play.sciencekingdom.gg"
bedrockserver = "bedrock.sciencekingdom.gg"
bot_token = "xxxxxxxx"

def get_response_java():
    try:
        serverdata = MinecraftServer.lookup(javaserver).status()
        return True, serverdata
    except Exception:
        return False, 'nothing'

def get_response_bedrock():
    try:
        MinecraftBedrockServer.lookup(bedrockserver).status()
        return True 
    except Exception:
        return False 

def check_time():
    time_now_zone = datetime.datetime.now(pytz.timezone("Asia/Jakarta"))
    waktu = time_now_zone.strftime("Update: %d/%m/%Y | %H:%M WIB")
    return waktu

def embedmsg():

    bedrock_stat = get_response_bedrock()
    if bedrock_stat:
        bedrockstatus = '<a:MSK_verified:925684036632973312> Online'
    else:
        bedrockstatus = '<a:MSK_warning:950189573345017866> Offline'

    java_stat, server = get_response_java()
    if java_stat:
        javastatus = '<a:MSK_verified:925684036632973312> Online'
        playeronline, playermax = server.players.online, server.players.max
        deskripsi = '<a:MSK_sheeprgbmc:925679692739145758> Player: '+ str(playeronline) +'/'+ str(playermax) +'\n\n<a:MSK_minecraftjoged:925683776888111165> **JAVA**\nIP: play.sciencekingdom.gg\nStatus: ' + javastatus +'\n\n<a:MSK_minecraftjoged:925683776888111165> **BEDROCK**\nIP: bedrock.sciencekingdom.gg\nPort: 19132\nStatus: ' + bedrockstatus + ' \n\u200B '
    else:
        javastatus = '<a:MSK_warning:950189573345017866> Offline'
        deskripsi = '<a:MSK_minecraftjoged:925683776888111165> **JAVA**\nIP: play.sciencekingdom.gg\nStatus: ' + javastatus +'\n\n<a:MSK_minecraftjoged:925683776888111165> **BEDROCK**\nIP: bedrock.sciencekingdom.gg\nPort: 19132\nStatus: ' + bedrockstatus + ' \n\u200B '
    lastupdate = check_time()
    
    try:
        if 'MAINTENANCE' in server.description:
            deskripsi = '<a:MSK_warning:950189573345017866> Maintenance mode\n\u200B'
    except Exception:
        pass

    return discord.Embed(title='**MSK Server Status**', description=deskripsi, color=discord.Color.blue()).set_footer(text=lastupdate, icon_url='https://images-ext-2.discordapp.net/external/7uqHzZFjSUnhJmO0JBBbkl3NwJWctAqzsZ4NCSw7UGI/https/media.discordapp.net/attachments/939463451468771348/940956084011667466/LOGO_MSK1.png')

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        # print('receive message')
        if message.author == self.user:
            return
        if message.content == '!server':
            embedmessage = embedmsg()
            await message.channel.send(embed=embedmessage)

client = MyClient()
client.run(bot_token)
