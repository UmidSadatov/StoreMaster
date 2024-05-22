import flet as ft
import datetime

HomeTabBarCodeOrProductFilterTextField = ft.TextField(
    "",
    label="Штрих-код или Наименование",
    width=300
)


HomeTabActionsFilterDropdown = ft.Dropdown(
    value="all",
    options=[
        ft.dropdown.Option(key="all", text="Все"),
        ft.dropdown.Option(key="sales", text="Продажи"),
        ft.dropdown.Option(key="arrivals", text="Приходы"),
        ft.dropdown.Option(key="returns", text="Возвраты")
    ],
    width=200
)

HomeTimeFilterDropdown = ft.Dropdown(
    value="today",
    options=[
        ft.dropdown.Option(key="all", text="За все время"),
        ft.dropdown.Option(key="month", text="За месяц"),
        ft.dropdown.Option(key="week", text="За неделю"),
        ft.dropdown.Option(key="today", text="За сегодня")
    ],
    width=200
)

HomeTabFilterRow = ft.Row(
    [
        HomeTabBarCodeOrProductFilterTextField,
        ft.Row([ft.Text("Операции"), HomeTabActionsFilterDropdown]),
        ft.Row([ft.Text("Период"), HomeTimeFilterDropdown])
    ],
    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
)


HomeTabContentColumn = ft.Column(
    [HomeTabFilterRow]
)

HomeTabContentContainer = ft.Container(
    HomeTabContentColumn,
    padding=20
)