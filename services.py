from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from validations import validate_input_for_null
from mysql.connector import Error
from validations import validate_input_for_invalid_email
from validations import validate_input_for_empty_space
from validations import validate_phone_number
import db_utils

connection = db_utils.get_db_connection()
cursor = connection.cursor()


def create_user(first_name, last_name, email, user_password, phone_number, contact_list):
    password = generate_password_hash(user_password)
    null_input = validate_input_for_null(first_name, last_name, email)
    valid_email = validate_input_for_invalid_email(email)
    empty_space = validate_input_for_empty_space(first_name, last_name, email)
    valid_phone_number = validate_phone_number(phone_number)

    if not null_input and valid_email and not empty_space and valid_phone_number:
        try:
            user = {
                "first name:": first_name,
                "last name": last_name,
                "email": email,
                "phone number": phone_number,
                "phone book": contact_list,
                "password": password,
                "login status": "offline"
            }

            insert_user_query = """
            INSERT INTO `contact_manager` (first_name, last_name, email, password, phone_number, login_status) VALUES (%s, %s, %s, %s, %s, %s)
            """

            user_data = (first_name, last_name, email, password, phone_number, 'offline')
            cursor.execute(insert_user_query, user_data)
            connection.commit()
            return True
        except Error as e:
            print(e)
            return False
    else:
        return False


def login_user_services(email, password):
    try:
        query = """
            SELECT password, login_status
            FROM contact_manager
            WHERE email = %s
        """

        cursor.execute(query, (email,))
        result = cursor.fetchone()

        if result:
            stored_password, login_status = result

            if check_password_hash(stored_password, password):
                update_login_status(email, "online")
                return True
            else:
                return False
        else:
            return False
    except Error as e:
        print(e)
        return False


def update_login_status(email, status):
    try:
        update_query = """
        UPDATE contact_manager
        SET login_status = %s
        WHERE email = %s
        """

        cursor.execute(update_query, (status, email))
        connection.commit()

    except Error as e:
        print(e)


def create_contact_services(first_name, last_name, contact_phone_number, email):
    try:
        query = """
            SELECT id, email
            FROM contact_manager
            WHERE login_status = 'online'
        """

        cursor.execute(query)
        user = cursor.fetchone()
        user_id, user_email = user

        add_contacts = """
            INSERT INTO phone_book (user_id, first_name, last_name, phone_number, email) VALUES (%s, %s, %s, %s, %s)
        """
        contacts_data = [
            (user_id, first_name, last_name, contact_phone_number, email)
        ]
        cursor.executemany(add_contacts, contacts_data)
        connection.commit()
        if connection:
            return True
        else:
            return False
    except Error as e:
        print(e)


def get_all_contacts():
    try:
        login_status_query = """
        SELECT email
        FROM contact_manager
        WHERE login_status = 'online'
        """
        cursor.execute(login_status_query)
        online_users = cursor.fetchall()
        connection.commit()

        if online_users:
            query = """
            SELECT c.first_name, c.last_name, c.email, c.phone_number
            FROM phone_book c
            JOIN contact_manager cm ON c.user_id = cm.id
            WHERE cm.email = %s
    
            """

            all_contacts = []

            for user in online_users:
                email = user[0]
                cursor.execute(query, (email,))
                contacts = cursor.fetchall()
                all_contacts.extend(contacts)
            return all_contacts
            # connection.commit()
    except Exception as e:
        print(e)


def delete_contact_services(contact_to_delete):
    try:
        id_query = """
            SELECT id 
            FROM contact_manager 
            WHERE login_status = 'online'
        """

        cursor.execute(id_query)
        result = cursor.fetchone()
        connection.commit()
        print(result)

        if result:
            user_id = result[0]

            delete_contact_query_by_first_name = """
                DELETE FROM phone_book
                WHERE user_id = %s AND first_name = %s
            """
            cursor.execute(delete_contact_query_by_first_name, (user_id, contact_to_delete,))
            connection.commit()

            user_id = result[0]
            delete_contact_query_by_last_name = """
                DELETE FROM phone_book
                WHERE user_id = %s AND last_name = %s
                """

            cursor.execute(delete_contact_query_by_last_name, (user_id, contact_to_delete))
            connection.commit()



        # if 'first_name' == contact_to_delete:
        #     query = "DELETE FROM phone_book WHERE first_name = %s"
        #     print(query, contact_to_delete)
        #     cursor.execute(query, (contact_to_delete,))
        #     connection.commit()
        #
        # #
        # elif 'last_name' in contact_to_delete:
        #     value = contact_to_delete['last_name']
        #     query = "DELETE FROM phone_book WHERE last_name = %s"
        #     print(query, (value,))
        #     cursor.execute(query, (value,))
        #     connection.commit()
        #
        # elif 'phone_number' in contact_to_delete:
        #     value = contact_to_delete['phone_number']
        #     query = "DELETE FROM phone_book WHERE phone_number = %s"
        #     cursor.execute(query, (value,))
        #
        # elif 'email' in contact_to_delete:
        #     value = contact_to_delete['email']
        #     query = "DELETE FROM phone_book WHERE email = %s"
        #     cursor.execute(query, (value,))

        if cursor.rowcount:
            return True
    except Exception as e:
        print(e)

    # get_id_query = """
        #     SELECT id
        #     FROM contact_manager
        #     WHERE login_status = 'online'
        # """
        #
        # cursor.execute(get_id_query)
        # user_id = cursor.fetchone()
        #
        # if user_id:
        #     get_fields_query = """
        #         SELECT c.first_name, c.last_name, c.email, c.phone_number
        #         FROM phone_book c
        #         WHERE user_id = %s
        #     """
        #     cursor.execute(get_fields_query, (user_id,))
        #     contact_list = cursor.findall()
        #
        #     list_of_user_contacts = []
        #     for contacts in contact_list:
        #         user_contacts = contacts[0]
        #         list_of_user_contacts.extend(user_contacts)
        #         print(list_of_user_contacts)


def delete_all_contact(phone_number, password):
    check_contact = db.users.find_one({"login status": "online"})
    if check_contact and check_password_hash(check_contact['password'], password):
        deleted_all_contacts = db.users.update_one({"phone number": phone_number}, {"$unset": {"phone book": ""}})
        if deleted_all_contacts.modified_count > 0:
            return True
    else:
        return False


def logout_user(email):
    try:
        logout_query = """
            UPDATE contact_manager
            SET login_status = 'offline'
            WHERE email = %s        
        """

        cursor.execute(logout_query, (email,))
        connection.commit()
        cursor.close()
        if connection:
            return True
    except Exception as e:
        print(e)
# def logout_user(phone_number, password):
#     try:
#         update_query = """
#             SELECT email
#
#         """
