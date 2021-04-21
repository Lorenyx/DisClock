import gspread

gc_token = gspread.service_account(filename='service_account.json')

gs_token = gc_token.open('Useful Coin Timesheet')

HEADER_VALUES = ['Day', 'Time', 'In/Out', 'Name', 'ID']
HEADER_RANGE = 'A1:D1'