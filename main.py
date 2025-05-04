from flet import *
import flet as ft
import requests
from datetime import datetime
import calendar

def get_month_dates():
    today = datetime.today()
    year = today.year
    month = today.month
    start_date = f"{year}-{month:02d}-01"
    last_day = calendar.monthrange(year, month)[1]
    end_date = f"{year}-{month:02d}-{last_day:02d}"
    return start_date, end_date
start_date, end_date = get_month_dates()

def main(page: Page):
    BG = '#041955'
    FWG = '#97b4ff'
    FG = '#3450a1'

    page.title = "School Management Application"
    page.bgcolor = BG
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    page.vertical_alignment = MainAxisAlignment.CENTER
    #page.window_width = 500
    #page.window_height = 800
    page.window_maximized = True
    page.window_resizable = True

    categories = [
        '🤖--> A.I 𝐿𝑒𝒸𝓉𝓊𝓇𝑒 𝒩𝑜𝓉𝑒𝓈',
        '📜--> Dairy',
        '🎓--> Exams',
        '💯--> Ranks',
        '📅-->   Attendance',
        '📝--> Assignments',
        '🎖️--> Rewards',
        '🛠️--> Projects'
    ]

    def open_drawer(e):
        page.drawer.open = True
        page.update()

    def show_category_page(name):
        global p_dsrid
        page.clean()
        page.bgcolor = "black"
        page.appbar = AppBar(
            title=Text(name),
            bgcolor=BG,
            leading=IconButton(
                icon=icons.ARROW_BACK,
                icon_color="white",
                on_click=show_main_page
            )
        )

        if name.startswith("📅"):
            try:
                response = requests.get(f"https://sd50.serveo.net/attendance/student/{p_dsrid}?start_date={start_date}&end_date={end_date}")
                if response.status_code == 200:
                    data = response.json()
                    summary = data.get("summary", {})
                    total = summary.get("total_days", 0)
                    present = summary.get("present_days", 0)
                    absent = summary.get("absent_days", 0)
                    percentage = summary.get("percentage", "0%")
                else:
                    total, present, absent, percentage = 0, 0, 0, "0%"
            except:
                total, present, absent, percentage = 0, 0, 0, "0%"

            page.add(
                Column(
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    controls=[
                        Text("📊 Attendance Overview", color="white", size=22, weight="bold"),
                        Container(height=20),
                        Row(
                            alignment=MainAxisAlignment.SPACE_EVENLY,
                            controls=[
                                Column(controls=[
                                    Text("Total Days", color=FWG),
                                    Text(str(total), color="white", weight="bold", size=16)
                                ]),
                                Column(controls=[
                                    Text("Present", color=FWG),
                                    Text(str(present), color="green", weight="bold", size=16)
                                ]),
                                Column(controls=[
                                    Text("Absent", color=FWG),
                                    Text(str(absent), color="red", weight="bold", size=16)
                                ])
                            ]
                        ),
                        Container(height=30),
                        Text("📊 Attendance Graph", color=FWG, size=18, weight="bold"),
                        Container(
                            height=200,
                            width=350,
                            content=Column(
                                spacing=10,
                                controls=[
                                    Row([
                                        Container(width=80, content=Text("Present", color="white")),
                                        ProgressBar(value=present/total if total else 0, width=200, color="green"),
                                        Text(f"{round((present/total)*100) if total else 0}%", color="green")
                                    ]),
                                    Row([
                                        Container(width=80, content=Text("Absent", color="white")),
                                        ProgressBar(value=absent/total if total else 0, width=200, color="red"),
                                        Text(f"{round((absent/total)*100) if total else 0}%", color="red")
                                    ]),
                                ]
                            )
                        )
                    ]
                )
            )
        else:
            page.add(
                Column(
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    controls=[
                        Container(height=100),
                        Text(f"You clicked on {name}", color="white", size=22, weight="bold")
                    ]
                )
            )
            
        if name.startswith("📜"):
            page.add(
                Column(
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    scroll=ScrollMode.AUTO,
                    controls=[
                        Container(height=20),
                        Text("📖 Daily Subjects Dairy", color="white", size=22, weight="bold"),
                        Container(height=20),
                        DataTable(
                            columns=[
                                DataColumn(label=Text("Subject Name", color="white")),
                                DataColumn(label=Text("Status / Note", color="white")),
                            ],
                            rows=[
                                DataRow(cells=[
                                    DataCell(Text("Telugu", color="white")),
                                    DataCell(Text("")),
                                ]),
                                DataRow(cells=[
                                    DataCell(Text("Hindi", color="white")),
                                    DataCell(Text("")),
                                ]),
                                DataRow(cells=[
                                    DataCell(Text("English", color="white")),
                                    DataCell(Text("")),
                                ]),
                                DataRow(cells=[
                                    DataCell(Text("Maths", color="white")),
                                    DataCell(Text("")),
                                ]),
                                DataRow(cells=[
                                    DataCell(Text("Science", color="white")),
                                    DataCell(Text("")),
                                ]),
                                DataRow(cells=[
                                    DataCell(Text("Social", color="white")),
                                    DataCell(Text("")),
                                ]),
                            ],
                            border=BorderSide(1, "white"),
                            heading_row_color="black",
                            data_row_color={"even": "black", "odd": "black"},
                        ),
                        Container(height=30),
                    ]
                )
            )

    def get_main_page():
        print("Frontend: main() function loaded")
        page.title = "School Management Dashboard"
        page.bgcolor = "#041955"
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.vertical_alignment = ft.MainAxisAlignment.CENTER

        welcome_text = Text(f"Welcome {p_name}! 👋", size=28, color="white", weight="bold")

        category_buttons = [
            ElevatedButton(
                text=cat,
                width=300,
                on_click=lambda e, name=cat: show_category_page(name),
                bgcolor="#3450a1",
                color="white"
            )
            for cat in categories
        ]

        page.add(
            Column(
                alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    welcome_text,
                    Container(height=30),
                    *category_buttons
                ]
            )
        )

        page.update()

    def show_main_page(e=None):
        page.controls.clear()
        get_main_page()
        page.update()

    def show_login_page(e=None):
        email_field = TextField(label="Email", width=300)
        password_field = TextField(label="Password", password=True, can_reveal_password=True, width=300)
        error_text = Text("", color="red")

        def validate_login(ev):
            nonlocal email_field, password_field
            global p_dsrid ,p_name, school_name, class_to_student, id_dsrid
            try:
                response = requests.post(
                    "https://sd50.serveo.net/login",
                    data={"email": email_field.value, "password": password_field.value}
                )
                if response.status_code == 200:
                    data = response.json()
                    p_dsrid = data.get("dsrid", "")
                    print(p_dsrid)
                    p_name = data.get("name", "")
                    print(p_name)
                    school_name = data.get("school_name", "")
                    print(school_name)
                    class_to_student = data.get("class_to_student", "")
                    print(class_to_student)
                    id_dsrid = data.get("id_dsrid", "")  
                    print(id_dsrid)
                    show_main_page()
                else:
                    error_text.value = "Invalid email or password"
            except:
                error_text.value = "Server error. Please try again."
            page.update()

        page.clean()
        page.add(
            Container(
                width=400,
                height=700,
                bgcolor=BG,
                border_radius=30,
                padding=30,
                content=Column(
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    controls=[
                        Text("Welcome Back", size=28, color="white", weight="bold"),
                        Container(height=30),
                        email_field,
                        password_field,
                        Container(height=10),
                        error_text,
                        Container(alignment=alignment.center_right, content=Text("Forgot password?", size=12, color=FWG)),
                        Container(height=30),
                        ElevatedButton("Log in", width=200, on_click=validate_login),
                        #TextButton(content=Text("Don't have an account? Sign up", color="white"), on_click=show_signup_page)
                    ]
                )
            )
        )

    def show_welcome_screen():
        page.clean()
        page.add(
            Container(
                width=400,
                height=700,
                bgcolor=BG,
                padding=30,
                content=Column(
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    controls=[
                        Text("🎓 ONlINE SCHOOL TEACHER", size=20, color="white", weight="bold"),
                        Container(height=30),
                        Text("Smart-Teacher", size=30, color="white", weight="bold"),
                        Text("Empowering young minds through smart education.", size=14, color=FWG, text_align=TextAlign.CENTER),
                        Container(height=50),
                        ElevatedButton("Log in", bgcolor="white", color=BG, on_click=show_login_page, width=200)
                    ]
                )
            )
        )
        
    def show_notification(title, message):
        def close_dialog(e):
            page.dialog.open = False
            page.update()

        page.dialog = AlertDialog(
            title=Text(title, weight="bold"),
            content=Text(message),
            actions=[
                TextButton("OK", on_click=close_dialog)
            ],
            on_dismiss=close_dialog
        )
        page.dialog.open = True
        page.update()

    show_welcome_screen()
if __name__ == "__main__":
    #ft.app(target=main)
    ft.app(target=main)
