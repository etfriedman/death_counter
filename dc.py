from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import discord
from discord.ext import commands

class DeathCount():
    def __init__(self,streamer):
        chrome_options = Options()
        chrome_options.add_argument('--log-level=3')
        chrome_options.add_argument(r"--user-data-dir=C:\Users\YOUR USERNAME\AppData\Local\Temp\SCOPED_DIR FOR YOUR CHROME INSTANCE") # <-- replace stuff here
        site = webdriver.Chrome(executable_path=r"chromedriver.exe", options=chrome_options)
        streamer = streamer
        site.get('https://www.twitch.tv/popout/' + streamer + "/chat?popout=")
        self.chat = site.find_elements_by_tag_name('textarea')[0]

    def set_text(self,num_counters,counter,counters):
        self.num_counters = int(num_counters)
        self.counter = counter
        self.counters = counters
        self.counter = self.counter.format(*(i for i in self.counters))

    def add_count(self):
        for val in self.counters:
            self.counter = self.counter.replace(str(val),str(val+1))
        print(self.counter)
        self.chat.send_keys(self.counter)
        self.chat.send_keys(Keys.RETURN)
        for num in self.counters:
            self.counters[self.counters.index(num)] = self.counters[self.counters.index(num)]+1

    def repeat(self):
        self.chat.send_keys(self.counter)
        self.chat.send_keys(Keys.RETURN)

TOKEN = open("token.txt","r").readline()
client = commands.Bot(command_prefix = '.')

@client.command()
async def init(ctx):
    await ctx.send("Starting Death Counter. Please enter name of streamer")
    msg = await client.wait_for('message')
    global first_count
    first_count = DeathCount(msg.content)
    await ctx.send("Done. please send '.set_counters' to proceed.")

@client.command()
async def set_counters(ctx):
    await ctx.send("please enter the number of counters you would like to include")
    msg = await client.wait_for('message')
    global num_counters
    num_counters = msg.content
    await ctx.send("Number of counters set")
    await ctx.send("Done. please send '.set_counter' to proceed. (not set_counters)")
@client.command()
async def set_counter(ctx):
    await ctx.send("Input the text you would like to have accompany the death count. place '\{\}' where you would like the death count to be put in the text, i.e. 'current deaths: \{\}' would yield 'current deaths: 125' For adding a secondary counter, include \{\}, \{\}, etc")
    msg = await client.wait_for('message')
    global counter
    counter = msg.content
    await ctx.send("Counter text set")
    await ctx.send("Done. please send '.set_values' to proceed")

@client.command()
async def set_values(ctx):
    await ctx.send("put numbers for each counter (i.e. with 2 counters you would put 0,2 if the first counter = 0 and second counter = 2)")
    msg = await client.wait_for('message')
    counters = [int(i) for i in msg.content.replace(",","")]
    print(num_counters,counter,counters)
    await ctx.send("Counters set")
    first_count.set_text(num_counters,counter,counters)
    await ctx.send("Done. please refer to .help on how to use the bot now.")

@client.command()
async def add(ctx):
    first_count.add_count()
    await ctx.send('Added 1 to each death count')

@client.command()
async def r(ctx):
    first_count.repeat()
    await ctx.send('Repeated death count!')

@client.event
async def on_command_error(ctx, error):
    await ctx.send(f'Error: {error}. Try .help')


client.remove_command('help')
client.remove_command('start')
@client.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(
        colour = discord.Colour.purple())
    embed.set_author(name='Available commands:')
    embed.add_field(name='.start', value='start the death_count process', inline=False)
    embed.add_field(name='.add', value='increases counters by 1, sends to chat', inline=False)
    embed.add_field(name='.r', value='re-sends current death count in chat', inline=False)
    await ctx.send(embed=embed)

client.run(TOKEN)
