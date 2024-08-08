USE factorydb;

-- Insert sample data into Employee table
INSERT INTO Employee (EmployeeID, FirstName, LastName, Address, PhoneNo, Email, Position, Salary, ManagerID)
VALUES
    (1, 'John', 'Doe', '123 Main St', '1234567890', 'john.doe@email.com', 'Manager', 60000.00, NULL),
    (2, 'Jane', 'Smith', '456 Oak St', '1234567390', 'jane.smith@email.com', 'Employee', 45000.00, 1),
    (3, 'Bob', 'Johnson', '789 Pine St', '1234256790', 'bob.johnson@email.com', 'Employee', 50000.00, 1),
    (4, 'Alice', 'Williams', '101 Maple St', '1234527890', 'alice.williams@email.com', 'Manager', 70000.00, NULL),
    (5, 'Charlie', 'Brown', '202 Elm St', '1234567899', 'charlie.brown@email.com', 'Employee', 48000.00, 4);


-- Insert sample data into Department table
INSERT INTO Department (DepartmentID, DepartmentName)
VALUES
    (1, 'HR'),
    (2, 'IT'),
    (3, 'Finance'),
    (4, 'Marketing'),
    (5, 'Operations');

-- Insert sample data into Machine table
INSERT INTO Machine (MachineID, MachineName, MachineType, InstallationDate)
VALUES
    (1, 'Machine1', 'TypeA', '2023-01-01'),
    (2, 'Machine2', 'TypeB', '2023-02-01'),
    (3, 'Machine3', 'TypeC', '2023-03-01'),
    (4, 'Machine4', 'TypeD', '2023-04-01'),
    (5, 'Machine5', 'TypeE', '2023-05-01');

-- Insert sample data into Product table
INSERT INTO Product (ProductID, ProductName, Description, Price)
VALUES
    (1, 'Product1', 'Description1', 19.99),
    (2, 'Product2', 'Description2', 29.99),
    (3, 'Product3', 'Description3', 39.99),
    (4, 'Product4', 'Description4', 49.99),
    (5, 'Product5', 'Description5', 59.99);

-- Insert sample data into User table
INSERT INTO Users (CustomerID, CustomerName, ContactNo, Pass_word)
VALUES
    (1, 'Customer1', 1234567890, 'password1'),
    (2, 'Customer2', 2345678901, 'password2'),
    (3, 'Customer3', 3456789012, 'password3'),
    (4, 'Customer4', 4567890123, 'password4'),
    (5, 'Customer5', 5678901234, 'password5');

-- Insert sample data into Orders table
INSERT INTO Orders (OrderID, CustomerID, ProductID, TotalAmount,Price)
VALUES
    (1, 1, 1, 100.00, 1999),
    (2, 2, 2, 150.00, 4498.5),
    (3, 3, 3, 200.00, 7998),
    (4, 4, 3, 250.00, 9997.5),
    (5, 5, 2, 300.00, 14997);

-- Insert sample data into Supplier table
INSERT INTO Supplier (SupplierID, SupplierName, ContactPerson, PhoneNo, Email)
VALUES
    (1, 'Supplier1', 'Contact1', '555-1111', 'supplier1@email.com'),
    (2, 'Supplier2', 'Contact2', '555-2222', 'supplier2@email.com'),
    (3, 'Supplier3', 'Contact3', '555-3333', 'supplier3@email.com'),
    (4, 'Supplier4', 'Contact4', '555-4444', 'supplier4@email.com'),
    (5, 'Supplier5', 'Contact5', '555-5555', 'supplier5@email.com');

-- Insert sample data into WorksIn table
INSERT INTO WorksIn (EmployeeID, DepartmentID)
VALUES
    (1, 1),
    (2, 2),
    (3, 1),
    (4, 3),
    (5, 2);

-- Insert sample data into Manages table
INSERT INTO Manages (ManagerID, EmployeeID)
VALUES
    (1, 2),
    (1, 3),
    (4, 5),
    (4, 1),
    (4, 3);

-- Insert sample data into Uses table
INSERT INTO Uses (DepartmentID, MachineID, UsageStartDate)
VALUES
    (1, 1, '2023-01-01'),
    (2, 2, '2023-01-01'),
    (3, 3, '2023-01-01'),
    (1, 4, '2023-01-01'),
    (2, 5, '2023-01-01');

-- Insert sample data into Produces table
INSERT INTO Produces (DepartmentID, ProductID)
VALUES
    (1, 1),
    (2, 2),
    (3, 3),
    (1, 4),
    (2, 5);

-- Insert sample data into Supplies table
INSERT INTO Supplies (SupplierID, ProductID, SupplyPrice, SupplyDate)
VALUES
    (1, 1, 10.00, '2023-01-01'),
    (2, 2, 20.00, '2023-02-01'),
    (3, 3, 30.00, '2023-03-01'),
    (4, 4, 40.00, '2023-04-01'),
    (5, 5, 50.00, '2023-05-01');

-- Insert sample data into Places table
INSERT INTO Places (EmployeeID, OrderID)
VALUES
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5);
