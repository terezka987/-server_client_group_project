

def handle_client_options(user_input: str) -> int:
    """
    Test that the input is integer
    If valid return entered number
    If not valid return -1
    """
    try:
        input_num = int(user_input)

    except ValueError:
        print("Entered value is not a integer")
        return -1

    if input_num not in (0, 1, 2, 3, 4, 5):
        print("Entered value should be between 0 and 5")
        return -1
    return input_num


def handle_whether_to_encrypt(user_input: str) -> tuple:
    """
    Check whether the user has entered a boolean value
    first return value is whether we processed the input
    second return value is whether to encrypt
    """
    if user_input not in ('y', 'n'):
        print("Entered value is not 'y' or 'n', please enter one of these values")
        return (False, False)

    if user_input == 'y':
        return (True, True)
    else:
        return (True, False)


def get_password_from_user() -> str:
    """Prompt the user for a password"""
    first_entry = str()
    second_entry = str()
    while (not first_entry and not second_entry) or (first_entry != second_entry):
        first_entry = input("Enter a password to encrypt files with \n")
        second_entry = input("Re-Enter the password to encrypt files with \n")
        if first_entry != second_entry:
            print("Passwords dont match, please retry setting your password")
    return first_entry
