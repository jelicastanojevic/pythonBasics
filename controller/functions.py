import pickle
import pprint
import json
import smtplib
from string import Template
from .queries import *


def can_u_log_in(un, pw, s):
    employees_un_and_pass = get_hotel_employee_un_and_pass(s)

    # pickle tuple of dictionaries, users
    output = open('users.pkl', 'wb')
    pickle.dump(employees_un_and_pass, output)
    output.close()

    pkl_file = open('users.pkl', 'rb')
    data = pickle.load(pkl_file)
    pprint.pprint(data)
    pkl_file.close()

    # json
    list_json = list(employees_un_and_pass)
    print(json.dumps(list_json, sort_keys=True, indent=4, separators=(',', ': ')))

    for e in employees_un_and_pass:
        if e['username'] == un and e['password'] == pw:
            return True
    return False


def can_u_reserve_that_room(date_from, date_to, id, s):
    return is_room_available(date_from, date_to, id, s)


def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Something is happening before the function is called.")
        func(*args, **kwargs)
        print("Something is happening after the function is called.")
    return wrapper


@my_decorator
def send_email(from_addr, to_addr_list, cc_addr_list,
               subject, message,
               login, password):

    header = 'From: %s\n' % from_addr
    header += 'To: %s\n' % ', '.join(to_addr_list)
    header += 'Cc: %s\n' % ', '.join(cc_addr_list)
    header += 'Subject: %s\n\n' % subject
    message = header + message

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(login, password)
    problems = server.sendmail(from_addr, to_addr_list, message)
    print(problems)
    server.quit()


def create_mail(name, surname, id_card, date_from, date_to, id_room, s):
    mail_content = '{} {}, with id card number: {}, reserved room number {} from {} to {}'.format(
        name, surname, id_card, id_room, date_from, date_to)

    mails = []

    while True:
        email = input('Input gmail: ')
        if(email == ''):
            break
        mails.append(email)

    send_email('jelicastanojevicc@gmail.com', mails, [], '[Reservation]',
               mail_content, 'jelicastanojevicc@gmail.com', 'asussonicmaster')

    print(mail_content)

    # templating
    mail = Template(
        '$name $surname, with id card number: $idc, reserved room number $idr from $df to $dt')
    mail.substitute(name=name, surname=surname, idc=id_card,
                    idr=id_room, df=date_from, dt=date_to)
    print(mail)

    #write in file
    file = open("reservations.txt", "w")
    file.write(mail_content)
    file.close()

    """ with open(“reservations.txt”, “w”) as f: 
        f.write(mail_content)  """


def reserve_that_room(name, surname, id_card, date_from, date_to, id_room, s):
    reserve_room(name, surname, id_card, date_from, date_to, id_room, s)


def room_exists(id, s):
    rooms = get_rooms(s)
    for r in rooms:
        if r.id == id:
            return True
    return False


def get_info_about_price(id, s):
    tax_percent = 26
    res = get_reservation(id, s)
    room_price = res.room.price*res.room.bed_number/100*(100+tax_percent)
    # fraction

    # escape charatcers
    message = '\'{0} {1}\' needs to pay {price} for this reservation'.format(
        res.guest_name, res.guest_surname, price=room_price)

    """
    message = "'{0} {1}' needs to pay {price} for this reservation".format(
        res.guest_name, res.guest_surname, price=room_price)
    raw string
    message = r'\'{0} {1}\' needs to pay {price} for this reservation'.format(
        res.guest_name, res.guest_surname, price=room_price)
    """

    print("""This should 
    print message
        on multiple 
    lines.
    :)
    """)
    return message
