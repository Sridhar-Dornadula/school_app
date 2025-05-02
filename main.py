from flet import *
import requests
from datetime import datetime
import calendar

# Global user info variables
p_name = ""
school_name = ""
class_to_student = ""
id_dsrid = ""
p_dsrid=""

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

    def get_main_page():
        global p_dsrid
        categories_grid = Column(spacing=10)

        # build rows with 2 categories each
        for i in range(0, len(categories), 2):
            row_controls = []

            for j in range(2):
                if i + j < len(categories):
                    row_controls.append(
                        Container(
                            bgcolor=FG,
                            height=80,
                            width=210,
                            border_radius=20,
                            padding=15,
                            content=Column(
                                controls=[Text(categories[i + j], color="white", weight="bold")]
                            ),
                            on_click=lambda e, name=categories[i + j]: show_category_page(name)
                        )
                    )
            categories_grid.controls.append(Row(spacing=10, controls=row_controls))

        # Fetch attendance data here
        try:
            attendance_response = requests.get(f"https://sd50.serveo.net/attendance/student/{p_dsrid}?start_date={start_date}&end_date={end_date}")
            if attendance_response.status_code == 200:
                attendance_data = attendance_response.json()
                summary = attendance_data.get("summary", {})
                total = summary.get("total_days", 0)
                present = summary.get("present_days", 0)
                absent = summary.get("absent_days", 0)
                percentage = summary.get("percentage", "0%")
            else:
                total, present, absent, percentage = 0, 0, 0, "0%"
        except:
            total, present, absent, percentage = 0, 0, 0, "0%"

        page.appbar = AppBar(
            leading=IconButton(icon=icons.MENU, icon_color="white", on_click=open_drawer),
            title=Text(""),
            center_title=False,
            bgcolor=BG,
            actions=[
                IconButton(icon=icons.SEARCH, icon_color="white"),
                IconButton(icon=icons.NOTIFICATION_ADD_OUTLINED, icon_color="white"),
            ],
        )

        page.drawer = NavigationDrawer(
            controls=[
                Container(height=40),
                ListTile(
                    leading=CircleAvatar(
                        foreground_image_url=f"https://sd50.serveo.net/photo/{p_dsrid}",
                        radius=20,
                    ),
                    title=Text(p_name, size=16, weight="bold"),
                    subtitle=Text("paid", color="orange"),
                ),
                Divider(),
                *[
                    ListTile(leading=Icon(icon), title=Text(title))
                    for icon, title in [
                        (icons.CREDIT_CARD, "Cards"),
                        (icons.MESSAGE, "Messages"),
                        (icons.NOTIFICATIONS, "Notification"),
                        (icons.HISTORY, "Purchase History"),
                        (icons.ASSIGNMENT, "Activity History"),
                        (icons.SETTINGS, "Settings"),
                        (icons.LOCK, "Change Password"),
                        (icons.LANGUAGE, "Change Language"),
                        (icons.HELP_CENTER, "Help Center"),
                        (icons.FEEDBACK, "Feedback"),
                        (icons.POLICY, "Privacy Policy")
                    ]
                ]
            ]
        )

        return Container(
            expand=True,
            bgcolor=BG,
            border_radius=30,
            padding=padding.all(20),
            content=Column(
                expand=True,  
                scroll=ScrollMode.AUTO,  
                controls=[
                    Row(
                        vertical_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            CircleAvatar(
                                foreground_image_url=f"https://sd50.serveo.net/photo/{p_dsrid}",
                                radius=25,
                            ),
                            Container(width=10),
                            Column(
                                alignment=MainAxisAlignment.CENTER,
                                spacing=2,
                                controls=[
                                    Text(p_name, size=16, color="white", weight="bold"),
                                    Text(f"Class={class_to_student}", size=12, color=FWG)
                                ]
                            )
                        ]
                    ),
                    Container(height=20),
                    Text(f"Hi {p_name} Welcome", color="white"),
                    # Dashboard section
                    Container(
                        padding=padding.symmetric(vertical=10),
                        bgcolor=FG,
                        border_radius=15,
                        width=450,
                        content=Column(
                            horizontal_alignment=CrossAxisAlignment.START,
                            controls=[
                                Text("  📅--> 𝒜𝓉𝓉𝑒𝓃𝒹𝒶𝓃𝒸𝑒 𝒟𝒶𝓈𝒽𝒷𝑜𝒶𝓇𝒹", color="white", weight="bold", size=16),
                                Row(
                                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                                    controls=[
                                        Column(controls=[Text("  Total Days", color=FWG), Text(f"  {total}", color="white", weight="bold")]),
                                        Column(controls=[Text("Present", color=FWG), Text(f"{present}", color="white", weight="bold")]),
                                        Column(controls=[Text("Absent", color=FWG), Text(f"{absent}", color="white", weight="bold")]),
                                        Column(controls=[Text("Percentage  ", color=FWG), Text(f"{percentage}", color="white", weight="bold")]),
                                    ]
                                )
                            ]
                        )
                    ),
                    Text('CATEGORIES', color=FWG),
                    Container(
                        padding=padding.only(top=10, bottom=20),
                        content=categories_grid
                    )
                ]
            )
        )

    def show_main_page(e=None):
        page.clean()
        page.add(get_main_page())

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
                        TextButton(content=Text("Don't have an account? Sign up", color="white"), on_click=show_signup_page)
                    ]
                )
            )
        )

    def show_signup_page(e=None):
        name_field = TextField(label="Name", width=300)
        email_field = TextField(label="Email", width=300)
        password_field = TextField(label="Password", password=True, can_reveal_password=True, width=300)
        school_field = TextField(label="School", width=300)
        class_field = TextField(label="Class", width=300)
        error_text = Text("", color="red")

        def handle_signup(ev):
            try:
                response = requests.post(
                    "https://sd50.serveo.net/signup",
                    data={
                        "name": name_field.value,
                        "email": email_field.value,
                        "password": password_field.value,
                        "class_dsr": class_field.value,
                        "school_dsr": school_field.value
                    }
                )
                if response.status_code == 200:
                    show_login_page()
                else:
                    error_text.value = response.json().get("detail", "Signup failed.")
            except:
                error_text.value = "Signup failed. Server not reachable."
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
                        Text("Create Account", size=28, color="white", weight="bold"),
                        Container(height=30),
                        name_field,
                        email_field,
                        password_field,
                        school_field,
                        class_field,
                        Container(height=10),
                        error_text,
                        Container(height=30),
                        ElevatedButton("Sign up", width=200, on_click=handle_signup),
                        TextButton(content=Text("Already have an account? Log in", color="white"), on_click=show_login_page)
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
                border_radius=30,
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

    show_welcome_screen()

app(target=main, host="0.0.0.0", port=8550)
