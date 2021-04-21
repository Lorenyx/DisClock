import gspread


from discord.ext import commands
from discord import Emoji
from datetime import datetime

from .constants import HEADER_VALUES, HEADER_RANGE, gs_token

class Timesheet(commands.Cog):
    """Handles the time and connection to the google sheet"""

    #TODO See if space-sperated works later
    @commands.command(aliases=['in', 'clock_in', 'out', 'clock_out'])
    async def punch(self, ctx):
        if ctx.command in ['in', 'clock_in']:
            await self._attend(ctx, 'in')
        elif ctx.command in ['out', 'clock_out']:
            await self._attenf(ctx, 'out')


    async def _attend(self, ctx, __dest: str):
        try:
            await self.insert_entry(__dest, ctx.author.id)
            await ctx.message.add_reaction(r'✅')
        except Exception as E:
            print(f'[-] Error: {E}')
            await ctx.message.add_reaction(r'❌')


    async def ctime(self) -> datetime:
        return datetime.datetime.now()


    async def get_wks_title(self):
        return await self.ctime().strftime("%m-%Y")


    async def get_wks(self):
        try:
            wks = gs_token.worksheet(await self.cmonth())
        except gspread.WorksheetNotFound:
            wks = gs_token.add_worksheet(await self.get_wks_title(), 10, 5)
            #TODO Verify update_values
            wks.update_values(HEADER_VALUES, table_range=HEADER_RANGE)
        return wks


    async def insert_entry(self, attendance, user_id):
        "Appends entry to monthly log"
        wks = await self.get_wks()
        time_val = await self.ctime()
        wks.append_row([
            time_val.strftime("%d-%m"),
            time_val.strftime("%H:%M:%S"),
            attendance.strip(),
            user_id
        ])