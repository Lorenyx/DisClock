import gspread

gc = gspread.service_account(filename='./service_account.json')

gsheet = gc.open('Useful Coin Timesheet')

HEADER = ['Date', 'In', 'Out', 'Hours']