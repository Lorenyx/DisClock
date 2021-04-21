import gspread

gc_token = gspread.service_account(filename='./service_account.json')

gs_token = gc_token.open('Useful Coin Timesheet')

HEADER = ['ID', 'Date', 'In', 'Out']

LAST_STATE_CELL = 'A2'