# Dependencies
import mysql.connector
import sys

# Initiate Connection
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database='ecommerce'
)

# Initiate db.
mycursor = mydb.cursor(buffered=True)

def delete(db, arg1, arg2):
    print('DELETE FROM ' + db + ' WHERE ' + arg1 +' = ' + arg2)
    mycursor.execute('DELETE FROM ' + db + ' WHERE ' + arg1 +' = ' + arg2)
    mydb.commit()
    print(mycursor.rowcount, "record(s) deleted")
    print('Successfully Deleted Item in: ', db)

