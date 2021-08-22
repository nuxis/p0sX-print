import escpos.constants
import prompt_toolkit.key_binding.bindings.page_navigation
from escpos.printer import Usb
import time
from datetime import datetime

# Adapt to your needs
# find the USB device id with `lsusb`, example line: "Bus 001 Device 010: ID 0525:a700 Netchip Technology, Inc."
p = Usb(0x0525, 0xa700)  # profile="POS-5890")

# set the character encoding to get æøå to print correctly.
p.charcode('CP865')

code = "1234"  # 11 chars/nums: max size for CODE128
# p.barcode('123456789', 'CODE39')  # max length of this thing.

# vars
time_format = "%Y-%m-%d %H:%M:%S"
companyInfo = {
    'header': 'PP29 - Enigma',
    'name': 'Polar Interesseprganisasjon',
    'address': 'Kolstadgata 1, 0652 OSLO',
    'orgnr': '986 255 486',
}
dummy_order_line = {'name': 'dummy_name_burger', 'ingredients': 'mais, løk, æøå, sopp, ananas', 'message': 'dummy order message'}
dummy_order_line_list = [dummy_order_line, dummy_order_line]
dummy_order = {'id': -99999, 'order_line_list': dummy_order_line_list}
dummy_shift = {'start': datetime.now(), 'credit': 'dummy_credit', 'cash': 'dummy_cash'}


# create service: https://medium.com/codex/setup-a-python-script-as-a-service-through-systemctl-systemd-f0cc55a42267

def kitchen_print(order_id=-99999, order_line=dummy_order_line):
    print("kitchen print")

    p.set(align='center', double_width=True, double_height=True)
    p.textln('Ordre: ' + str(order_id))
    p.ln()

    p.set()
    p.textln('\tDato: ' + datetime.now().strftime(time_format))

    p.textln('\t' + order_line['name'])
    p.textln('\t' + order_line['ingredients'])  # TODO might need formatting.

    if order_line['message']:
        p.ln()
        p.textln('\t' + order_line['message'])

    barcode_print(order_id)


def customer_order_receipt(order=dummy_order):
    print_header()
    print_order(order['id'], order['order_line_list'])
    print_company_info()


def print_order(order_id=-99999, order_list=dummy_order_line_list):
    p.set(align='center')
    print("customer order")
    p.textln('OrderId: ' + str(order_id))
    p.ln()
    for o in order_list:
        p.set()
        p.textln('\tNavn:\t' + o['name'])

        if len(o['ingredients']) > 0:
            p.textln('\tIngredienser: ')

            p.set(align='right')
            p.textln(o['ingredients'])

        if len(o['message']) > 0:
            p.set()
            p.textln('\tMelding: ')

            p.set(align='right')
            p.textln(o['message'])

        p.set(align='center')
        p.textln('-----')
        p.ln()


def print_shift(name='dummy_shift', shift=dummy_shift):
    print("shift")
    p.set(align='center')
    p.textln("Shift print")
    p.set()
    p.textln('\tKasse:   ' + name)
    p.textln('\tStarted: ' + shift['start'].strftime(time_format))
    p.textln('\tNow:     ' + datetime.now().strftime(time_format))
    p.textln('\tCash:    ' + shift['cash'] + ',-')
    p.textln('\tCredit:  ' + shift['credit'] + ',-')
    p.set(align='center')
    p.textln('-----')


def print_normal():
    print("normal print")
    # TODO kvitto content here


def print_header():
    p.set(align='center')
    p.image("./pp29s.png")
    p.textln(companyInfo['header'])
    p.ln()
    print('image out')


def print_company_info():
    p.set()
    p.textln('\t' + companyInfo['name'])
    p.textln('\tAdresse: ' + companyInfo['address'])
    p.textln('\tOrgNr:   ' + companyInfo['orgnr'])
    p.textln('\tDato:    ' + datetime.now().strftime(time_format))


def barcode_print(order_id):
    p.barcode("{B" + str(order_id), "CODE128", pos="bottom", function_type="B")
    p.ln()
    p.textln('prefix: {B')
    p.textln('code: ' + str(order_id))
    p.textln('type: CODE128')
    p.textln('function type: B')
    p.ln()


customer_order_receipt()
#kitchen_print()
#print_shift()
p.cut()

# while True:
#    br_print()
#    print("Kvitto: "+code)
#    time.sleep(5)
