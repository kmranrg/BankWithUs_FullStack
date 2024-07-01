import flet as ft
from components.primary_font import PRIMARY_FONT, ITALIC_FONT
from backend_engine import insert_into_db
from backend_engine import search_account_number_in_db
from backend_engine import get_account_balance, withdraw_from_account_balance, deposit_to_account_balance
from components.one_time_password import generate_otp
from components.notifier import send_email

bank_data = {}

def main(page: ft.Page):
    page.title = "Bank Management System"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.scroll = "auto"
    page.theme_mode = "light"

    page.fonts = {
        ITALIC_FONT: "fonts/Montserrat-Italic-VariableFont_wght.ttf",
        PRIMARY_FONT: "fonts/Montserrat-VariableFont_wght.ttf",
        "playwrite": "fonts/PlaywriteUSTrad-VariableFont_wght.ttf",
        "oswald": "fonts/Oswald-VariableFont_wght.ttf"
    }

    def main_menu_function(e):
        if main_menu_choice.value == '1':
            account_already_exists_error.visible = False
            user_not_found_error.visible = False
            new_customer_form.visible = True
            account_number_for_validation.visible = False
            user_account_validation_button.visible = False
            main_menu_error.visible = False
        elif main_menu_choice.value == '2':
            account_already_exists_error.visible = False
            new_customer_form.visible = False
            account_number_for_validation.visible = True
            user_account_validation_button.visible = True
            main_menu_error.visible = False
        else:
            account_already_exists_error.visible = False
            main_menu_error.visible = True
            new_customer_form.visible = False
            account_number_for_validation.visible = False
            user_account_validation_button.visible = False
            user_not_found_error.visible = False
        page.update()

    main_menu_choice = ft.TextField(label="Enter Choice", border_radius=20, on_submit=main_menu_function)
    account_already_exists_error = ft.Text("Account number already exists", font_family=PRIMARY_FONT, style="titleLarge", color='red')
    account_already_exists_error.visible = False

    def store_data(e):
        if search_account_number_in_db(int(account_number.value))== "Account not present in the database":
            bank_data[int(account_number.value)] = {"name":name.value, "pancard":pancard.value, "age":int(age.value), "account_type":account_type.value, "amount": int(amount.value), "account_number": int(account_number.value), "email": email.value, "otp": otp}
            customer_values = [int(account_number.value), name.value, pancard.value, int(age.value), account_type.value, int(amount.value), email.value, otp]
            insert_into_db(customer_values)
            new_customer_status.visible = True
        else:
            account_already_exists_error.visible = True
        page.update()

    name = ft.TextField(label="Enter name", border_radius=20)
    pancard= ft.TextField(label="Enter PAN card number", border_radius=20)
    age = ft.TextField(label="Enter age", border_radius=20)
    account_type = ft.TextField(label="Enter account type", border_radius=20)
    amount = ft.TextField(label="Enter amount", border_radius=20)
    account_number = ft.TextField(label="Enter account number", border_radius=20)
    email = ft.TextField(label="Enter email address", border_radius=20)
    otp = generate_otp()
    submit_customer_button = ft.ElevatedButton("Register", color='green', on_click=store_data)
    new_customer_status = ft.Text("Account created successfully!!!", font_family=PRIMARY_FONT, style="titleLarge", color='green')
    new_customer_status.visible = False

    new_customer_form = ft.Column([
        name,
        pancard,
        age,
        account_type,
        amount,
        account_number,
        email,
        ft.Container(height=5),
        submit_customer_button,
        ft.Container(height=5),
        new_customer_status,
        account_already_exists_error
    ],horizontal_alignment='center')

    new_customer_form.visible = False

    main_menu_error = ft.Text("Please enter a valid input...", font_family=PRIMARY_FONT, style="titleLarge", color='red')
    main_menu_error.visible = False


    account_number_for_validation = ft.TextField(label="confirm your account number", border_radius=20)
    account_number_for_validation.visible = False

    main_menu_button = ft.ElevatedButton("Submit", on_click=main_menu_function)
    user_not_found_error = ft.Text("Account not found in the Database", font_family=PRIMARY_FONT, style="titleLarge", color='red')
    user_not_found_error.visible = False

    def search_in_db(e):
        if search_account_number_in_db(int(account_number_for_validation.value)) == "Account Exists":
            logged_in_data.value = f"Account No.: {account_number_for_validation.value}"
            main_portal.visible = False
            user_not_found_error.visible = False
            user_portal.visible = True
        else:
            user_not_found_error.visible = True
        page.update()

    user_account_validation_button = ft.IconButton(icon=ft.icons.ADS_CLICK, on_click=search_in_db, icon_color='blue')
    user_account_validation_button.visible = False

    main_portal =ft.Column(
        [
            ft.Row([ft.Text(value="Main Menu", font_family="playwrite", style='headlineLarge', text_align="center")],alignment='center'),

            ft.Container(height=30),

            ft.Text(value="1. New Customer", font_family=PRIMARY_FONT, style="titleLarge"),
            ft.Text(value="2. Existing Customer", font_family=PRIMARY_FONT, style="titleLarge"),
            ft.Container(height=10),
            main_menu_choice,
            main_menu_button,
            ft.Container(height=5),
            ft.Row([account_number_for_validation,user_account_validation_button]),
            main_menu_error,
            user_not_found_error
            
        ]
    )

    user_portal_choice = ft.TextField(label="Enter Choice", border_radius=20)
    user_portal_result = ft.Text(font_family=PRIMARY_FONT, style="titleLarge", color='orange')
    user_portal_result.visible = False

    withdraw_amount = ft.TextField(label="amount", border_radius=20, width=100)
    deposit_amount = ft.TextField(label="amount", border_radius=20, width=100)

    def user_portal_validation(e):
        if user_portal_choice.value == '1':
            user_portal_result.value = 'Your account balance is ₹' + str(get_account_balance(int(account_number_for_validation.value)))
        elif user_portal_choice.value == '2':
            withdraw_amount.visible = True
            user_portal_result.value = 'Amount withdrawn, new account balance is ₹' + str(withdraw_from_account_balance(int(account_number_for_validation.value), int(withdraw_amount.value)))
        elif user_portal_choice.value == '3':
            deposit_amount.visible = True
            user_portal_result.value = 'Amount deposited, new account balance is ₹' + str(deposit_to_account_balance(int(account_number_for_validation.value), int(deposit_amount.value)))
        elif user_portal_choice.value == '4':
            user_portal.visible = False
            main_portal.visible = True
        else:
            user_portal_result.value = "WARNING: Invalid Choice!!!"
        user_portal_result.visible = True
        page.update()

    user_portal_submit_button = ft.ElevatedButton("Submit", on_click=user_portal_validation)
    logged_in_data = ft.Text(font_family=ITALIC_FONT, style="titleSmall", text_align='right')

    user_portal =ft.Column(
        [
            ft.Row([ft.Text(value="User Portal", font_family="playwrite", style='headlineLarge', text_align="center")]),
            logged_in_data,
            ft.Container(height=30),

            ft.Text(value="1. Check Balance", font_family=PRIMARY_FONT, style="titleLarge"),
            ft.Row([ft.Text(value="2. Withdraw", font_family=PRIMARY_FONT, style="titleLarge"),ft.Container(width=10),withdraw_amount]),
            ft.Row([ft.Text(value="3. Deposit", font_family=PRIMARY_FONT, style="titleLarge"),ft.Container(width=10),deposit_amount]),
            ft.Text(value="4. Back To Main Menu", font_family=PRIMARY_FONT, style="titleLarge"),
            ft.Container(height=10),
            user_portal_choice,
            ft.Container(height=5),
            user_portal_submit_button,
            ft.Container(height=5),
            user_portal_result
        ]
    )

    user_portal.visible = False

    main_page = ft.Row(
        [
            
            ft.Column(
                [
                    ft.Image(src="images/bank_main_page.png", height=630)
                ],
            ),
            ft.Container(width=20),
            main_portal,
            user_portal,
            new_customer_form
        ], alignment='center'
    )

    page.add(
        ft.Container(height=20),
        main_page
    )

ft.app(target=main, view=ft.WEB_BROWSER, port=9090, assets_dir="assets")