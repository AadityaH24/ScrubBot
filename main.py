import os
import discord

bot = discord.Bot(debug_guilds=[796219509047296011]) # specify the guild IDs in debug_guilds

#Initial Login
@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")


#Commands

@bot.command(description="Sends the bot's latency.") 
async def ping(ctx): 
    await ctx.respond(f"Pong! Latency is {bot.latency}")
    
    
@bot.command(description="Convert 24hr HH:MM time to other timezones.")
async def timeconv(ctx, zone:discord.Option(str,choices = ["IST","ICT","EDT"]), *, time):
    
    #timezone offsets in hours and minutes againt GMT
    #to add more timezones simply add more tuples to the dictionary below
    timediff = {"IST": [5,30], "ICT": [7,0], "EDT": [20,0]} 
    ot = {} #temp store for output times
    defmsg = "{hours:02d}:{minutes:02d}" #preformatted o/p str
    
    #Calc and store time in preformatted string
    if zone in timediff and time.count(":") == 1:
        time = time.split(":")
        hour = int(time[0])
        minute = int(time[1])
        ot[zone] = defmsg.format(hours=hour, minutes=minute) #first timezone
        
        #get remaining timezones into ot
        for i in timediff:
            if(i == zone):
                continue
            temph = timediff[i][0] - timediff[zone][0]
            tempm = timediff[i][1] - timediff[zone][1]
            if(tempm + minute < 0):
                temph -= 1
                tempm += 60
            elif(tempm + minute > 60):
                temph += 1
                tempm -= 60
            ot[i] = defmsg.format(hours=(hour + temph)%24, minutes=(minute + tempm)%60)
        
        #final response
        await ctx.respond(ctx.author.mention + " mentioned this time\n" + "\n".join("{}\t{}".format(k, v) for k, v in ot.items()))
            
        
    else:
        await ctx.respond(f"Invalid timezone or time format.\n{ctx.author.mention}")


#TESTING


#choices in slash command
# @bot.command()
# async def test(ctx, num: discord.Option(int), char: discord.Option(str,choices = ["a","b","c"])):
#   await ctx.respond(f"{num} {char}")


# slash command groups with bot.create_group
# greetings = bot.create_group("greetings", "Greet people")

# @greetings.command()
# async def hello(ctx):
#   await ctx.respond(f"Hello, {ctx.author}!")

# @greetings.command()
# async def bye(ctx):
#   await ctx.respond(f"Bye, {ctx.author}!")

###WIP: custom role allotment

#Bot exec

my_secret = os.environ['token']
bot.run(my_secret)
