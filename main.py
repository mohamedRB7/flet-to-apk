import flet as ft
import json
import os

DATA_FILE = "products.json"

# تحميل البيانات من الملف (لو موجود)
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# حفظ البيانات في الملف
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main(page: ft.Page):
    page.title = "قارئ الباركود"
    page.window_width = 400
    page.window_height = 400
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = "light"

    data = load_data()

    barcode_input = ft.TextField(label="ادخل الباركود", autofocus=True, on_submit=lambda e: read_barcode(e))
    output_text = ft.Text(value="", size=18, color="blue")

    name_field = ft.TextField(label="اسم المنتج", visible=False)
    price_field = ft.TextField(label="السعر", visible=False)
    save_button = ft.ElevatedButton("حفظ المنتج", visible=False)

    def show_message(msg, color="blue"):
        output_text.value = msg
        output_text.color = color
        page.update()

    def read_barcode(e):
        barcode = barcode_input.value.strip()
        if not barcode:
            show_message("⚠️ الرجاء إدخال الباركود", "red")
            return

        if barcode in data:
            product = data[barcode]
            show_message(f"✅ الاسم: {product['name']} | السعر: {product['price']} جنيه", "green")
            name_field.visible = price_field.visible = save_button.visible = False
        else:
            show_message("❌ باركود جديد - أدخل البيانات لحفظ المنتج", "orange")
            name_field.visible = price_field.visible = save_button.visible = True
            name_field.value = ""
            price_field.value = ""
        page.update()

    def save_product(e):
        barcode = barcode_input.value.strip()
        name = name_field.value.strip()
        price = price_field.value.strip()

        if not (barcode and name and price):
            show_message("⚠️ من فضلك أدخل كل البيانات", "red")
            return

        data[barcode] = {"name": name, "price": price}
        save_data(data)
        show_message("💾 تم حفظ المنتج بنجاح", "green")

        name_field.visible = price_field.visible = save_button.visible = False
        page.update()

    save_button.on_click = save_product

    page.add(
        ft.Column(
            [
                ft.Text("📦 قارئ الباركود", size=22, weight=ft.FontWeight.BOLD),
                barcode_input,
                output_text,
                name_field,
                price_field,
                save_button,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

ft.app(target=main)
