#discord.py generator
#if you get internal error create an issue in github repository
#DO NOT MODIFY

import os, json, sys

if os.name == "nt": pathsp = "\\"
else: pathsp = "/"

try:
    with open(f"db{pathsp}commands.json") as f: data = json.load(f)
except Exception as e: print(f"{type(e).__name__}: {e}")

status = 0

def write(name, cost, isUsable=False, reward=None, rwmnt=None, rwlow=1, rwhigh=1000):
    with open("items.json", "r") as f: items = json.load(f)
    items[name] = dict()
    items[name]["cost"] = cost
    if isUsable:
        items[name]["isUsable"] = "true"
        items[name]["reward"] = reward
        items[name]["rwmnt"] = rwmnt
        if rwmnt == "random":
            if rwlow > rwhigh:
                print("[ERROR] lowest value is greater than higher value")
                return
            items[name]["lowest"] = int(rwlow)
            items[name]["highest"] = int(rwhigh)
    if not isUsable:
        items[name]["isUsable"] = "false"
    with open("items.json", "w+") as f: json.dump(items, f)

def itemgen():
    if not os.path.isfile("items.json"):
        f = open("items.json", "w")
        f.write("{}")
        f.close()
    with open("items.json", "r") as f: items = json.load(f)
    while True:
        name = input("item name: ")
        if name in items.keys():
            print("Item already exists")
            break
        if len(name) < 3:
            print("Item name must be at least 3 characters")
            break
        while True:
            try:
                value = int(input("item value (cost): "))
                break
            except ValueError: print("item value must be an integer")
        isUsable = input("item is usable [y/n/true/false]: ")
        if isUsable.lower() == "yes" or isUsable.lower() == "y" or isUsable.lower() == "true":
            isUsable = True
            itemType = "box"
            itemlist = []
            if len(items.keys()) != 0:
                for i in items.keys():
                    itemlist.append(i)
            if len(itemlist) == 0: reward = "coins"
            else: reward = input(f"reward when using item [coins/{'/'.join(itemlist)}]")
            if reward not in items.keys() and reward != "coins":
                raise ValueError(f"Invalid value: {reward}")
            rwamount = input(f"Amount of items rewarded [amount/random]: ")
            if rwamount == "random" or rwamount.isdigit: pass
            else: raise ValueError(f"Invalid value: {rwamount}")
            if rwamount == "random":
                low = input(f"lowest possible value of reward (press enter to skip): ")
                if low == None:
                    low = 1
                    _max = 1000
                else:
                    try: int(low)
                    except ValueError: raise ValueError(f"Invalid value: {low}")
                    try: _max = int(input(f"highest possible value of reward: "))
                    except ValueError: print("value must be an integer")
                write(name, value, True, reward, rwamount, low, _max)
            else: 
                write(name, value, True, reward, rwamount)
        elif isUsable.lower() == "no" or isUsable.lower() == "n" or isUsable.lower() == "false":
            write(name, value, False)
        else: raise ValueError(f"Invalid value: {isUsable}")
        cont = input("Would you like to create another item (y/n): ")
        if cont.lower() == "y" or cont.lower() == "yes": pass
        else: break

def modinsprompt():
    inp = input("Install required modules? (y/n): ")
    if inp.lower() == "y" or inp.lower() == "yes":
        if not os.path.isfile(f"{os.getcwd()}{pathsp}requirements.txt"): print("[FATAL] Cannot find requirements.txt")
        if os.name == "nt":
            os.system("py -m pip install -r requirements.txt")
        else: os.system("pip install -r requirements.txt")
    elif inp.lower() == "n" or inp.lower() == "no":
        print("Exiting...")
        return
    else:
        print(f"{inp}: bad input: {inp}")
        status = 1
        return

def addv(dic, key, valarr):
    if key not in dic:
        dic[key] = list()
    dic[key].extend(valarr)

def pmsg():
    print("No bot info file found.\nMake sure to create a file named cmds.txt that contains the bot commands like this:\nping\nhelp\nbeg\nwork\n\nIf you want to add a token add this\ntoken: your bot token here\nFor prefix add this:\nprefix: your bot prefix here\n")
    input("Press enter to exit...")
    return

