import time
from random import choices
from string import digits, ascii_uppercase


def generate_random_passcode() -> str:
    """
    Generate random pass code (format "A5B4")
    :return: str: random pass code
    """
    return "".join(choices(ascii_uppercase + digits, k=4))


def send_sms(phone: str, message: str) -> None:
    """
    Send a sms message to specified phone number.
    :param phone:
    :param message:
    :return: None
    """
    time.sleep(2)
