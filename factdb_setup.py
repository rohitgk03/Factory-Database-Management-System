import mysql.connector
import streamlit as st
import pandas as pd


class FactoryDBSetup:
    host = "localhost"
    user = "root"
    password = "kulkarni03"
    db = "factorydb"

    def create_factory_database(self):
        # Establish a connection to the MySQL server
        db = mysql.connector.connect(
            # Host where the MySQL server is located (e.g., "localhost")
            host=self.host,
            # Username for the MySQL server (e.g., "root")
            user=self.user,
            # Port number for MySQL server (3306 is the default)
            port=3306,
            password=self.password  # Password for the MySQL user
        )

    # Create a cursor object to interact with the database
        c = db.cursor()

    # Execute an SQL command to create the database if it does not already exist
        c.execute("CREATE DATABASE IF NOT EXISTS factorydb")

    # Close the cursor to free up database resources
        c.close()

    # Close the connection to the MySQL server
        db.close()


# create_all_tables: Connects to the database and calls methods to create all required tables.


    def create_all_tables(self):
        db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.db
        )
        self.create_employee_table(db)
        self.create_department_table(db)
        self.create_machine_table(db)
        self.create_product_table(db)
        self.create_users_table(db)
        self.create_orders_table(db)
        self.create_supplier_table(db)
        self.create_works_in_table(db)
        self.create_manages_table(db)
        self.create_uses_table(db)
        self.create_produces_table(db)
        self.create_supplies_table(db)
        self.create_places_table(db)
        db.close()

    def create_employee_table(self, db):
        c = db.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS Employee (
                        EmployeeID INTEGER UNSIGNED PRIMARY KEY,
                        FirstName VARCHAR(255),
                        LastName VARCHAR(255),
                        Address VARCHAR(255),
                        PhoneNo VARCHAR(10),
                        Email VARCHAR(255),
                        Position VARCHAR(255),
                        Salary DECIMAL(10,2),
                        ManagerID INTEGER UNSIGNED,
                        FOREIGN KEY (ManagerID) REFERENCES Employee(EmployeeID)
                            ON DELETE SET NULL
                            ON UPDATE CASCADE
                    )""")
        c.close()

    def create_department_table(self, db):
        c = db.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS Department (
                        DepartmentID INTEGER PRIMARY KEY,
                        DepartmentName VARCHAR(255)
                    )""")
        c.close()

    def create_machine_table(self, db):
        c = db.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS Machine (
                        MachineID INTEGER PRIMARY KEY,
                        MachineName VARCHAR(255),
                        MachineType VARCHAR(255),
                        InstallationDate DATE
                    )""")
        c.close()

    def create_product_table(self, db):
        c = db.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS Product (
                        ProductID INTEGER PRIMARY KEY,
                        ProductName VARCHAR(255),
                        Description TEXT,
                        Price DECIMAL(10,2)
                    )""")
        c.close()

    def create_users_table(self, db):
        c = db.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS Users (
                        CustomerID INTEGER PRIMARY KEY AUTO_INCREMENT,
                        CustomerName VARCHAR(255),
                        ContactNo VARCHAR(10) UNIQUE NOT NULL,
                        Pass_word Varchar(25),
                        Time_of_Signup DATETIME
                    )""")
        c.close()

    def create_orders_table(self, db):
        c = db.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS Orders (
                        OrderID INTEGER PRIMARY KEY AUTO_INCREMENT,
                        CustomerID INTEGER,
                        ProductID INTEGER,
                        TotalAmount DECIMAL(10,2),
                        Price INTEGER,
                        OrderDate DATETIME,
                        FOREIGN KEY (CustomerID) REFERENCES Users(CustomerID)
                            ON DELETE CASCADE
                            ON UPDATE CASCADE,
                        FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
                            ON DELETE CASCADE
                            ON UPDATE CASCADE
                    )""")
        c.close()

    def create_supplier_table(self, db):
        c = db.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS Supplier (
                        SupplierID INTEGER PRIMARY KEY,
                        SupplierName VARCHAR(255),
                        ContactPerson VARCHAR(255),
                        PhoneNo VARCHAR(15),
                        Email VARCHAR(255)
                    )""")
        c.close()

    def create_works_in_table(self, db):
        c = db.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS WorksIn (
                        EmployeeID INTEGER UNSIGNED,
                        DepartmentID INTEGER,
                        PRIMARY KEY (EmployeeID, DepartmentID),
                        FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID)
                            ON DELETE CASCADE
                            ON UPDATE CASCADE,
                        FOREIGN KEY (DepartmentID) REFERENCES Department(DepartmentID)
                            ON DELETE CASCADE
                            ON UPDATE CASCADE
                    )""")
        c.close()

    def create_manages_table(self, db):
        c = db.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS Manages (
                        ManagerID INTEGER UNSIGNED,
                        EmployeeID INTEGER UNSIGNED,
                        PRIMARY KEY (ManagerID, EmployeeID),
                        FOREIGN KEY (ManagerID) REFERENCES Employee(EmployeeID)
                            ON DELETE CASCADE
                            ON UPDATE CASCADE,
                        FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID)
                            ON DELETE CASCADE
                            ON UPDATE CASCADE
                    )""")
        c.close()

    def create_uses_table(self, db):
        c = db.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS Uses (
                        DepartmentID INTEGER,
                        MachineID INTEGER,
                        UsageStartDate DATE,
                        PRIMARY KEY (DepartmentID, MachineID),
                        FOREIGN KEY (DepartmentID) REFERENCES Department(DepartmentID)
                            ON DELETE CASCADE
                            ON UPDATE CASCADE,
                        FOREIGN KEY (MachineID) REFERENCES Machine(MachineID)
                            ON DELETE CASCADE
                            ON UPDATE CASCADE
                    )""")
        c.close()

    def create_produces_table(self, db):
        c = db.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS Produces (
                        DepartmentID INTEGER,
                        ProductID INTEGER,
                        PRIMARY KEY (DepartmentID, ProductID),
                        FOREIGN KEY (DepartmentID) REFERENCES Department(DepartmentID)
                            ON DELETE CASCADE
                            ON UPDATE CASCADE,
                        FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
                            ON DELETE CASCADE
                            ON UPDATE CASCADE
                    )""")
        c.close()

    def create_supplies_table(self, db):
        c = db.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS Supplies (
                        SupplierID INTEGER,
                        ProductID INTEGER,
                        SupplyPrice DECIMAL(10,2),
                        SupplyDate DATE,
                        PRIMARY KEY (SupplierID, ProductID),
                        FOREIGN KEY (SupplierID) REFERENCES Supplier(SupplierID)
                            ON DELETE CASCADE
                            ON UPDATE CASCADE,
                        FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
                            ON DELETE CASCADE
                            ON UPDATE CASCADE
                    )""")
        c.close()

    def create_places_table(self, db):
        c = db.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS Places (
                        EmployeeID INTEGER UNSIGNED,
                        OrderID INTEGER,
                        PRIMARY KEY (EmployeeID, OrderID),
                        FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID)
                            ON DELETE CASCADE
                            ON UPDATE CASCADE,
                        FOREIGN KEY (OrderID) REFERENCES Orders(OrderID)
                            ON DELETE CASCADE
                            ON UPDATE CASCADE
                    )""")
        c.close()

    def sql_trigger(self):
        db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.db
        )
        self.before_user_insert_trigger(db)
        self.before_order_insert_trigger(db)
        self.before_employee_delete_trigger(db)

    def before_user_insert_trigger(self, db):
        c = db.cursor()
        c.execute("""CREATE TRIGGER IF NOT EXISTS before_user_insert
                    BEFORE INSERT ON Users
                    FOR EACH ROW
                    BEGIN
                    SET NEW.Time_of_signup = NOW();
                    END;
        """)
        c.close()

    def before_order_insert_trigger(self, db):
        c = db.cursor()
        c.execute("""CREATE TRIGGER IF NOT EXISTS before_order_insert
                    BEFORE INSERT ON Orders
                    FOR EACH ROW
                    BEGIN
                    SET NEW.OrderDate = NOW();
                    END;
        """)
        c.close()

    # def before_employee_delete_trigger(self, db):
    #     c = db.cursor()
    #     c.execute("""CREATE TRIGGER before_employee_delete
    #     BEFORE DELETE ON Employee
    #     FOR EACH ROW
    #     BEGIN
    #     IF OLD.EmployeeID IN (SELECT ManagerID FROM Manages) THEN
    #         SIGNAL SQLSTATE '45000'
    #         SET MESSAGE_TEXT = 'Cannot delete a manager.';
    #     END IF;
    #     END;
    #     """)
    #     c.close()

    def before_employee_delete_trigger(self, db):
        c = db.cursor()
        # Check if the trigger already exists
        c.execute("""
            SELECT COUNT(*)
            FROM information_schema.triggers
            WHERE trigger_schema = %s
            AND trigger_name = 'before_employee_delete'
        """, (self.db,))
        trigger_exists = c.fetchone()[0]

        if trigger_exists == 0:
            c.execute("""
                CREATE TRIGGER before_employee_delete
                BEFORE DELETE ON Employee
                FOR EACH ROW
                BEGIN
                    IF OLD.EmployeeID IN (SELECT ManagerID FROM Manages) THEN
                        SIGNAL SQLSTATE '45000'
                        SET MESSAGE_TEXT = 'Cannot delete a manager.';
                    END IF;
                END;
            """)
        c.close()


    def sql_function(self):
        db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.db
        )
        self.user_order_function(db)

    def user_order_function(self, db):
        c = db.cursor()
        c.execute("""
                CREATE PROCEDURE GetCustomerOrders(IN phone_number VARCHAR(10))
            BEGIN
                SELECT * FROM Orders
                WHERE CustomerID = (SELECT CustomerID FROM Users WHERE ContactNo = phone_number);
            END
        """)
        c.close()
# SELECT * FROM Orders WHERE CustomerID = (SELECT CustomerID FROM Users WHERE ContactNo = phone_number);:
# This SQL query retrieves all orders from the Orders table for the customer whose contact number matches the provided phone_number.
# It uses a nested SELECT query to find the CustomerID based on the ContactNo.


factoryDBSetup = FactoryDBSetup()
factoryDBSetup.create_factory_database()
factoryDBSetup.create_all_tables()
factoryDBSetup.sql_trigger()
factoryDBSetup.sql_function()
