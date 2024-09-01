def validate_input_for_null(firstname, lastname, email):
    if email == " " or firstname == " " or lastname == " ":
        return True
    else:
        return False


def validate_input_for_empty_space(firstname, lastname, email):
    if email == "" or firstname == "" or lastname == "":
        return True
    else:
        return False


def validate_input_for_invalid_email(email):
    if "@gmail.com" or "@email.com" in email:
        return True
    else:
        return False


def validate_phone_number(number):
    if len(number) == 11:
        return True
    else:
        return False
