import discord
from discord.ext import commands

import json
import os.path
import random



class Mycog:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def santa(self, ctx):
        if ctx.invoked_subcommand is None:
            help = """
            ```
Secret Santa plugin

available commands:
    • register <address> - Join the Secret Santa. You have to provide your valid address.
    • unregister - Resign from participation and delete your data.
    • info - Get info about the current number of participants and your provided address. This command is DM-only.
owner-only commands:
    • shuffle - Start Secret Santa.
            ```
            """
            await self.bot.say(help)

    @santa.command(pass_context=True)
    async def register(self, ctx, *address):
        """Register to the Secret Santa"""

        address = " ".join(address)
        if ctx.message.server == None:
            if 100 > len(address) > 0:
                store = open("data/santa/users.json").read()
                file = json.loads(store)
                user = {
                    'id': str(ctx.message.author),
                    'address': address
                }
                for u in file:
                    if u['id'] == user['id']:
                        file.remove(u)

                file.append(user)
                with open("data/santa/users.json", "w") as outfile:
                    json.dump(file, outfile)
                await self.bot.say("Registered! 🎁 \nYour address is: **" + user['address'] + "** \nIf this isn't your correct address, you can use `register` command again to change it.")
            else:
                await self.bot.say('Your address is too long or too short.')
        else:
            await self.bot.say("You want to leak your address so badly, dummy? Use this command in DMs.")

    @santa.command(pass_context=True)
    async def info(self, ctx):
        if ctx.message.server == None:
            store = open("data/santa/users.json").read()
            file = json.loads(store)
            user = {}
            for u in file:
                if u['id'] == str(ctx.message.author):
                    user = u
            if user:
                await self.bot.say("Currently **" + str(len(file)) + "** users are registered. \nYour registered address is: **" + str(user['address']) + "**")
            else: 
                await self.bot.say("You are not registered!")
        else:
            await self.bot.say("You want to leak your address so badly, dummy? Use this command in DMs.")

    @santa.command(pass_context=True)
    async def shuffle(self, ctx):
        if ctx.message.author.id == ctx.bot.settings.owner:
            store = open("data/santa/users.json").read()
            givers = json.loads(store)
            random.shuffle(givers)
            receivers = givers.copy()
            receivers = receivers[1::] + receivers[:1:]

            for index, u in enumerate(givers):
                user = ctx.message.server.get_member_named(name = u['id'])
                msg = "Ho ho ho, you drawed **" + str(receivers[index]['id']) + "** for the Secret Santa! 🎅 \nTheir address is: **" + str(receivers[index]['address']) + "**, don't leak it!"
                await self.bot.send_message(user, msg)
        else: 
            await self.bot.say("You are not allowed to do this.")

    @santa.command(pass_context=True)
    async def unregister(self, ctx):
        store = open("data/santa/users.json").read()
        file = json.loads(store)
        user = {}
        for u in file:
            if u['id'] == str(ctx.message.author):
                user = u
        if user:
            file.remove(user)
            with open("data/santa/users.json", "w") as outfile:
                json.dump(file, outfile)
            await self.bot.say("You are no longer registered! :<")
        else:
            await self.bot.say("You cannot unregister if you are not registered :rollsafe:")


def setup(bot):
    bot.add_cog(Mycog(bot))
