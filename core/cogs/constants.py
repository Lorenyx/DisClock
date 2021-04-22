import gspread

gc_token = gspread.service_account(filename='service_account.json')

gs_token = gc_token.open('Useful Coin Timesheet')

HEADER_VALUES = ['Day', 'Time', 'In/Out', 'Name', 'ID']
DATE_F = "%m-%d"
TIME_F = "%H:%M:%S"
WKS_TITLE_F = "%m-%Y"