import time

import flet_core

from products_tab import *
import manage_db as db


def main(page: ft.Page):
    page.title = "StoreMaster"
    page.window_min_width = 1200
    page.window_min_height = 650

    def set_focus(event):
        if app_tabs.selected_index == 0:
            pass
        elif app_tabs.selected_index == 1:
            pass
        elif app_tabs.selected_index == 2:
            pass
        elif app_tabs.selected_index == 3:
            ProductTab_ProductSearchTextField.focus()

    app_tabs = ft.Tabs(
        animation_duration=200,
        clip_behavior=ft.ClipBehavior.NONE,
        divider_color=ft.colors.BLUE,
        divider_height=5.0,
        indicator_thickness=6.0,
        indicator_color=ft.colors.RED,
        indicator_tab_size=True,
        label_color=ft.colors.BLUE_ACCENT,
        on_change=set_focus,
        overlay_color={
            ft.MaterialState.FOCUSED: ft.colors.BLACK,
        },
        scrollable=False,
        tabs=[
            ft.Tab(
                text="Продажа",
                icon=ft.icons.MONEY_ROUNDED,
                content=ft.Text("ПРОДАЖА"),
            ),
            ft.Tab(
                text="Приход",
                icon=ft.icons.ADD,
                content=ft.Text("ПРИХОД"),
            ),
            ft.Tab(
                text="Отчет",
                icon=ft.icons.DOCUMENT_SCANNER,
                content=ft.Text("ОТЧЕТ"),
            ),
            ft.Tab(
                text="Товары",
                icon=ft.icons.BOOK_ROUNDED,
                content=ProductsTabContentColumn,
            ),
        ],
        expand=1,
    )
    page.add(app_tabs)
    page.update()

    AddNewProductButton.on_click = \
        lambda n: open_product_edit_form(title="Новый товар", page=page)

    for row in Products_DataTable.rows:
        row.cells[-1].content.on_click = \
            lambda event, nrow=row: open_form_function(nrow, page=page)

    CancelButton.on_click = lambda n: close_product_edit_form(page)

    ProductTab_ProductSearchTextField.on_change = \
        lambda n: search_product_in_products_table(
            ProductTab_ProductSearchTextField.value,
            page
        )

    ProductTab_ProductSearchTextFieldClearIconButton.on_click = \
        lambda n: clear_product_search_text_field(page)

    BarCodeTextField.on_change = \
        lambda n: validate_save_edition_form_setting(n)
    NameTextField.on_change = \
        lambda n: validate_save_edition_form_setting(n)
    DescriptionTextField.on_change = \
        lambda n: validate_save_edition_form_setting(n)
    CostPriceTextField.on_change = \
        lambda n: validate_save_edition_form_setting(n)
    MarkupSumTextField.on_change = \
        lambda n: validate_save_edition_form_setting(n)
    MarkupPercentTextField.on_change = \
        lambda n: validate_save_edition_form_setting(n)
    PriceTextField.on_change = \
        lambda n: validate_save_edition_form_setting(n)


ft.app(target=main, web_renderer=ft.WebRenderer.HTML)
