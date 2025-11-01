import flet as ft
import json
import os

DATA_FILE = "products.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main(page: ft.Page):
    page.title = "📷 قارئ الباركود بالكاميرا"
    page.window_width = 420
    page.window_height = 600
    page.theme_mode = "light"

    data = load_data()

    # العناصر
    barcode_input = ft.TextField(label="📇 أدخل الباركود يدويًا", autofocus=True)
    output_text = ft.Text(value="", size=18, color="blue")
    name_field = ft.TextField(label="اسم المنتج", visible=False)
    price_field = ft.TextField(label="السعر", visible=False)
    save_button = ft.ElevatedButton("💾 حفظ المنتج", visible=False)

    # مكان الكاميرا (WebView)
    webview = ft.WebView(
        expand=True,
        visible=False,
        url="https://rawcdn.githack.com/mebjas/html5-qrcode/master/minified/html5-qrcode.min.js",  # مكتبة الباركود
    )

    # HTML مخصص لتشغيل الكاميرا
    camera_html = """
    <html>
    <body style='margin:0; text-align:center; background:#eee;'>
        <script src="https://unpkg.com/html5-qrcode"></script>
        <div id="reader" style="width:100%;height:350px;"></div>
        <script>
            function onScanSuccess(decodedText, decodedResult) {
                window.parent.postMessage(decodedText, "*");
            }
            const html5QrCode = new Html5Qrcode("reader");
            html5QrCode.start(
                { facingMode: "environment" },
                { fps: 10, qrbox: 250 },
                onScanSuccess
            ).catch(err => console.error(err));
        </script>
    </body>
    </html>
    """

    camera_view = ft.Html(content=camera_html, visible=False)

    # عرض رسالة
    def show_message(msg, color="blue"):
        output_text.value = msg
        output_text.color = color
        page.update()

    # قراءة الباركود
    def read_barcode(barcode):
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

    # عند الضغط على زر "قراءة"
    def manual_read(e):
        read_barcode(barcode_input.value.strip())

    # عند حفظ المنتج
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

    # فتح الكاميرا
    def open_camera(e):
        camera_view.visible = True
        show_message("📷 الكاميرا مفتوحة - وجّه الكود أمام العدسة", "blue")
        page.update()

    # إغلاق الكاميرا
    def close_camera(e):
        camera_view.visible = False
        show_message("🔒 تم إغلاق الكاميرا", "orange")
        page.update()

    save_button.on_click = save_product

    # استقبال الباركود من الكاميرا (من JavaScript)
    def on_barcode_msg(e):
        barcode_input.value = e.data
        read_barcode(e.data)

    page.on_message = on_barcode_msg

    # الأزرار
    open_btn = ft.ElevatedButton("📸 فتح الكاميرا", on_click=open_camera)
    close_btn = ft.ElevatedButton("🚫 إغلاق الكاميرا", on_click=close_camera)
    read_btn = ft.ElevatedButton("🔍 قراءة يدويًا", on_click=manual_read)

    page.add(
        ft.Column(
            [
                ft.Text("📦 قارئ الباركود", size=22, weight=ft.FontWeight.BOLD),
                barcode_input,
                ft.Row([open_btn, close_btn, read_btn], alignment=ft.MainAxisAlignment.CENTER),
                output_text,
                camera_view,
                name_field,
                price_field,
                save_button,
            ],
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

ft.app(target=main)
