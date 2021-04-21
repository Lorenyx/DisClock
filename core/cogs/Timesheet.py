import gspread

from discord.ext import commands
from datetime import datetime

from constants import HEADER, LAST_STATE_CELL, gs_token

class Timesheet(commands.Cog):
    """Handles the time and connection to the google sheet"""
    def __init__(self):
        # Boolean value, True if clocked in, False if not clocked in
        self.__clocked_in = self.previous_state()



    async def ctime(self) -> datetime:
        return datetime.datetime.now()


    async def cmonth(self):
        return await self.ctime().strftime("%m-%Y")


    async def day_time(self) -> tuple:
        """
        Returns tuple of current day (mm-dd) and time (hh:mm:ss) """
        time = await self.ctime()
        return (
            time.strftime("%m-%d"),
            time.strftime("%H:%M:%S")
        )


    async def get_wks(self):
        try:
            wks = gs_token.worksheet(self.cmonth())
        except gspread.WorksheetNotFound:
            wks = gs_token.add_worksheet(self.cmonth(), 10, 5)
            #TODO Verify update_values
            wks.update_values(HEADER, table_range='A1:D1')
        return wks


    async def previous_state(self):
        """
        Not to be called directly.
            - Returns the last action of the user.
            - Returns True if user is currently clocked in.
            (Value of 1 in 'Last State' cell from 'Config' sheet.)
            - Returns False if user is not currently clocked in.
            (Value of 0 in 'Last State' cell from 'Config' sheet.) 
        """
        #TODO Verify if it works
        prev_state = gs_token.worksheet('config').acell(LAST_STATE_CELL)
        if prev_state == 1:
            return True
        return False


    @commands.command(alias='in')
    async def clock_in(self, ctx):
        #TODO Verify if this works
        if not self.__current_state:
            user_id = ctx.author.id
            wks = await self.get_wks()
            day, time = await self.day_time()
            # Follow pattern of HEADER (ID, Date, In, Out)
            wks.append_row([
                user_id,
                day,
                time
            ])
        #TODO Finish the other part
        return True


    @commands.command(alias='out')
    async def clock_out(self, ctx):
        #TODO Verify if this works
