import gspread

gc_token = gspread.service_account(filename='./service_account.json')

gs_token = gc_token.open('Useful Coin Timesheet')

HEADER = ['Date', 'In', 'Out', 'Hours']