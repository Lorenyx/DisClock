import gspread

from discord.ext import commands
from datetime import datetime

from constants import HEADER, gsheet_token

class Timesheet(commands.Cog):
    """Handles the time and connection to the google sheet"""

    async def ctime(self) -> datetime:
        return datetime.datetime.now()


    async def cmonth(self):
        return await self.ctime().strftime("%m-%Y")


    async def get_wks(self):
        try:
            wks = gsheet.worksheet(self.cmonth())
        except gspread.WorksheetNotFound:
            wks = gsheet.add_worksheet(self.cmonth(), 10, 5)
            wks.append_row(HEADER, table_range='A1:D1')
        return wks