import mysql.connector as sql
import streamlit as st
import pandas as pd

conn = sql.connect(host='localhost', user='root',
                   password='kulkarni03', database='factorydb')

cursor = conn.cursor()


def validate_user(phno, password):
    query = "SELECT * FROM users WHERE ContactNo = %s AND pass_word = %s"
    cursor.execute(query, (phno, password))
    result = cursor.fetchall()
    return len(result) > 0


def product():
    st.title("Product Table")
    cursor.execute("SELECT * FROM Product")
    result = cursor.fetchall()

    if result:
        df = pd.DataFrame(
            result, columns=["ProductID", "ProductName", "Description", "Price"])
        st.dataframe(df)
    else:
        st.write("No data found in the Product table.")


# customer_login()
def place_order():

    if 'add_order' not in st.session_state:
        st.session_state.add_order = False

    if st.button("add order"):
        st.session_state.add_order = True

    if st.session_state.add_order:
        # Assuming phone_no is a variable containing the phone number
        cursor.execute(
            "SELECT CustomerID FROM Users WHERE ContactNo = %s", (st.session_state.phone_no,))
        result = cursor.fetchall()
        # print(st.session_state.phone_no)
        product_id = st.number_input("Enter product_id", step=1)
        total_amount = st.text_input("Enter the total amount",value=0)
        cursor.execute("SELECT Price from Product WHERE ProductID=%s",(product_id,))
        result1=cursor.fetchone()
        if(result1):
            new_price = int(result1[0])*float(total_amount)

        if st.button("add"):
            try:
                # Assuming result is a single value, extract it before passing to the query
                customer_id = result[0][0]

                cursor.execute("INSERT INTO Orders (CustomerID, ProductID, TotalAmount,Price) VALUES (%s, %s, %s, %s)",
                               (customer_id, product_id, total_amount,new_price))
                conn.commit()
                st.success("Order added")
                st.session_state.add_order = False
            except Exception as e:
                st.error(f"Error: {e}")


def customer_orders():
    cursor.execute(
        "SELECT o.OrderID, o.CustomerID, o.ProductID, o.TotalAmount, p.Price, o.TotalAmount * p.Price AS Total_Price, o.OrderDate "
        "FROM Orders o "
        "JOIN Product p ON o.ProductID = p.ProductID "
        "WHERE o.CustomerID = (SELECT CustomerID FROM Users WHERE ContactNo = %s)",
        (st.session_state.phone_no,))
    orders_result = cursor.fetchall()
    if orders_result:
        df = pd.DataFrame(
            orders_result, columns=["OrderID", "CustomerID", "ProductID", "TotalAmount", "Price", "Total_Price", "OrderDate"])
        st.dataframe(df)
    else:
        st.write("No orders found for this customer.")

    # Calculate the sum of Total_Price from the database
    cursor.execute(
        "SELECT SUM(o.TotalAmount * p.Price) "
        "FROM Orders o "
        "JOIN Product p ON o.ProductID = p.ProductID "
        "WHERE o.CustomerID = (SELECT CustomerID FROM Users WHERE ContactNo = %s)",
        (st.session_state.phone_no,))
    total_price_sum_result = cursor.fetchone()

    if total_price_sum_result and total_price_sum_result[0] is not None:
        total_price_sum = total_price_sum_result[0]
        # st.text(f"**TOTAL: {total_price_sum}**")
        st.markdown(
            f"<b>TOTAL:</b> {round(total_price_sum, 2)}", unsafe_allow_html=True)
    else:
        st.text("No orders found for calculating the sum.")

    if 'update_order' not in st.session_state:
        st.session_state.update_order = False

    if st.button("Update order"):
        st.session_state.update_order = True

    if st.session_state.update_order:
        update_order_id = st.number_input(
            "Enter the OrderID to update:", step=1)
        cursor.execute("SELECT o.OrderID, o.CustomerID, o.ProductID, o.TotalAmount, p.Price, o.TotalAmount * p.Price AS Total_Price, o.OrderDate "
                       "FROM Orders o "
                       "JOIN Product p ON o.ProductID = p.ProductID "
                       "WHERE o.OrderID = %s",
                       (update_order_id,))
        existing_data = cursor.fetchone()
        if existing_data:
            st.subheader("Existing Order Data")
            existing_df = pd.DataFrame([existing_data], columns=[
                                       "OrderID", "CustomerID", "ProductID", "TotalAmount", "Price", "Total_Price", "OrderDate"])
            st.dataframe(existing_df)

            # UI to input new data for the order
            new_customer_id = existing_data[1]
            new_product_id = st.number_input(
                "Enter the new ProductID", value=existing_data[2], step=1)
            new_total_amount = st.text_input(
                "Enter the new TotalAmount", value=existing_data[3])
            cursor.execute("SELECT Price from Product WHERE ProductID=%s",(new_product_id,))
            result2=cursor.fetchone()
            new_price = float(result2[0])*float(new_total_amount)
            new_order_date = existing_data[5]
            new_order_date = existing_data[6]

            # Update the data in the database
            update_data = (new_customer_id, new_product_id, new_total_amount,
                           new_price, new_order_date, update_order_id)
            update_query = "UPDATE Orders SET CustomerID=%s, ProductID=%s, TotalAmount=%s, Price=%s, OrderDate=%s WHERE OrderID=%s"
            if st.button("Commit"):
                try:
                    cursor.execute(update_query, update_data)
                    conn.commit()
                    st.success("Order data updated successfully.")
                    st.session_state.update_order = False
                except Exception as e:
                    st.error(f"Error updating order data: {e}")
        else:
            st.warning(f"No data found for OrderID {update_order_id}.")

    st.subheader("Cancel Order")
    delete_row_id = st.number_input("Enter the OrderID to cancel:", step=1)
    delete_button = st.button("Delete")

    if delete_button:
        delete_row("Orders", "OrderID", delete_row_id)


