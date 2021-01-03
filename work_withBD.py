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

    def createTable(self, arrayLines: dict, nameTable: str):
        keys = [i for i in arrayLines]
        helpString = "CREATE TABLE " + nameTable + " ("
        for i in keys:
            helpString += i + " " + arrayLines[i] + ", "
        helpString = helpString[:len(helpString) - 2]
        helpString += ")"
        self.current.execute(helpString)
        self.connection.commit()

    def getTableColums(self, nameTable: str):
        self.current.execute("SELECT * FROM " + nameTable + " LIMIT 0")
        self.connection.commit()
        return ([desc[0] for desc in self.current.description])

    def createUserTable(self, nameTable: str, values: tuple):
        self.current.execute(
            "INSERT INTO {} ({}) VALUES {}".format(nameTable, ", ".join(self.getTableColums(nameTable)[1:]), values))
        self.connection.commit()

    def deleteUserTable(self, nameTable: str, usl: str):
        self.current.execute("DELETE FROM {} WHERE {}".format(nameTable, usl))
        self.connection.commit()

    def printUsers(self, nameTable: str):
        helpString = ""
        for i in self.getTableColums(nameTable): helpString += i + ", "
        helpString = helpString[:len(helpString) - 2]
        self.current.execute("SELECT " + helpString + " FROM " + nameTable)
        array = self.current.fetchall()
        return array


#admin = Control("main", "db_creator", "12345Q", "localhost", 5432)
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