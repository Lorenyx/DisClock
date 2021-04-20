from discord.ext import commands
from datetime import datetime

class Timesheet(commands.Cog):
    """Handles the time and connection to the google sheet"""

    async def ctime(self) -> datetime:
        return datetime.datetime.now()

    async def cmonth(self):
        return self.ctime().strftime("%m-%Y")


    async def get_worksheet(self):
        if  self.cmonth() == 