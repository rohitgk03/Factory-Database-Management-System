import mysql.connector as sql
import streamlit as st
import pandas as pd

conn = sql.connect(host='localhost', user='root',
                   password='kulkarni03', database='factorydb')

cursor = conn.cursor()


def delete_row(table_name, row_id_column, delete_row_id):
    try:
        cursor.execute(
            f"DELETE FROM {table_name} WHERE {row_id_column} = %s", (delete_row_id,))
        conn.commit()
        st.success(
            f"Row with {row_id_column} {delete_row_id} deleted successfully.")
    except Exception as e:
        st.error(f"Error: {e}")


def add_employee_with_manager(employee_id, manager_id):
    try:
        # Define the stored procedure SQL query
        sql_query = """
            CREATE PROCEDURE InsertManagerIfNotNull(IN new_employee_id INT, IN new_manager_id INT)
            BEGIN
                IF new_manager_id IS NOT NULL THEN
                    INSERT INTO Manages (ManagerID, EmployeeID) VALUES (new_manager_id, new_employee_id);
                END IF;
            END;
        """

        # Execute the stored procedure creation query
        cursor.execute(sql_query)
        conn.commit()

        # Execute the stored procedure and insert into Employee table
        cursor.callproc('InsertManagerIfNotNull', (employee_id, manager_id))
        conn.commit()

        st.success("Employee added")
        st.session_state.add_employee = False
    except Exception as e:
        st.error(f"Error: {e}")


