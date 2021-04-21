import gspread


from discord.ext import commands
from discord import Emoji
from datetime import datetime

from .constants import HEADER_VALUES, HEADER_RANGE, gs_token

class Timesheet(commands.Cog):
    """Handles the time and connection to the google sheet"""


    @commands.command()
    async def clock(self, ctx, arg):
        "General method for clocking in and out"
        if arg == 'in':
            await self.clock_in(ctx)
        elif arg == 'out':
            await self.clock_out(ctx)

    
    @commands.command(aliases=['in'])
    async def clock_in(self, ctx):
        "Command used when clocking in"
        await self._attend(ctx, 'in')
        

    @commands.command(aliases=['out'])
    async def clock_out(self, ctx):
        "Command used when clocking out"
        await self._attend(ctx, 'out')


    async def _attend(self, ctx, __dest: str):
        try:
            async with ctx.typing():
                await self.insert_entry(__dest, ctx.author)
            await ctx.message.add_reaction(r'✅')
        except Exception as E:
            print(f'[-] Error: {E}')
            await ctx.message.add_reaction(r'❌')

    
    async def ctime(self) -> datetime:
        return datetime.now()


    async def get_wks_title(self):
        return (await self.ctime()).strftime("%m-%Y")


    async def get_wks(self):
        try:
            wks = gs_token.worksheet(await self.get_wks_title())
        except gspread.WorksheetNotFound:
            wks = gs_token.add_worksheet(await self.get_wks_title(), 10, 5)
            #TODO Verify update_values
            wks.insert_row(HEADER_VALUES, index=1)
        return wks


    async def insert_entry(self, attendance, user):
        "Appends entry to monthly log"
        wks = await self.get_wks()
        time_val = await self.ctime()
        wks.append_row([
            time_val.strftime("%m-%d"),
            time_val.strftime("%H:%M:%S"),
            attendance.strip(),
            user.name,
            user.id
        ])