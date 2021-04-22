import gspread


from discord.ext import commands
from discord import Emoji
from datetime import datetime, timedelta

from .constants import HEADER_VALUES, TIME_F, DATE_F, WKS_TITLE_F, gs_token

class Timesheet(commands.Cog):
    """Handles the time and connection to the google sheet"""
    def __init__(self):
        self.__current_state = None
        self.__time_clocked_in = None


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
        return (await self.ctime()).strftime(WKS_TITLE_F)


    async def get_wks(self):
        try:
            wks = gs_token.worksheet(await self.get_wks_title())
        except gspread.WorksheetNotFound:
            wks = gs_token.add_worksheet(await self.get_wks_title(), 10, 5)
            wks.insert_row(HEADER_VALUES, index=1)
        return wks


    async def calc_hours_worked(self, user, *, __days=0, __weeks=0, __months=0):
        #TODO IDEA: allow specific time range
        async def hours_per_day(__records: list) -> timedelta:
            total_hours = timedelta(0)
            for record in range(len(__records), step=2):

        retval = []
        start_dt = await self.ctime()
        end_dt = start_dt - timedelta(days=(__days + __months * 30), weeks=__weeks)
        records = await self.get_wks().get_all_records()
        


    async def insert_entry(self, attendance, user):
        "Appends entry to monthly log"
        wks = await self.get_wks()
        time_val = await self.ctime()
        wks.append_row([
            time_val.strftime(DATE_F),
            time_val.strftime(TIME_F),
            attendance.strip(),
            user.name,
            f'<@{user.id}>'
        ])

    