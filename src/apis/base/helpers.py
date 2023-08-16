import calendar
import mimetypes

from datetime import datetime, timedelta

from bson import ObjectId
from django.contrib.auth.base_user import BaseUserManager
from django.core.management.utils import get_random_string


def append_phone_no_with_0(phone_number: str):
    """Format Phone number to 0xxx"""
    # if phone number starts with Zero(0) and the length is 11, then replace Zero(0) with '234'
    if phone_number.startswith('0') and len(phone_number) == 11:
        return phone_number
    elif not phone_number.startswith('0') and len(phone_number) == 10:
        ph_no = f'0{phone_number}'
        return ph_no
    # If any of the above conditions do not match return Invalid Phone Number
    else:
        return phone_number


def append_country_code_with_plus(country_code: str):
    """Format Phone number to 0xxx"""
    # if country_code starts with plus(+) return it as is
    if country_code.startswith('+'):
        return country_code
    elif not country_code.startswith('+'):
        ph_no = f'+{country_code}'
        return ph_no
    # If any of the above conditions do not match return Invalid Phone Number
    else:
        return country_code


def flatten_list(data: list, depth: int = 1) -> list:
    """
    flatten list into 1d list
    """
    flat_list = []
    # Iterate through the outer list
    if depth == 1:
        for element in data:
            if isinstance(element, list):
                # If the element is an instance of list, iterate through the sublist
                for item in element:
                    flat_list.append(item)
            else:
                # else just append if it's not an instance of list
                flat_list.append(element)
        return flat_list
    elif depth == 2:
        for element in data:
            if isinstance(element, list):
                # If the element is an instance of list, iterate through the sublist
                for item in element:
                    # inspect the item if it is a list, then iterate through it
                    if isinstance(item, list):
                        for i in item:
                            flat_list.append(i)
                    else:
                        flat_list.append(item)
            else:
                # else just append if it's not an instance of list
                flat_list.append(element)
        return flat_list
    else:
        return flat_list


def generate_object_id() -> str:
    return f'{ObjectId()}'


def generate_model_id(model_prefix: str) -> str:
    return f'{model_prefix}{generate_object_id()}'


def generate_transaction_ref() -> str:
    return f'trxn_ref_{get_random_string(12)}'


def get_file_size(file) -> int | float:
    """
    :param file: file to be uploaded
    returns file size
    """
    return round((file.size / 1024 / 1000), 2)


def get_valid_file_extensions(file, valid_extensions: list) -> bool:
    """
    valid_extensions should be retrieved from TenantDocument model in the `files` app.
    return True if file is part of the supported files.
    supported file extensions are .jpg, .png, .pdf.
    NB: Admin can add more if more features are required
    """

    valid_ext_mimetypes = []
    for ext in valid_extensions:
        # get the list of valid extensions and guess the mimetypes
        if ext.startswith('.'):
            # check if the extensions saved for each file on the db startswith `.`
            m = mimetypes.guess_type(f'file{ext.lower()}')[0]
        else:
            m = mimetypes.guess_type(f'file.{ext.lower()}')[0]
        valid_ext_mimetypes.append(m)
    if mimetypes.guess_type(file)[0] in valid_ext_mimetypes:
        return True
    return False


def generate_password() -> str:
    special_chars = get_random_string(3, '!@#$%^&*(-_=+)')
    digits = get_random_string(3, '0123456789')
    random_password = BaseUserManager().make_random_password()
    generated_password = f'{random_password}{digits}{special_chars}'
    return generated_password


def send_email(email: str, payload: str):
    pass


def get_last_working_day(year, month) -> datetime:
    last_day = calendar.monthrange(year, month)[1]
    last_day_date = datetime(year, month, last_day)

    # If the last day is a weekend (Saturday or Sunday)
    if last_day_date.weekday() in (5, 6):
        # Find the last Friday (if last day is Saturday) or last Friday/Thursday (if last day is Sunday)
        if last_day_date.weekday() == 5:
            offset = 1
        else:
            offset = 2

        last_working_day = last_day_date - timedelta(days=offset)
    else:
        last_working_day = last_day_date

    return last_working_day


def main():
    year = 2023
    for month in range(1, 13):
        last_working_day = get_last_working_day(year, month)
        print(f"Last working day of {calendar.month_name[month]} {year}: {last_working_day.strftime('%Y-%m-%d')}")

if __name__ == "__main__":
    main()
