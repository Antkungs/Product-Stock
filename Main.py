import PySimpleGUI as sg #ใช้ไลบรารี

class Product:#Class
    def __init__(self, name, price, quantity):#Constructor
        self.name = name
        self.price = price
        self.quantity = quantity
    

sg.theme('DarkAmber')
layout = [
    [sg.Text('ชื่อสินค้า :')],
    [sg.InputText(size=(42), key='-NAME-')],
    [sg.Text('ราคา :')],
    [sg.InputText(size=(42), key='-PRICE-')],
    [sg.Text('จำนวน :')],
    [sg.InputText(size=(42), key='-QUANTITY-')],
    [sg.Button('เพิ่มสินค้า'),sg.Button('ลบสินค้า'),sg.Button('แสดงสินค้า')],
    [sg.Button('ออกโปรแกรม')],
]#สร้างGUI

window = sg.Window('จัดการสินค้า', layout)#สร้างGUI


def add_product(name, price, quantity):#ฟังก์ชั่นเพิ่มสินค้า
    for product in products:
        if product.name == name:
            product.price = price
            product.quantity += quantity
            return
    new_product = Product(name, price, quantity)
    products.append(new_product)
    sg.popup(f"เพิ่มสินค้า : {name} , จำนวน {quantity} ชิ้นสำเร็จ", title='แจ้งเตือน')

def remove_product(name, quantity_to_remove):#ฟังก์ชั่นลบสินค้า
    for product in products:
        if product.name == name:
            if product.quantity >= quantity_to_remove:
                product.quantity -= quantity_to_remove
                if product.quantity == 0:
                    products.remove(product)
                sg.popup(f"ลบสินค้า : {name} ออกไป {(quantity_to_remove)} ชิ้นสำเร็จ", title='แจ้งเตือน')
                return
            else:
                sg.popup_error("เกิดข้อผิดพลาดกรุณาใส่จำนวนให้ถูกต้อง.",title="Error")
                return
    sg.popup_error("ไม่พบสินค้า.",title="Error")

def save_to_file():#เขียนไฟล์
    with open('productInventory.txt', 'w') as file:
        for product in products:
            file.write(f"{product.name}-{product.price}-{product.quantity}\n")

def load_from_file():#อ่านไฟล์
    listacc = []
    try:
        with open('productInventory.txt', 'r') as file:
            for line in file.readlines():
                data = line.split('-')
                name = data[0]
                price = float(data[1])
                quantity = int(data[2])
                listacc.append(Product(data[0], float(data[1]), int(data[2])))
        return listacc
    except FileNotFoundError:
        sg.popup_error("ไม่พบไฟล์.")

products = load_from_file()

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        save_to_file()
        break

    if event == 'ออกโปรแกรม':
        save_to_file()
        break

    if event == 'เพิ่มสินค้า':
        name = values['-NAME-']
        price = values['-PRICE-']
        quantity = values['-QUANTITY-']

        try:
            price = float(price)
            quantity = int(quantity)
            add_product(name, price, quantity)
            window['-NAME-'].update('')
            window['-PRICE-'].update('')
            window['-QUANTITY-'].update('')
        except ValueError:
            sg.popup_error("ข้อผิดพลาด Input.",title="Error")

    if event == 'แสดงสินค้า':
        product_list = [f'ชื่อสินค้า: {p.name} - ราคา: {p.price} บาท - จำนวน: {p.quantity} ชิ้น' for p in products]
        sg.popup_scrolled('\n'.join(product_list), size=(50, 15), title='สินค้าในระบบ')

    if event == 'ลบสินค้า':
        if values['-NAME-'] == '' or values['-QUANTITY-'] == '':
            sg.popup_error("กรุณาใส่ชื่อสินค้า และจำนวนที่ต้องการลบ.",title="Error")
        else:
            name_to_remove = values['-NAME-']
            quantity_to_remove = int(values['-QUANTITY-'])
            window['-NAME-'].update('')
            window['-QUANTITY-'].update('')
            remove_product(name_to_remove, quantity_to_remove)


window.close()
