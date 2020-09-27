import openpyxl
from sqlite3 import connect
from os.path import exists

DATABASE= 'test.db'
LAW_FILE = 'all.xlsx'

if not exists(DATABASE):
  sql = "CREATE TABLE all_states (State,station_name,NSN,Item_Name, Quantity,UI,Acquisition_Value,DEMIL_Code,DEMIL_IC,Ship_Date, Station_Type)"
  db = connect(DATABASE)
  cur = db.cursor()
  cur.execute(sql)
else:
  db = connect(DATABASE)
  cur = db.cursor()
  
print ("Loading excel document (this may take a few minutes)")
wb = openpyxl.load_workbook(LAW_FILE)

sheets = wb.get_sheet_names()

for active_sheet_name in sheets:
  active_sheet = wb.get_sheet_by_name(active_sheet_name)
  values = [i[:11] for i in active_sheet.values if i[0] != 'State']
  count = len(values)
  state = values[0][0]
  
  sql = "INSERT INTO all_states VALUES(?,?,?,?,?,?,?,?,?,?,?)"
  print("Adding {} items into state {}".format(count,state))
  if not cur.executemany(sql,values):
     print ('DATABASE ERROR')