import psycopg2
import csv

class Control:
    def __init__(self, db_name, user_name, password, host, port):
        self.databaseName = db_name
        self.userName = user_name
        self.userPassword = password
        self.host = host
        self.port = port

        self.connection = psycopg2.connect(database=self.databaseName, user=self.userName,
                                           password=self.userPassword, host=self.host,
                                           port=self.port)
        self.current = self.connection.cursor()

    def createTable(self, nameTable: str, arrayLines: dict):
        keys = [i for i in arrayLines]
        helpString = "CREATE TABLE " + nameTable + " ("
        for i in keys:
            helpString += i + " " + arrayLines[i] + ", "
        helpString = helpString[:len(helpString) - 2]
        helpString += ")"
        self.current.execute(helpString)
        self.connection.commit()
        
    def updateTable(self, nameTable:str, condition:str):
        self.current.execute("ALTER TABLE {} {}".format(nameTable, condition))
        self.connection.commit()

    def getTableColums(self, nameTable: str):
        self.current.execute("SELECT * FROM " + nameTable + " LIMIT 0")
        self.connection.commit()
        return ([desc[0] for desc in self.current.description])

    def createElTable(self, nameTable: str, values: tuple):
        self.current.execute(
            "INSERT INTO {} ({}) VALUES {}".format(nameTable, ", ".join(self.getTableColums(nameTable)[1:]), values))
        self.connection.commit()
        
    def updateElTable(self, nameTable: str, condition: str, **kwargs):
        self.current.execute("UPDATE {} SET {} WHERE {}".format(
            nameTable,
            ", ".join(key+'='+value for key, value in kwargs.items()),
            condition)
         ) #updateElTable("apps", "city = 'San Francisco' AND date = '2003-07-03'", temp_lo='temp_lo+1', temp_hi='temp_lo+15')
        self.connection.commit()

    def deleteElTable(self, nameTable: str, usl: str):
        self.current.execute("DELETE FROM {} WHERE {}".format(nameTable, usl))
        self.connection.commit()

    def printEl(self, nameTable: str, orderBy='', limit=10000, ofset=0):
        helpString = ""
        for i in self.getTableColums(nameTable): helpString += i + ", "
        helpString = helpString[:len(helpString) - 2]
        if (orderBy == ''): orderBy = self.getTableColums(nameTable)[0]
        self.current.execute("SELECT {} FROM {} ORDER BY {} LIMIT {} OFFSET {}".format(
          helpString, nameTable, orderBy, limit, ofset)
        )
        array = self.current.fetchall()
        return array

    def printCurrEl(self, nameTable: str, wtfselect='*',orderBy='', limit=10000, ofset=0):
        if (orderBy == ''): orderBy = self.getTableColums(nameTable)[0]
        self.current.execute("SELECT {} FROM {} ORDER BY {} LIMIT {} OFFSET {}".format(
          wtfselect, nameTable, orderBy, limit, ofset)
        )
        array = self.current.fetchall()
        return array


#admin = Control("main", "db_creator", "12345Q", "localhost", 5432)
'''with open('data_login.csv', 'r') as csvfile:
    spamreader = csv.reader(csvfile)
    i = 1
    for row in spamreader:
        arr = row[0].split(";")
        admin.createElTable("data_login", (arr[0], arr[1], i)) #data_login.csv
        admin.createElTable("bank_info", (i, arr[0], int(arr[1]))) #bank_info.csv
        admin.createElTable("info_work", (arr[0], arr[1], arr[2])) #info_work.csv
        admin.createElTable("service", (i ,arr[0][0:25], arr[1])) #service.csv
        i += 1'''
# admin.createTable({"id": "SERIAL PRIMARY KEY" ,"login": "VARCHAR(64)",
#                   "password": "VARCHAR(64)"}, "test1")
# admin.createUserTable("users", ("cweubffw", "456123"))
# print(admin.printUsers("users"))
# admin.deleteUserTable("users", "login = '{}'".format("cweubffw"))
# print(admin.printUsers("users"))

#with open('table_data.csv', 'r') as csvfile:
#    spamreader = csv.reader(csvfile)
#    for row in spamreader:
#        arr = row[0].split(";")
#        admin.createUserTable("users", (arr[0], arr[1]))
#
#print(admin.printUsers("users"))

#admin.deleteUserTable("users", "login = 'Ludie_Steuber57@hotmail.com'")