def employee():

    st.title("Employee Table")
    cursor.execute("SELECT * FROM Employee")
    result = cursor.fetchall()

    if result:
        df = pd.DataFrame(result, columns=["EmployeeID", "FirstName", "LastName",
                          "Address", "PhoneNo", "Email", "Position", "Salary", "Manag  erID"])
        st.dataframe(df)
    else:
        st.write("No data found in the Employee table.")

    if 'add_employee' not in st.session_state:
        st.session_state.add_employee = False

    if 'update_employee' not in st.session_state:
        st.session_state.update_employee = False

    if st.button("Update employee"):
        st.session_state.update_employee = True

    if st.session_state.update_employee:
        update_employee_id = st.number_input(
            "Enter the EmployeeID to update:", step=1)
        cursor.execute(
            "SELECT * FROM Employee WHERE EmployeeID = %s", (update_employee_id,))
        existing_data = cursor.fetchone()

        if existing_data:

            st.subheader("Existing Employee Data")
            existing_df = pd.DataFrame([existing_data], columns=["EmployeeID", "FirstName", "LastName",
                                                                 "Address", "PhoneNo", "Email", "Position", "Salary", "ManagerID"])
            st.dataframe(existing_df)

            new_first_name = st.text_input(
                "Enter the new first name", existing_data[1])
            new_last_name = st.text_input(
                "Enter the new last name", existing_data[2])
            new_address = st.text_input(
                "Enter the new address", existing_data[3])
            new_phone_no = st.text_input(
                "Enter the new phone number", existing_data[4])
            new_email = st.text_input("Enter the new email", existing_data[5])
            new_position = st.text_input(
                "Enter the new position", existing_data[6])
            new_salary = st.number_input(
                "Enter the new salary", value=int(existing_data[7]), step=1)
            new_manager_id = st.text_input(
                "Enter the new manager ID", value=(existing_data[8]))

            update_data = (new_first_name, new_last_name, new_address, new_phone_no, new_email,
                           new_position, new_salary, new_manager_id, update_employee_id)
            update_query = "UPDATE Employee SET FirstName=%s, LastName=%s, Address=%s, PhoneNo=%s, Email=%s, Position=%s, Salary=%s, ManagerID=%s WHERE EmployeeID=%s"
            if st.button("Commit"):
                try:
                    cursor.execute(update_query, update_data)
                    conn.commit()
                    st.success("Employee data updated successfully.")
                    st.session_state.update_employee = False
                except Exception as e:
                    st.error(f"Error updating data: {e}")
        else:
            st.warning(f"No data found for EmployeeID {update_employee_id}.")

    if st.button("Add employee"):
        st.session_state.add_employee = True

    if st.session_state.add_employee:
        employee_id = st.number_input("Enter the employee ID", step=1)
        first_name = st.text_input("Enter the first name")
        last_name = st.text_input("Enter the last name")
        address = st.text_input("Enter the address")
        phone_no = st.text_input("Enter the phone number")
        email = st.text_input("Enter the email")
        position = st.text_input("Enter the position")
        salary = st.number_input("Enter the salary", step=1)
        manager_id = st.text_input("Enter the manager ID", value=None)
    if st.button("Add"):
        try:
            cursor.execute("INSERT INTO Employee (EmployeeID, FirstName, LastName, Address, PhoneNo, Email, Position, Salary, ManagerID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                           (employee_id, first_name, last_name, address, phone_no, email, position, salary, manager_id))
            conn.commit()
            add_employee_with_manager(
                employee_id, manager_id)
            st.success("Employee added")
            st.session_state.add_employee = False
        except Exception as e:
            st.error(f"Error: {e}")

    st.subheader("Delete Employee Entry")
    delete_row_id = st.number_input("Enter the EmployeeID to delete:", step=1)
    delete_button = st.button("Delete")

    if delete_button:
        delete_row("Employee", "EmployeeID", delete_row_id)


def department():
    def callback():
        st.session_state.update_dept = True

    st.title("Department Table")
    cursor.execute("SELECT * FROM Department")
    result = cursor.fetchall()

    if result:
        df = pd.DataFrame(result, columns=["DepartmentID", "DepartmentName"])
        st.dataframe(df)
    else:
        st.write("No data found in the Department table.")

    if 'add_dept' not in st.session_state:
        st.session_state.add_dept = False

    if 'update_dept' not in st.session_state:
        st.session_state.update_dept = False

    if st.button("Add Department"):
        st.session_state.add_dept = True

    if st.session_state.add_dept:
        dept_id = st.number_input("Enter the department ID", step=1)
        dept_name = st.text_input("Enter the department name")
        if st.button("Add"):
            try:
                cursor.execute(
                    "INSERT INTO Department (DepartmentID, DepartmentName) VALUES (%s, %s)", (dept_id, dept_name))
                conn.commit()
                st.success("Department added")
                st.session_state.add_dept = False
            except Exception as e:
                st.error(f"Error: {e}")

    if st.button("Update Department"):
        st.session_state.update_dept = True

    if st.session_state.update_dept:
        update_dept_id = st.number_input(
            "Enter the DepartmentID to update:", step=1)
        cursor.execute(
            "SELECT * FROM Department WHERE DepartmentID = %s", (update_dept_id,))
        existing_data = cursor.fetchone()

        if existing_data:
            # Display the existing data for the user to modify
            st.subheader("Existing Department Data")
            existing_df = pd.DataFrame([existing_data], columns=[
                                       "DepartmentID", "DepartmentName"])
            st.dataframe(existing_df)

            # Allow the user to input new data
            new_dept_name = st.text_input(
                "Enter the new department name", existing_data[1])

            # Update the data in the database
            update_data = (new_dept_name, update_dept_id)
            update_query = "UPDATE Department SET DepartmentName=%s WHERE DepartmentID=%s"
            if st.button("Commit"):
                try:
                    cursor.execute(update_query, update_data)
                    conn.commit()
                    st.success("Department data updated successfully.")
                    st.session_state.update_dept = False
                except Exception as e:
                    st.error(f"Error updating data: {e}")
        else:
            st.warning(f"No data found for DepartmentID {update_dept_id}.")

    st.subheader("Delete Department Entry")
    delete_row_id = st.number_input(
        "Enter the DepartmentID to delete:", step=1)
    delete_button = st.button("Delete")

    if delete_button:
        try:
            cursor.execute(
                "DELETE FROM Department WHERE DepartmentID = %s", (delete_row_id,))
            conn.commit()
            st.success(
                f"Row with DepartmentID {delete_row_id} deleted successfully.")
        except Exception as e:
            st.error(f"Error: {e}")


def machine():
    def callback():
        st.session_state.update_machine = True

    st.title("Machine Table")
    cursor.execute("SELECT * FROM Machine")
    result = cursor.fetchall()

    if result:
        df = pd.DataFrame(result, columns=[
                          "MachineID", "MachineName", "MachineType", "InstallationDate"])
        st.dataframe(df)
    else:
        st.write("No data found in the Machine table.")

    if 'add_machine' not in st.session_state:
        st.session_state.add_machine = False

    if 'update_machine' not in st.session_state:
        st.session_state.update_machine = False

    if st.button("Add Machine"):
        st.session_state.add_machine = True

    if st.session_state.add_machine:
        machine_id = st.number_input("Enter the machine ID", step=1)
        machine_name = st.text_input("Enter the machine name")
        machine_type = st.text_input("Enter the machine type")
        installation_date = st.date_input("Enter the installation date")

        if st.button("Add"):
            try:
                cursor.execute("INSERT INTO Machine (MachineID, MachineName, MachineType, InstallationDate) VALUES (%s, %s, %s, %s)",
                               (machine_id, machine_name, machine_type, installation_date))
                conn.commit()
                st.success("Machine added")
                st.session_state.add_machine = False
            except Exception as e:
                st.error(f"Error: {e}")

    if st.button("Update Machine"):
        st.session_state.update_machine = True

    if st.session_state.update_machine:
        update_machine_id = st.number_input(
            "Enter the MachineID to update:", step=1)
        cursor.execute(
            "SELECT * FROM Machine WHERE MachineID = %s", (update_machine_id,))
        existing_data = cursor.fetchone()

        if existing_data:
            # Display the existing data for the user to modify
            st.subheader("Existing Machine Data")
            existing_df = pd.DataFrame([existing_data], columns=[
                "MachineID", "MachineName", "MachineType", "InstallationDate"])
            st.dataframe(existing_df)

            # Allow the user to input new data
            new_machine_name = st.text_input(
                "Enter the new machine name", existing_data[1])
            new_machine_type = st.text_input(
                "Enter the new machine type", existing_data[2])
            new_installation_date = st.date_input(
                "Enter the new installation date", existing_data[3])

            # Update the data in the database
            update_data = (new_machine_name, new_machine_type,
                           new_installation_date, update_machine_id)
            update_query = "UPDATE Machine SET MachineName=%s, MachineType=%s, InstallationDate=%s WHERE MachineID=%s"
            if st.button("Commit"):
                try:
                    cursor.execute(update_query, update_data)
                    conn.commit()
                    st.success("Machine data updated successfully.")
                    st.session_state.update_machine = False
                except Exception as e:
                    st.error(f"Error updating data: {e}")
        else:
            st.warning(f"No data found for MachineID {update_machine_id}.")

    # Add delete functionality
    st.subheader("Delete Machine Entry")
    delete_row_id = st.number_input("Enter the MachineID to delete:", step=1)
    delete_button = st.button("Delete")

    if delete_button:
        delete_row("Machine", "MachineID", delete_row_id)


def product():
    def callback():
        st.session_state.update_product = True

    st.title("Product Table")
    cursor.execute("SELECT * FROM Product")
    result = cursor.fetchall()

    if result:
        df = pd.DataFrame(
            result, columns=["ProductID", "ProductName", "Description", "Price"])
        st.dataframe(df)
    else:
        st.write("No data found in the Product table.")

    if 'add_product' not in st.session_state:
        st.session_state.add_product = False

    if 'update_product' not in st.session_state:
        st.session_state.update_product = False

    if st.button("Add Product"):
        st.session_state.add_product = True

    if st.session_state.add_product:
        product_id = st.number_input("Enter the product ID", step=1)
        product_name = st.text_input("Enter the product name")
        description = st.text_input("Enter the description")
        price = st.number_input("Enter the price", step=1)

        if st.button("Add"):
            try:
                cursor.execute("INSERT INTO Product (ProductID, ProductName, Description, Price) VALUES (%s, %s, %s, %s)",
                               (product_id, product_name, description, price))
                conn.commit()
                st.success("Product added")
                st.session_state.add_product = False
            except Exception as e:
                st.error(f"Error: {e}")

    if st.button("Update Product"):
        st.session_state.update_product = True

    if st.session_state.update_product:
        update_product_id = st.number_input(
            "Enter the ProductID to update:", step=1)
        cursor.execute(
            "SELECT * FROM Product WHERE ProductID = %s", (update_product_id,))
        existing_data = cursor.fetchone()

        if existing_data:
            # Display the existing data for the user to modify
            st.subheader("Existing Product Data")
            existing_df = pd.DataFrame([existing_data], columns=[
                "ProductID", "ProductName", "Description", "Price"])
            st.dataframe(existing_df)

            # Allow the user to input new data
            new_product_name = st.text_input(
                "Enter the new product name", existing_data[1])
            new_description = st.text_input(
                "Enter the new description", existing_data[2])
            new_price = st.number_input(
                "Enter the new price", value=float(existing_data[3]), step=1.0)

            # Update the data in the database
            update_data = (new_product_name, new_description,
                           new_price, update_product_id)
            update_query = "UPDATE Product SET ProductName=%s, Description=%s, Price=%s WHERE ProductID=%s"
            if st.button("Commit"):
                try:
                    cursor.execute(update_query, update_data)
                    conn.commit()
                    st.success("Product data updated successfully.")
                    st.session_state.update_product = False
                except Exception as e:
                    st.error(f"Error updating data: {e}")
        else:
            st.warning(f"No data found for ProductID {update_product_id}.")

    # Add delete functionality
    st.subheader("Delete Product Entry")
    delete_row_id = st.number_input("Enter the ProductID to delete:", step=1)
    delete_button = st.button("Delete")

    if delete_button:
        delete_row("Product", "ProductID", delete_row_id)


def users():
    st.title("Users Table")
    cursor.execute("SELECT * FROM Users")
    result = cursor.fetchall()

    if result:
        df = pd.DataFrame(result, columns=[
                          "CustomerID", "CustomerName", "ContactNo", "Password", "Time_of_Signup"])
        st.dataframe(df)
    else:
        st.write("No data found in the Users table.")

    if 'add_user' not in st.session_state:
        st.session_state.add_user = False

    if st.button("add user"):
        st.session_state.add_user = True

    if st.session_state.add_user:
        customer_name = st.text_input("Enter the customer name")
        contact_no = st.text_input("Enter the contact number")
        password = st.text_input("Enter the password", type="password")

        if st.button("add"):
            try:
                cursor.execute("INSERT INTO Users (CustomerName, ContactNo, Pass_word, Time_of_Signup) VALUES (%s, %s, %s, NOW())",
                               (customer_name, contact_no, password))
                conn.commit()
                st.success("User added")
                st.session_state.add_user = False
            except Exception as e:
                st.error(f"Error: {e}")
    # Add delete functionality
    st.subheader("Delete Users Entry")
    delete_row_id = st.number_input("Enter the CustomerID to delete:", step=1)
    delete_button = st.button("Delete")

    if delete_button:
        delete_row("Users", "CustomerID", delete_row_id)

def orders():
    st.title("Orders Table")
    cursor.execute("SELECT * FROM Orders")
    result = cursor.fetchall()

    if result:
        df = pd.DataFrame(
            result, columns=["OrderID", "ProductID", "CustomerID", "TotalAmount", "Price", "OrderDate"])
        st.dataframe(df)
    else:
        st.write("No data found in the Orders table.")

    st.subheader("Delete Orders Entry")
    delete_row_id = st.number_input("Enter the OrderID to delete:", step=1)
    delete_button = st.button("Delete")

    if delete_button:
        delete_row("Orders", "OrderID", delete_row_id)

    st.subheader("View Orders on a Specific Date")
    specific_date = st.date_input("Enter a specific date:")
    view_button = st.button("View Orders on this Date")

    if view_button:
        formatted_date = specific_date.strftime('%Y-%m-%d')
        cursor.execute("SELECT * FROM Orders WHERE DATE(OrderDate) = %s", (formatted_date,))
        orders_on_date = cursor.fetchall()

        if orders_on_date:
            df_date = pd.DataFrame(
                orders_on_date, columns=["OrderID", "ProductID", "CustomerID", "TotalAmount", "Price", "OrderDate"])
            st.dataframe(df_date)
        else:
            st.write("No orders found for this date.")

def supplier():
    st.title("Supplier Table")
    cursor.execute("SELECT * FROM Supplier")
    result = cursor.fetchall()

    if result:
        df = pd.DataFrame(result, columns=[
                          "SupplierID", "SupplierName", "ContactPerson", "PhoneNo", "Email"])
        st.dataframe(df)
    else:
        st.write("No data found in the Supplier table.")

    if 'add_supplier' not in st.session_state:
        st.session_state.add_supplier = False

    if st.button("add supplier"):
        st.session_state.add_supplier = True

    if st.session_state.add_supplier:
        supplier_id = st.number_input("Enter the supplier ID", step=1)
        supplier_name = st.text_input("Enter the supplier name")
        contact_person = st.text_input("Enter the contact person")
        phone_no = st.text_input("Enter the phone number")
        email = st.text_input("Enter the email")

        if st.button("add"):
            try:
                cursor.execute("INSERT INTO Supplier (SupplierID, SupplierName, ContactPerson, PhoneNo, Email) VALUES (%s, %s, %s, %s, %s)",
                               (supplier_id, supplier_name, contact_person, phone_no, email))
                conn.commit()
                st.success("Supplier added")
                st.session_state.add_supplier = False
            except Exception as e:
                st.error(f"Error: {e}")
    # Add delete functionality
    st.subheader("Delete Supplies Entry")
    delete_row_id = st.number_input("Enter the SupplierID to delete:", step=1)
    delete_button = st.button("Delete")

    if delete_button:
        delete_row("Supplies", "SupplierID", delete_row_id)


def works_in():
    st.title("WorksIn Table")
    cursor.execute("SELECT * FROM WorksIn")
    result = cursor.fetchall()

    if result:
        df = pd.DataFrame(result, columns=["EmployeeID", "DepartmentID"])
        st.dataframe(df)
    else:
        st.write("No data found in the WorksIn table.")

    if 'add_works_in' not in st.session_state:
        st.session_state.add_works_in = False

    if st.button("add works_in"):
        st.session_state.add_works_in = True

    if st.session_state.add_works_in:
        employee_id = st.number_input("Enter the employee ID", step=1)
        department_id = st.number_input("Enter the department ID", step=1)

        if st.button("add"):
            try:
                cursor.execute("INSERT INTO WorksIn (EmployeeID, DepartmentID) VALUES (%s, %s)",
                               (employee_id, department_id))
                conn.commit()
                st.success("WorksIn added")
                st.session_state.add_works_in = False
            except Exception as e:
                st.error(f"Error: {e}")
    # Add delete functionality
    st.subheader("Delete WorksIn Entry")
    delete_row_id = st.number_input("Enter the EmployeeID to delete:", step=1)
    delete_button = st.button("Delete")

    if delete_button:
        delete_row("WorksIn", "EmployeeID", delete_row_id)


def manages():
    st.title("Manages Table")
    cursor.execute("SELECT * FROM Manages")
    result = cursor.fetchall()

    if result:
        df = pd.DataFrame(result, columns=["ManagerID", "EmployeeID"])
        st.dataframe(df)
    else:
        st.write("No data found in the Manages table.")

    if 'add_manages' not in st.session_state:
        st.session_state.add_manages = False

    if st.button("add manages"):
        st.session_state.add_manages = True

    if st.session_state.add_manages:
        manager_id = st.number_input("Enter the manager ID", step=1)
        employee_id = st.number_input("Enter the employee ID", step=1)

        if st.button("add"):
            try:
                cursor.execute("INSERT INTO Manages (ManagerID, EmployeeID) VALUES (%s, %s)",
                               (manager_id, employee_id))
                conn.commit()
                st.success("Manages added")
                st.session_state.add_manages = False
            except Exception as e:
                st.error(f"Error: {e}")

    # Add delete functionality
    st.subheader("Delete Manages Entry")
    delete_row_id = st.number_input("Enter the ManagerID to delete:", step=1)
    delete_button = st.button("Delete")

    if delete_button:
        delete_row("Manages", "ManagerID", delete_row_id)


def uses():
    st.title("Uses Table")
    cursor.execute("SELECT * FROM Uses")
    result = cursor.fetchall()

    if result:
        df = pd.DataFrame(
            result, columns=["DepartmentID", "MachineID", "UsageStartDate"])
        st.dataframe(df)
    else:
        st.write("No data found in the Uses table.")

    if 'add_uses' not in st.session_state:
        st.session_state.add_uses = False

    if st.button("add uses"):
        st.session_state.add_uses = True

    if st.session_state.add_uses:
        department_id = st.number_input("Enter the department ID", step=1)
        machine_id = st.number_input("Enter the machine ID", step=1)
        usage_start_date = st.date_input("Enter the usage start date")

        if st.button("add"):
            try:
                cursor.execute("INSERT INTO Uses (DepartmentID, MachineID, UsageStartDate) VALUES (%s, %s, %s)",
                               (department_id, machine_id, usage_start_date))
                conn.commit()
                st.success("Uses added")
                st.session_state.add_uses = False
            except Exception as e:
                st.error(f"Error: {e}")
    # Add delete functionality
    st.subheader("Delete Uses Entry")
    delete_row_id = st.number_input(
        "Enter the DepartmentID to delete:", step=1)
    delete_button = st.button("Delete")

    if delete_button:
        delete_row("Uses", "DepartmentID", delete_row_id)


def produces():
    st.title("Produces Table")
    cursor.execute("SELECT * FROM Produces")
    result = cursor.fetchall()

    if result:
        df = pd.DataFrame(result, columns=["DepartmentID", "ProductID"])
        st.dataframe(df)
    else:
        st.write("No data found in the Produces table.")

    if 'add_produces' not in st.session_state:
        st.session_state.add_produces = False

    if st.button("add produces"):
        st.session_state.add_produces = True

    if st.session_state.add_produces:
        department_id = st.number_input("Enter the department ID", step=1)
        product_id = st.number_input("Enter the product ID", step=1)

        if st.button("add"):
            try:
                cursor.execute("INSERT INTO Produces (DepartmentID, ProductID) VALUES (%s, %s)",
                               (department_id, product_id))
                conn.commit()
                st.success("Produces added")
                st.session_state.add_produces = False
            except Exception as e:
                st.error(f"Error: {e}")
    # Add delete functionality
    st.subheader("Delete Produces Entry")
    delete_row_id = st.number_input(
        "Enter the DepartmentID to delete:", step=1)
    delete_button = st.button("Delete")

    if delete_button:
        delete_row("Produces", "DepartmentID", delete_row_id)


def supplies():
    st.title("Supplies Table")
    cursor.execute("SELECT * FROM Supplies")
    result = cursor.fetchall()

    if result:
        df = pd.DataFrame(
            result, columns=["SupplierID", "ProductID", "SupplyPrice", "SupplyDate"])
        st.dataframe(df)
    else:
        st.write("No data found in the Supplies table.")

    if 'add_supplies' not in st.session_state:
        st.session_state.add_supplies = False

    if st.button("add supplies"):
        st.session_state.add_supplies = True

    if st.session_state.add_supplies:
        supplier_id = st.number_input("Enter the supplier ID", step=1)
        product_id = st.number_input("Enter the product ID", step=1)
        supply_price = st.number_input("Enter the supply price", step=1)
        supply_date = st.date_input("Enter the supply date")

        if st.button("add"):
            try:
                cursor.execute("INSERT INTO Supplies (SupplierID, ProductID, SupplyPrice, SupplyDate) VALUES (%s, %s, %s, %s)",
                               (supplier_id, product_id, supply_price, supply_date))
                conn.commit()
                st.success("Supplies added")
                st.session_state.add_supplies = False
            except Exception as e:
                st.error(f"Error: {e}")
    # Add delete functionality
    st.subheader("Delete Supplies Entry")
    delete_row_id = st.number_input("Enter the SupplierID to delete:", step=1)
    delete_button = st.button("Delete")

    if delete_button:
        delete_row("Supplies", "SupplierID", delete_row_id)


def places():
    st.title("Places Table")
    cursor.execute("SELECT * FROM Places")
    result = cursor.fetchall()

    if result:
        df = pd.DataFrame(result, columns=["EmployeeID", "OrderID"])
        st.dataframe(df)
    else:
        st.write("No data found in the Places table.")

    if 'add_places' not in st.session_state:
        st.session_state.add_places = False

    if st.button("add places"):
        st.session_state.add_places = True

    if st.session_state.add_places:
        employee_id = st.number_input("Enter the employee ID", step=1)
        order_id = st.number_input("Enter the order ID", step=1)

        if st.button("add"):
            try:
                cursor.execute("INSERT INTO Places (EmployeeID, OrderID) VALUES (%s, %s)",
                               (employee_id, order_id))
                conn.commit()
                st.success("Places added")
                st.session_state.add_places = False
            except Exception as e:
                st.error(f"Error: {e}")

    st.subheader("Delete Places Entry")
    delete_row_id = st.number_input("Enter the EmployeeID to delete:", step=1)
    delete_button = st.button("Delete")

    if delete_button:
        delete_row("Places", "EmployeeID", delete_row_id)


def employee_department():
    st.title("Employee_Department Details using Join")

    cursor.execute("""
        SELECT 
            Employee.EmployeeID, 
            Employee.FirstName, 
            Employee.LastName,
            Employee.PhoneNo, 
            Employee.Position, 
            Manages.ManagerID, 
            WorksIn.DepartmentID,
            Department.DepartmentName
        FROM Employee
        LEFT JOIN Manages ON Employee.EmployeeID = Manages.EmployeeID
        LEFT JOIN WorksIn ON Employee.EmployeeID = WorksIn.EmployeeID
        LEFT JOIN Department ON WorksIn.DepartmentID = Department.DepartmentID
    """)
    result = cursor.fetchall()

    if result:
        df = pd.DataFrame(result, columns=["EmployeeID", "FirstName", "LastName",
                          "PhoneNo", "Position", "ManagerID", "DepartmentID", "DepartmentName"])
        st.dataframe(df)
    else:
        st.write("No data found in the Employee table.")


def product_by_Dept():
    st.title("Product Produced by Department using Join")
    cursor.execute("""
        SELECT 
            Product.ProductID, 
            Product.ProductName, 
            Product.Description,
            Product.Price,
            Produces.DepartmentID,
            Department.DepartmentName
        FROM Product
        LEFT JOIN Produces ON Product.ProductID = Produces.ProductID
        LEFT JOIN Department ON Produces.DepartmentID = Department.DepartmentID
    """)
    result = cursor.fetchall()

    if result:
        df = pd.DataFrame(result, columns=[
                          "ProductID", "ProductName", "Description", "Price", "DepartmentID", "DepartmentName"])
        st.dataframe(df)
    else:
        st.write("No data found in the Product table.")


def admin_login():
    st.title("Admin Login Page")
    if 'admin_login' not in st.session_state:
        st.session_state.admin_login = False
    if not st.session_state.admin_login:
        admin_username = st.text_input("Enter Admin Username:")
        admin_password = st.text_input(
            "Enter Admin Password:", type="password")
        if st.button("login"):
            if admin_username == 'admin' and admin_password == '123':
                st.success('successfully logged in as admin')
                st.session_state.admin_login = True
            else:
                st.error("Invalid credentials")

    if st.session_state.admin_login:
        if st.button("Logout"):
            st.session_state.admin_login = False
    if st.session_state.admin_login:
        menu = ["Employees", "Departments",
                "Machines", "Products", "Users", "Orders", "Suppliers",
                "works_in", "manages", "uses", "produces", "supplies", "places", "Employee_Dept Details", "Product_Dept Details"]
        choice = st.sidebar.selectbox("Menu", menu)
        if choice == "Employees":
            employee()
        if choice == 'Departments':
            department()
        if choice == "Machines":
            machine()
        if choice == "Products":
            product()
        if choice == "Users":
            users()
        if choice == "Orders":
            orders()
        if choice == "Suppliers":
            supplier()
        if choice == "works_in":
            works_in()
        if choice == "manages":
            manages()
        if choice == "uses":
            uses()
        if choice == "produces":
            produces()
        if choice == "supplies":
            supplies()
        if choice == "places":
            places()
        if choice == "Employee_Dept Details":
            employee_department()
        if choice == "Product_Dept Details":
            product_by_Dept()


admin_login()
