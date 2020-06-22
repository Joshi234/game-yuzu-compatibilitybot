#url=https://yuzu-emu.org/game/
import requests
from bs4 import BeautifulSoup as bs
import os
import discord
from discord.ext.commands import has_permissions
import aiohttp
import asyncio
from urllib.request import Request, urlopen
client=discord.Client()
page=requests.get("https://yuzu-emu.org/game/")
soup=bs(page.text,'html.parser')
game_names_list=soup.find(class_="data-title")
game_names_list_names=soup.find_all("td")
compatibility={}
raw_name={}
last_date={}
def update():
    global compatibility
    global raw_name
    global last_date
    page=requests.get("https://yuzu-emu.org/game/")
    soup=bs(page.text,'html.parser')
    game_names_list=soup.find(class_="data-title")
    game_names_list_names=soup.find_all("td")
    compatibility={}
    raw_name={}
    for i in game_names_list_names:
    

        if "<td data-title=" in str(i):
            title=i.get_text().splitlines()[1]
        elif "<td data-compatibility=" in str(i):
        
            try:
                compatibility[title.lower()]=i.get_text().splitlines()[1]
                raw_name[title.lower()]=title
            except:
                pass
        elif "data-timestamp=" in str(i):
            last_date[title.lower()]=i.get_text().splitlines()[1]
    print(str(len(compatibility))+" Games found")
update()
@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    else:
  
        if(message.content[0:5]==">game"):
            try:
            
                coloure=0x808080
            
                if(compatibility[message.content[6:].lower()]==" Bad"):
                    coloure=0xE9F71D
                elif(compatibility[message.content[6:].lower()]==" Okay"):
                    coloure=0x85FF5F
                elif(compatibility[message.content[6:].lower()]==" Great"):
                    coloure=0x00FF44
                elif(compatibility[message.content[6:].lower()]==" Intro/Menu"):
                    coloure=0xFF3300
                elif(compatibility[message.content[6:].lower()]==" Perfect"):
                    coloure=0x006FFF
                embed=discord.Embed(
                    title="Compatibility",
                    
                    color=coloure
                )
                embed.add_field(name="Game Name: ",value=raw_name[message.content[6:].lower()])
                embed.add_field(name="Compatibility:",value=compatibility[message.content[6:].lower()])
                embed.add_field(name="Last Time Updated:",value=last_date[message.content[6:].lower()])
                await message.channel.send(embed=embed)
            
            except:
                isUsed=0
                for i in raw_name:
                    
                    if message.content.lower()[6:] in i:

                        if(isUsed==1):
                            isUsed=2
                        elif(isUsed==0):
                            game_name=i
                            isUsed=1

                if(isUsed==0):
                            embed=discord.Embed(
                                title="Compatibility",
                                
                              
                            )
                            embed.add_field(name="Error:",value="Could find game "+message.content[6:])
                            await message.channel.send(embed=embed)
                elif(isUsed==2):
                            embed=discord.Embed(
                                title="Compatibility",
                                
                                
                                    )
                            embed.add_field(name="Error:",value="There are multiple entries for the game"+message.content[6:])
                            await message.channel.send(embed=embed)
                else:
                    coloure=0x808080
                    i=game_name
                    if(compatibility[i]==" Bad"):
                        coloure=0xE9F71D
                    elif(compatibility[i]==" Okay"):
                        coloure=0x85FF5F
                    elif(compatibility[i]==" Great"):
                        coloure=0x00FF44
                    elif(compatibility[i]==" Intro/Menu"):
                        coloure=0xFF3300
                    elif(compatibility[i]==" Perfect"):
                        coloure=0x006FFF
                    embed=discord.Embed(
                        title="Compatibility",
                                
                        color=coloure
                    )
                    embed.add_field(name="Game Name: ",value=raw_name[i])
                    embed.add_field(name="Compatibility:",value=compatibility[i])
                    embed.add_field(name="Last Time Updated:",value=last_date[i])
                    await message.channel.send(embed=embed)

        elif(message.content[0:7]==">reload"):
            embed1=discord.Embed(
                    title="Reloading, please wait",
          
            )
            message=await message.channel.send(embed=embed1)
            update()
            embed=discord.Embed(
                    title="Finished reloading list",
          
            )
            embed.add_field(name="Game Count",value="Found "+str(len(compatibility))+" Games")
            await message.delete()
            await message.channel.send(embed=embed)



client.run("NzI0NjM1NzU4NzIzNDY1MjM2.XvDD7Q.r2r4JTGpxK0NYuCr_hffq61qoLA")