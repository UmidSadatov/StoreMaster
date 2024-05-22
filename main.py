import time

import flet_core

from products_tab import *
from home_tab import *
import manage_db as db


def main(page: ft.Page):
    page.title = "StoreMaster"
    page.window_min_width = 1200
    page.window_min_height = 650

    def set_focus(event: ft.ControlEvent):
        if app_tabs.selected_index == 0:
            pass
        elif app_tabs.selected_index == 1:
            pass
        elif app_tabs.selected_index == 2:
            pass
        elif app_tabs.selected_index == 3:
            ProductTab_ProductSearchTextField.focus()

        event.page.update()

    app_tabs = ft.Tabs(
        animation_duration=200,
        clip_behavior=ft.ClipBehavior.NONE,
        divider_color=ft.colors.BLUE,
        divider_height=5.0,
        indicator_thickness=6.0,
        indicator_color=ft.colors.RED,
        indicator_tab_size=True,
        label_color=ft.colors.BLUE_ACCENT,
        on_change=lambda event: set_focus(event),
        overlay_color=ft.colors.GREY_300,
        # overlay_color={
        #     ft.MaterialState.FOCUSED: ft.colors.BLACK,
        # },
        scrollable=False,
        tabs=[
            ft.Tab(
                text="Главное",
                icon=ft.icons.HOME,
                content=HomeTabContentContainer
            ),
            ft.Tab(
                text="Приход",
                icon=ft.icons.ADD,
                content=ft.Text("ПРИХОД"),
                visible=False
            ),
            ft.Tab(
                text="Отчет",
                icon=ft.icons.BOOK,
                content=ft.Text("ОТЧЕТ")
            ),
            ft.Tab(
                text="Товары",
                icon=ft.icons.TABLE_ROWS,
                content=ProductsTabContentColumn,
            ),
        ],
        expand=1,
    )
    page.add(app_tabs)
    page.update()


ft.app(target=main, web_renderer=ft.WebRenderer.HTML)
