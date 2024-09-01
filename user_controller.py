from flask import Flask, request, Response
from flask_cors import CORS, cross_origin

import services
import json

app = Flask(__name__)
CORS(app)


@app.post("/register")
# @cross_origin()
def register_user():
    try:
        first_name = request.form["first name"]
        last_name = request.form["last name"]
        email = request.form["email"]
        password = request.form["password"]
        phone_number = request.form["phone number"]
        contact_list = []

        response = services.create_user(first_name, last_name, email, password, phone_number, contact_list)
        if response:
            return Response(response=json.dumps({"message": "Registered Successfully"}), status=200,
                            mimetype="application/json")
        else:
            return Response(response=json.dumps({"message": "Invalid entry", "status": "Login failed"}),
                            status=406, mimetype="application/json")
    except:
        return Response(response=json.dumps({"message": "An error occurred"}),
                        status=502, mimetype="application/json")


@app.patch("/login")
def login_user():
    try:
        email = request.form.get("email")
        password = request.form.get("password")

        response = services.login_user_services(email, password)
        print(response)
        if response:
            return Response(response=json.dumps({"message": "login Successfully", "status": "online"}), status=200,
                            mimetype="application/json")
        if not response:
            return Response(response=json.dumps({"message": "please check your email or password"}), status=406,
                            mimetype="application/json")
    except:
        return Response(response=json.dumps({"message": "Error please login again !", "status": "Login failed"}),
                        status=502, mimetype="application/json")


@app.patch("/create-contact")
def create_new_contact():
    try:
        first_name = request.form["first name"]
        last_name = request.form["last name"]
        phone_number = request.form["phone number"]
        email = request.form['email']

        response = services.create_contact_services(first_name, last_name, phone_number, email)

        if response:
            return Response(response=json.dumps({"message": "Created contact successfully"}), status=201,
                            mimetype="application/json")
        if not response:
            return Response(response=json.dumps({"message": "Error creating contact, please ensure this is a new "
                                                            "contact"}), status=406,
                            mimetype="application/json")
    except:
        return Response(response=json.dumps({"message": "Error creating contact"}), status=502,
                        mimetype="application/json")

#
# @app.patch("/update-contact")
# def update_contact_from_phone_book():
#     try:
#         old_phone_number = request.form['old phone number']
#         new_phone_number = request.form['new phone number']
#
#         response = services.update_contact_from_list(old_phone_number, new_phone_number)
#         if response:
#             return Response(response=json.dumps({"message": "Contact updated successfully"}), status=200,
#                             mimetype="application/json")
#         if not response:
#             return Response(response=json.dumps({"message": "Error Updating contacts"}), status=406,
#                             mimetype="application/json")
#     except:
#         return Response(response=json.dumps({"message": "Couldn't update contact, Please try again"}), status=502,
#                         mimetype="application/json")


@app.delete("/delete-contact")
def delete_contact():
    try:
        contact_to_delete = request.form["enter_contact"]

        response = services.delete_contact_services(contact_to_delete)
        print(response)

        if response:
            return Response(response=json.dumps({"message": "Deleted contact successfully"}), status=200,
                            mimetype="application/json")
        if not response:
            return Response(response=json.dumps({"message": "Error deleting contacts"}), status=406,
                            mimetype="application/json")
    except:
        return Response(response=json.dumps({"message": "Please try again !"}), status=502,
                        mimetype="application/json")


@app.delete("/delete-all")
def delete_all_contacts():
    try:
        phone_number = request.form['phone number']
        password = request.form['password']

        response = services.delete_all_contact(phone_number, password)
        print(response)

        if response:
            return Response(response=json.dumps({"message": "All contacts deleted successfully"}), status=200,
                            mimetype="application/json")
        if not response:
            return Response(response=json.dumps({"message": "An error occurred"}), status=406,
                            mimetype="application/json")
    except:
        return Response(response=json.dumps({"message": "Please try again"}), status=506,
                        mimetype="application/json")


# @app.get('/find_contact')
# def find_contact():
#     try:


@app.get("/get-all-contacts")
def get_all_contacts():
    try:
        # phone_number = request.form['phone number']
        response = services.get_all_contacts()
        if response:
            return Response(response=json.dumps({"contacts": response}), status=200,
                            mimetype="application/json")
        if not response:
            return Response(response=json.dumps({"message": "Could not perform action"}), status=406,
                            mimetype="application/json")
    except:
        return Response(response=json.dumps({"message": "Error fetching all contacts"}), status=506,
                        mimetype="application/json")


@app.patch("/logout-user")
def logout():
    try:
        email = request.form['email']

        response = services.logout_user(email)
        print(response)

        if response:
            return Response(response=json.dumps({"message": "logged out successfully"}), status=200,
                            mimetype="application/json")
        if not response:
            return Response(response=json.dumps({"message": "something went wrong"}), status=406,
                            mimetype="application/json")
    except:
        return Response(response=json.dumps({"message": "please try again !"}), status=506,
                        mimetype="application/json")


if __name__ == '__main__':
    app.run(port=80, debug=True)
