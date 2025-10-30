import flet as ft

def main(page: ft.Page):
    # 1. إعدادات الصفحة الأساسية
    page.title = "تطبيق Flet جميل"
    page.theme_mode = ft.ThemeMode.LIGHT  # يمكنك التبديل إلى DARK
    page.padding = 10
    page.rtl = True  # تفعيل الوضع من اليمين إلى اليسار (للعربية)

    # 2. شريط التطبيق (AppBar)
    page.appbar = ft.AppBar(
        title=ft.Text("مرحبًا بك في Flet", weight=ft.FontWeight.BOLD),
        center_title=True,
        bgcolor=ft.Colors.BLUE_600,
        actions=[
            ft.IconButton(ft.Icons.SETTINGS, tooltip="الإعدادات"),
        ]
    )

    # 3. دالة معالج النقر على الزر العائم
    def button_click(e):
        # عرض شريط رسائل (SnackBar) عند النقر
        page.snack_bar = ft.SnackBar(ft.Text("تم النقر على الزر العائم!"), duration=2000)
        page.snack_bar.open = True
        page.update()

    # 4. الزر العائم (FloatingActionButton)
    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD,
        on_click=button_click,
        bgcolor=ft.Colors.AMBER_600,
        tooltip="إضافة عنصر جديد"
    )

    # 5. محتوى الصفحة
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.MOBILE_FRIENDLY, size=80, color=ft.Colors.BLUE_600),
                    ft.Text(
                        "هذا هو تطبيق موبايل بسيط وجميل!",
                        size=20,
                        weight=ft.FontWeight.W_500,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Divider(),
                    ft.ElevatedButton(
                        text="زر أساسي",
                        icon=ft.Icons.CHECK,
                        bgcolor=ft.Colors.GREEN_400,
                        color=ft.Colors.WHITE,
                        on_click=lambda e: print("تم النقر على الزر الأساسي")
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            ),
            alignment=ft.alignment.center,
            padding=30,
        )
    )

# تشغيل التطبيق
if __name__ == "__main__":
    # ft.app(target=main) # للتشغيل كصفحة ويب
    ft.app(target=main, view=ft.AppView.FLET_APP) # للتشغيل كبرنامج سطح مكتب/تطبيق موبايل (وضع المعاينة)