def delete_row(table_name, row_id_column, delete_row_id):
    try:
        cursor.execute(
            f"DELETE FROM {table_name} WHERE {row_id_column} = %s", (delete_row_id,))
        conn.commit()
        st.success(
            f"Row with {row_id_column} {delete_row_id} deleted successfully.")
    except Exception as e:
        st.error(f"Error: {e}")


# def customer_orders():
#     cursor.execute(
#         "SELECT * FROM Orders WHERE CustomerID = (SELECT CustomerID FROM Users WHERE ContactNo = %s)", (st.session_state.phone_no,))
#     orders_result = cursor.fetchall()
#     if orders_result:
#         df = pd.DataFrame(
#             orders_result, columns=["OrderID", "CustomerID", "ProductID", "TotalAmount", "Price", "OrderDate"])
#         st.dataframe(df)
#     else:
#         st.write("No orders found for this customer.")

#     if 'update_order' not in st.session_state:
#         st.session_state.update_order = False

#     if st.button("Update order"):
#         st.session_state.update_order = True

#     if st.session_state.update_order:
#         update_order_id = st.number_input(
#             "Enter the OrderID to update:", step=1)
#         cursor.execute("SELECT * FROM Orders WHERE OrderID = %s",
#                        (update_order_id,))
#         existing_data = cursor.fetchone()
#         if existing_data:
#             st.subheader("Existing Order Data")
#             existing_df = pd.DataFrame([existing_data], columns=[
#                                        "OrderID", "CustomerID", "ProductID", "TotalAmount", "Price", "OrderDate"])
#             st.dataframe(existing_df)

#             # UI to input new data for the order
#             new_customer_id = existing_data[1]
#             new_product_id = st.number_input(
#                 "Enter the new ProductID", value=existing_data[2], step=1)
#             new_total_amount = st.text_input(
#                 "Enter the new TotalAmount", value=existing_data[3])
#             new_price = existing_data[4]
#             new_order_date = existing_data[5]

#             # Update the data in the database
#             update_data = (new_customer_id, new_product_id, new_total_amount,
#                            new_price, new_order_date, update_order_id)
#             update_query = "UPDATE Orders SET CustomerID=%s, ProductID=%s, TotalAmount=%s, Price=%s, OrderDate=%s WHERE OrderID=%s"
#             if st.button("Commit"):
#                 try:
#                     cursor.execute(update_query, update_data)
#                     conn.commit()
#                     st.success("Order data updated successfully.")
#                     st.session_state.update_order = False
#                 except Exception as e:
#                     st.error(f"Error updating order data: {e}")
#         else:
#             st.warning(f"No data found for OrderID {update_order_id}.")

#     st.subheader("Cancel Order")
#     delete_row_id = st.number_input("Enter the OrderID to cancel:", step=1)
#     delete_button = st.button("Delete")

#     if delete_button:
#         delete_row("Orders", "OrderID", delete_row_id)


# def delete_row(table_name, row_id_column, delete_row_id):
#     try:
#         cursor.execute(
#             f"DELETE FROM {table_name} WHERE {row_id_column} = %s", (delete_row_id,))
#         conn.commit()
#         st.success(
#             f"Row with {row_id_column} {delete_row_id} deleted successfully.")
#     except Exception as e:
#         st.error(f"Error: {e}")


def customer_login():
    st.title("Customer Login Page")

    if 'customer_login' not in st.session_state:
        st.session_state.customer_login = False

    if not st.session_state.customer_login:
        st.session_state.phone_no = st.text_input(
            "Enter Customer Phone Number:")
        customer_password = st.text_input(
            "Enter Customer Password:", type="password")
        if st.button("Login"):
            if validate_user(st.session_state.phone_no, customer_password):
                st.session_state.customer_login = True
            else:
                st.warning("Invalid credentials. Don't have an account? Please Sign up")

    if st.session_state.customer_login:
        if st.button("Logout"):
            st.session_state.customer_login = False
    if st.session_state.customer_login:
        menu = ["Products", "Place your Order", "Your Orders"]
        choice = st.sidebar.selectbox("Menu", menu)
        if choice == "Products":
            product()
        if choice == 'Place your Order':
            place_order()
        if choice == 'Your Orders':
            customer_orders()


customer_login()