def mkdb():
    print("[INFO] writing database")
    path = f"{os.getcwd()}{pathsp}out{pathsp}database"
    if not os.path.isdir(path):
        os.mkdir(path)
    files = ["user", "guild", "items"]
    for i in files:
        fl = open(f"{path}{pathsp}{i}.json", "w")
        fl.write("{}")
        fl.close()
    if os.path.isfile("items.json"):
        with open("items.json") as f: items = json.load(f)
        global itemsmnt
        itemsmnt = len(items.keys())

def gen(_file, genserver:bool=False):
    print("Generating file...")
    to_write = []
    token = None
    prefix = None
    userid = None
    clientid = None
    f = open(_file, "r").read().splitlines()
    l = 1
    if "all" in f:
        for key in data.keys(): to_write.append(''.join(data[key]))
        to_write.append("buy")
        to_write.append("inventory")
        to_write.append("shop")
        for line in f:
            if line.startswith("token:"): token = line.replace("token: ", "")
            elif line.startswith("prefix:"): prefix = line.replace("prefix: ", "")
            elif line.startswith("userid:"): userid = line.replace("userid: ", "")
            elif line.startswith("clientid:"): clientid = line.replace("clientid: ", "")
            else: pass
    else:
        for line in f:
            if line.startswith("token:"): token = line.replace("token: ", "")
            elif line.startswith("prefix:"): prefix = line.replace("prefix: ", "")
            elif line.startswith("userid:"): userid = line.replace("userid: ", "")
            elif line.startswith("clientid:"): clientid = line.replace("clientid: ", "")
            elif line.startswith("#"): pass
            elif line == "buy": to_write.append("buy")
            elif line == "inventory": to_write.append("inventory")
            elif line == "shop": to_write.append("shop")
            else:
                try:
                    if ''.join(data[line]) in to_write: print(f"[WARNING] Duplicate command detected in line {l}")
                    to_write.append(''.join(data[line]))
                except KeyError: print(f"[WARNING] Skipping command {line} in line {l}: no such command")
            l += 1
    if prefix == None:
        print("[FATAL] No prefix found.")
        status = 1
        return
    if userid == None:
        print("[FATAL] No user id found.")
        status = 1
        return
    if clientid == None and invite in to_write:
        print("[FATAL] No client id found")
        status = 1
        return
    if token == None: token = "token"
    print("[INFO] Reading file complete")
    if not os.path.isdir(f"{os.getcwd()}{pathsp}out"):
        path = os.path.join(os.getcwd(), "out")
        os.mkdir(path)
    else: print("[WARNING] Overwriting existing bot...")
    if not os.path.isdir(f"{os.getcwd()}{pathsp}out{pathsp}cogs"):
        path = os.path.join(f"{os.getcwd()}{pathsp}out", "cogs")
        os.mkdir(path)
    if "rank" in to_write: ranking = "true"
    else: ranking = "false"
    if genserver and not os.path.isfile(f"{os.getcwd()}{pathsp}out{pathsp}keep_alive.py"):
        file = open(f"{os.getcwd()}{pathsp}out{pathsp}keep_alive.py", "w")
        file.write("""from flask import Flask
from threading import Thread
app = Flask('')

@app.route('/', methods=['GET'])
def main():
    return 'I am online', 200

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    server = Thread(target=run)
    server.daemon = True
    server.start()
        """)
    file = open(f"{os.getcwd()}{pathsp}out{pathsp}bot.py", "w")
    file.write(f"""import json, discord, random
from discord.ext import commands
from discord.ext.commands import *
{'from keep_alive import keep_alive' if genserver else ''}

client = commands.Bot(command_prefix=\"{prefix}\")
client.load_extension(\"cogs.MainCog\")
{'keep_alive()' if genserver else ''}
client.run(\"{token}\")""")
    file.close()
    if len(to_write) == 0:
        print("[FATAL] Command array is empty")
        status = 1
        return
    icmds = False
    if os.path.isfile("items.json"):
        with open("items.json", "r") as f: items = json.load(f)
        if len(items) != 0 and "buy" in to_write and "inventory" in to_write and "shop" in to_write:
            print("[INFO] writing inventory and buy commands...")
            buy = """
    @commands.command()
    async def buy(self, ctx, item, amount:int=1):"""
            sarr = "["
            for i in range(len(items)):
                if i+1 == len(items): sarr += "0]"
                else: sarr += "0, "
            inventory = """
    @commands.command(aliases=['inv'])
    async def inventory(self, ctx, user:discord.User=None):
        if user == None: user = ctx.author
        if str(user.id) not in items: self.addv(user, items, %s)
        embed = discord.Embed(title=f"{user}'s inventory", color=discord.Color.random())
""" % sarr
            shop = """
    @commands.command()
    async def shop(self, ctx):
        embed = discord.Embed(title="shop", color=discord.Color.random())\n"""
            indx = 0
            for i in items.keys():
                buy += """
        %s item == "%s":
            if amount == 1:
                if userdat[str(ctx.message.author.id)][0] >= int("%s"):
                    items[str(ctx.message.author.id)][int("%s")] += 1
                    userdat[str(ctx.message.author.id)][0] -= int("%s")
                    self.save()
                    await ctx.reply("You bought a %s for %s coins")
                else: await ctx.reply("You don't have enough coins to buy this")
            else:
                a = amount * int("%s")
                if a > userdat[str(ctx.message.author.id)][0]: return await ctx.reply("You don't have enough coins to buy this")
                else:
                    items[str(ctx.message.author.id)][int("%s")] += amount
                    userdat[str(ctx.message.author.id)][0] -= a
                    self.save()
                    await ctx.reply(f"You bought {amount} %s for {a} coins")""" % ("if" if indx == 0 else "elif", i, items[i]["cost"], indx, items[i]["cost"], i, items[i]["cost"], items[i]["cost"], indx, i)
                inventory += "        embed.add_field(name=\"%s\", value=str(items[str(user.id)][int(\"%s\")]))\n" % (i, indx)
                shop += "        embed.add_field(name=\"%s\", value=\"Cost: %s\")\n" % (i, items[i]["cost"])
                indx += 1
            buy += "\n        else: await ctx.reply(\"This item does not exist\")"
            inventory += "        await ctx.reply(embed=embed)\n"
            shop += "        await ctx.reply(embed=embed)\n"
            icmds = True
    file = open(f"{os.getcwd()}{pathsp}out{pathsp}cogs{pathsp}MainCog.py", "w")
    file.write("""#generated by discord-py-generator
import json, requests, discord, math, sys, praw, traceback, prawcore, datetime, asyncio, random
from discord.ext import *
import html

on_cooldown = {}
cd = {}
invest_time = 3600
clientid = int("%s")
ranking = "%s"
itemamount = "%s"
try:
    int(itemamount)
    itemamount = int(itemamount)
except ValueError:
    itemamount = 0
with open(f"database/user.json", "r") as f: userdat = json.load(f)
with open(f"database/guild.json", "r") as f: gdata = json.load(f)
with open(f"database/items.json", "r") as f: items = json.load(f)
reddit = praw.Reddit(client_id='_pazwWZHi9JldA',
                     client_secret='1tq1HM7UMEGIro6LlwtlmQYJ1jB4vQ',
                     user_agent='idk', check_for_async=False) 

global userid
userid = int("%s")

class MainCog(commands.Cog):
    def __init__(self, client:commands.Bot):
        self.client = client

    def addv(self, dic, key, valarr):
        if key not in dic:
            dic[key] = list()
        dic[key].extend(valarr)

    def save(self):
        with open("database/user.json", "w+") as f: json.dump(userdat, f)
        with open("database/guild.json", "w+") as f: json.dump(gdata, f)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'): return
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None: return
        ignored = (commands.CommandNotFound)
        error = getattr(error, 'original', error)
        if isinstance(error, ignored): return
        if isinstance(error, commands.DisabledCommand): await ctx.send(f'{ctx.command} has been disabled.')
        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except discord.HTTPException:
                pass       
        if isinstance(error, commands.CommandOnCooldown):
            print(f"{self.gettime()}CommandOnCooldown triggered by {ctx.author} in {ctx.command}")
            if math.ceil(error.retry_after) < 60:
                await ctx.reply(f'This command is on cooldown. Please try after {math.ceil(error.retry_after)} seconds')
            elif math.ceil(error.retry_after) < 3600:
                ret = math.ceil(error.retry_after) / 60
                await ctx.reply(f'This command is on cooldown. Please try after {math.ceil(ret)} minutes')
            elif math.ceil(error.retry_after) >= 3600:
                ret = math.ceil(error.retry_after) / 3600
                if ret >= 24:
                    r = math.ceil(ret) / 24
                    await ctx.reply(f"This command is on cooldown. Please try after {r} days")
                else:
                    await ctx.reply(f'This command is on cooldown. Please try after {math.ceil(ret)} hours')
        elif isinstance(error, commands.BadArgument):
            print(f"{self.gettime()}BadArgument triggered by {ctx.author} in {ctx.command}")
            if ctx.command.qualified_name == 'tag list':
                await ctx.send('I could not find that member. Please try again.')
            else:
                await ctx.send("Invalid argument")
        elif isinstance(error, commands.MissingRequiredArgument): await ctx.send("Missing required argument")
        elif isinstance(error, commands.MissingPermissions): await ctx.reply("You can\'t use this")
        elif isinstance(error, commands.BotMissingPermissions): await ctx.reply("I don\'t have permissions to use this")
        elif isinstance(error, commands.errors.NSFWChannelRequired): await ctx.reply("This command only works in a nsfw channel")
        else:
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            u = str(message.author.id)
            g = str(message.guild.id)
            if g not in gdata:
                self.addv(gdata, g, [dict(), "%s", 1, 0, list()])
                self.save()
            if u not in userdat:
                self.addv(userdat, u, [0, 0, 0])
                self.save()
            if u not in items:
                if itemamount != 0:
                    to_append = []
                    for i in range(itemamount): to_append.append(0)
                    self.addv(items, u, to_append)
                    self.save()
            if ranking == "true":
                if u not in gdata[g][0].keys(): self.addv(gdata[g][0], u, [1, 1])
                gdata[g][0][u][0] += 1
                xpreq = 0
                if gdata[g][0][u][1] == 1 or gdata[g][0][u][1] == 0:
                    xpreq = 25
                else:
                    for level in range(gdata[g][0][u][1]):
                        xpreq += 25
                        if xpreq >= 5000: break
                if int(gdata[g][0][u][0]) >= xpreq:
                    gdata[g][0][u][0] = 0
                    gdata[g][8][u][1] += 1
                    await message.channel.send(f"{message.author.mention} You just leveled up to level **{gdata[g][0][u][1]}**!")
                self.save()
            if gdata[g][3] == 1:
                if any(x in message.content.lower() for x in gdata[g][4]):
                    await message.delete()
                    await message.channel.send(f"{message.author.mention} Watch your language")
    
    %s
    %s
    %s
""" % (clientid, ranking, len(items) if os.path.isfile("items.json") else "none", userid, prefix, buy if icmds else '', inventory if icmds else '', shop if icmds else ''))
    for cmd in to_write:
        if cmd == "buy" or cmd == "inventory" or cmd == "shop": pass
        else: file.write(cmd)
    file.write("""def setup(client):
    client.add_cog(MainCog(client))""")
    file.close()
    mkdb()
    print("Operation complete!")
    modinsprompt()

try:
    if os.path.isfile(f"{os.getcwd()}{pathsp}cmds.txt"):
        inp = input("Add keep alive script for 24/7 hosting in replit? (y/n): ")
        inp1 = input("Start item generator? (y/n): ")
        if inp1.lower() == "y" or inp1.lower() == "yes": itemgen()
        else: pass
        if inp.lower() == "y" or inp.lower() == "yes": gen(f"{os.getcwd()}{pathsp}cmds.txt", True)
        elif inp.lower() == "n" or inp.lower() == "no": gen(f"{os.getcwd()}{pathsp}cmds.txt")
        else:
            print("Invalid input")
            status = 1
    else: pmsg()
except Exception as e:
    print(f"[Internal error] {type(e).__name__}: {e}")
    status = 1
sys.exit(status)
