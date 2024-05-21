import flet as ft
import manage_db as db
import time


def save_product(
        event: ft.ControlEvent,
        barcode: str,
        name,
        description,
        cost_price,
        markup_sum,
        markup_percent,
        final_price,
        product_id=None,
):
    try:
        if product_id is None:
            db.add_product(
                barcode=str(barcode),
                name=str(name),
                description=str(description),
                cost_price=str(cost_price),
                markup_sum=str(markup_sum),
                markup_percent=str(markup_percent),
                final_price=str(final_price)
            )
        else:
            db.update_product(
                id=product_id,
                barcode=str(barcode),
                name=str(name),
                description=str(description),
                cost_price=str(cost_price),
                markup_sum=str(markup_sum),
                markup_percent=str(markup_percent),
                final_price=str(final_price)
            )

        search_product_in_products_table(
            event,
            ProductTab_ProductSearchTextField.value,
        )

        close_product_edit_form(event)

    except:
        SavingErrorAlert.open = True
        event.page.update()
        time.sleep(3)
        SavingErrorAlert.open = False
        event.page.update()


def open_product_edit_form(
        event: ft.ControlEvent,
        title: str,
        barcode=None,
        name=None,
        description=None,
        cost_price=None,
        markup_sum=None,
        markup_percent=None,
        final_price=None,
        product_id=None
):
    page = event.page
    ProductTab_ProductSearchTextField.visible = False
    ProductsListView.visible = False
    AddNewProductButton.visible = False
    ProductTableAndButtonDivider.visible = False

    EditionColumn.visible = True

    TitleText.value = title
    BarCodeTextField.focus()

    BarCodeTextField.value = barcode if barcode is not None else ""
    NameTextField.value = name if name is not None else ""
    DescriptionTextField.value = \
        description if description is not None else ""
    CostPriceTextField.value = str(
        cost_price) if cost_price is not None else ""
    MarkupSumTextField.value = str(
        markup_sum) if markup_sum is not None else ""
    MarkupPercentTextField.value = str(
        markup_percent) if markup_percent is not None else ""
    PriceTextField.value = str(
        final_price) if final_price is not None else ""

    BarCodeTextField.error_text, NameTextField.error_text, \
        CostPriceTextField.error_text, MarkupSumTextField.error_text, \
        MarkupPercentTextField.error_text, PriceTextField.error_text = \
        None, None, None, None, None, None

    page.update()

    SaveButton.on_click = lambda event: save_product(
        event,
        barcode=str(BarCodeTextField.value),
        name=NameTextField.value,
        description=DescriptionTextField.value,
        cost_price=int(CostPriceTextField.value),
        markup_sum=int(MarkupSumTextField.value),
        markup_percent=float(MarkupPercentTextField.value),
        final_price=int(PriceTextField.value),
        product_id=int(product_id) if product_id is not None else None
    )

    page.update()


def open_form_function(event: ft.ControlEvent, row: ft.DataRow):
    spans_value_list = [
        span.text
        for span in row.cells[0].content.spans
    ]
    barcode_str = "".join(spans_value_list)
    product_dict = db.get_products_dict()[str(barcode_str)]
    # markup_sum, markup_percent =
    # re.findall(r'\d+', row.cells[4].content.value)
    open_product_edit_form(event,
                            "Редактировать товар",
                           barcode=str(product_dict['barcode']),
                           name=str(product_dict['name']),
                           description=str(
                               product_dict['description']),
                           cost_price=str(product_dict['cost_price']),
                           markup_sum=str(product_dict['markup_sum']),
                           markup_percent=str(
                               product_dict['markup_percent']),
                           final_price=str(
                               product_dict['final_price']),
                           product_id=int(product_dict['id'])
                           )


def search_product_in_products_table(event: ft.ControlEvent, text: str):
    page = event.page
    found_products = db.get_products_by_barcode_or_name(text)
    Products_DataTable.rows = make_product_table_rows_list(
        found_products,
        ProductTab_ProductSearchTextField.value
    )
    for nrow in Products_DataTable.rows:
        nrow.cells[-1].content.on_click = \
            lambda event, this_row=nrow: open_form_function(event, this_row)
    page.update()


def clear_product_search_text_field(event: ft.ControlEvent):
    ProductTab_ProductSearchTextField.value = ""
    search_product_in_products_table(event, "")
    event.page.update()


def close_product_edit_form(event: ft.ControlEvent):
    EditionColumn.visible = False

    ProductTab_ProductSearchTextField.visible = True
    ProductTab_ProductSearchTextField.focus()
    ProductsListView.visible = True
    Products_DataTable.visible = True
    ProductTableAndButtonDivider.visible = True
    AddNewProductButton.visible = True
    SaveButton.disabled = True

    event.page.update()


def is_num(n):
    try:
        float(n)
        return True
    except ValueError:
        return False


def validate_save_edition_form_setting(event: ft.ControlEvent):
    page = event.page

    if BarCodeTextField.value == "":
        BarCodeTextField.error_text = "* Введите штрих-код..."
    else:
        BarCodeTextField.error_text = None

    if NameTextField.value == "":
        NameTextField.error_text = "* Введите наименование..."
    else:
        NameTextField.error_text = None

    if CostPriceTextField.value == "":
        CostPriceTextField.error_text = "* Введите себестоимость..."
    else:
        CostPriceTextField.error_text = None

    if MarkupSumTextField.value == "":
        MarkupSumTextField.error_text = "* Введите наценку..."
    else:
        MarkupSumTextField.error_text = None

    if MarkupPercentTextField.value == "":
        MarkupPercentTextField.error_text = \
            "* Введите наценку в процентах..."
    else:
        MarkupPercentTextField.error_text = None

    if PriceTextField.value == "":
        PriceTextField.error_text = "* Введите цену..."
    else:
        PriceTextField.error_text = None

    if len(BarCodeTextField.value) and not is_num(BarCodeTextField.value):
        BarCodeTextField.error_text = "Введите штрих-код цифрами!"
        SaveButton.disabled = True

    if len(CostPriceTextField.value) and \
            not is_num(CostPriceTextField.value):
        CostPriceTextField.error_text = "Введите себестоимость цифрами!"
        SaveButton.disabled = True

    if len(MarkupSumTextField.value) and \
            not is_num(MarkupSumTextField.value):
        MarkupSumTextField.error_text = "Введите наценку цифрами!"
        SaveButton.disabled = True

    if len(MarkupPercentTextField.value) and \
            not is_num(MarkupPercentTextField.value):
        MarkupPercentTextField.error_text = \
            "Введите наценку в процентах цифрами!"
        SaveButton.disabled = True

    if len(PriceTextField.value) and \
            not is_num(PriceTextField.value):
        PriceTextField.error_text = "Введите цену цифрами!"
        SaveButton.disabled = True

    if event.control.label in ["Себестоимость", "Наценка", "Цена"]:
        if is_num(event.control.value):
            event.control.value = str(round(float(event.control.value)))
    elif event.control.label == "Наценка в процентах":
        if is_num(event.control.value):
            event.control.value = str(round(float(event.control.value), 2))

    if event.control.label == "Себестоимость" \
            and is_num(event.control.value):
        if is_num(MarkupPercentTextField.value):
            markup_sum = int(int(event.control.value) *
                             float(MarkupPercentTextField.value) / 100)
            final_price = int(event.control.value) + markup_sum
            MarkupSumTextField.value = str(markup_sum)
            PriceTextField.value = str(final_price)
        elif is_num(MarkupSumTextField.value):
            markup_percent = \
                (float(MarkupSumTextField.value) /
                 float(event.control.value)) * 100
            final_price = int(event.control.value) + \
                          int(MarkupSumTextField.value)
            MarkupPercentTextField.value = str(markup_percent)
            PriceTextField.value = str(final_price)

    elif event.control.label == "Наценка" and \
            is_num(event.control.value) and \
            is_num(CostPriceTextField.value):
        markup_percent = \
            round((float(event.control.value) /
                   float(CostPriceTextField.value)) * 100, 2)
        if int(markup_percent) == markup_percent:
            markup_percent = int(markup_percent)
        final_price = \
            int(CostPriceTextField.value) + int(event.control.value)
        MarkupPercentTextField.value = str(markup_percent)
        MarkupPercentTextField.error_text = None
        PriceTextField.value = str(final_price)
        PriceTextField.error_text = None

    elif event.control.label == "Наценка (процент)" and \
            is_num(event.control.value) and \
            is_num(CostPriceTextField.value):
        markup_sum = \
            round((float(CostPriceTextField.value) *
                   float(event.control.value)) / 100)
        final_price = int(CostPriceTextField.value) + markup_sum
        MarkupSumTextField.value = str(markup_sum)
        PriceTextField.value = str(final_price)

    elif event.control.label == "Цена" and \
            is_num(event.control.value) and \
            is_num(CostPriceTextField.value):
        markup_sum = int(event.control.value) - \
                     int(CostPriceTextField.value)
        markup_percent = \
            round((float(markup_sum) /
                   float(CostPriceTextField.value)) * 100, 2)
        if int(markup_percent) == markup_percent:
            markup_percent = round(markup_percent)
        MarkupSumTextField.value = str(markup_sum)
        MarkupPercentTextField.value = str(markup_percent)

    SaveButton.disabled = not (
            len(BarCodeTextField.value) and
            is_num(BarCodeTextField.value)
            and len(NameTextField.value)
            and len(CostPriceTextField.value) and
            is_num(CostPriceTextField.value)
            and len(MarkupSumTextField.value) and
            is_num(MarkupSumTextField.value)
            and len(MarkupPercentTextField.value) and
            is_num(MarkupPercentTextField.value)
            and len(PriceTextField.value) and
            is_num(PriceTextField.value)
    )

    page.update()


ProductTab_ProductSearchTextFieldClearIconButton = ft.IconButton(
    ft.icons.CLEAR_ROUNDED,
    icon_color=ft.colors.RED,
    bgcolor=ft.colors.GREY_200,
    hover_color=ft.colors.GREY_300,
    on_click=lambda event: clear_product_search_text_field(event)
)

ProductTab_ProductSearchTextField = ft.TextField(
    label="Товар",
    suffix=ProductTab_ProductSearchTextFieldClearIconButton,
    on_change=lambda event: search_product_in_products_table(
            event,
            ProductTab_ProductSearchTextField.value,
        )
)

ProductTab_ProductSearchRow = ft.Row(
    [
        ProductTab_ProductSearchTextField,
        ProductTab_ProductSearchTextFieldClearIconButton
    ]
)


def highlight_text_part(text, part):
    if text[:len(part)] == part and text[-len(part):] != part:
        return ft.Text(
            spans=[
                ft.TextSpan(
                    part,
                    style=ft.TextStyle(
                        bgcolor="#bbbbbb",
                    )
                ),
                ft.TextSpan(text[len(part):])
            ]
        )
    elif text[:len(part)] != part and text[-len(part):] == part:
        return ft.Text(
            spans=[
                ft.TextSpan(text[:-len(part)]),
                ft.TextSpan(
                    part,
                    style=ft.TextStyle(
                        bgcolor="#bbbbbb"
                    )
                )
            ]
        )
    elif text[:len(part)] == part and text[-len(part):] == part:
        if text != part:
            return ft.Text(
                spans=[
                    ft.TextSpan(
                        part,
                        style=ft.TextStyle(
                            bgcolor="#bbbbbb"
                        )
                    ),
                    ft.TextSpan(text[len(part):-len(part)]),
                    ft.TextSpan(
                        part,
                        style=ft.TextStyle(
                            bgcolor="#bbbbbb"
                        )
                    )
                ]
            )
        else:
            return ft.Text(
                text,
                style=ft.TextStyle(
                    bgcolor="#bbbbbb"
                )
            )
    else:
        return ft.Text(spans=[ft.TextSpan(text)])


def make_product_table_rows_list(
        product_dicts_list: list,
        highlighted_part=""
):
    return [
        ft.DataRow(
            [
                ft.DataCell(
                    highlight_text_part(
                        str(product['barcode']),
                        highlighted_part
                    )
                ),

                # ft.DataCell(ft.Text(product['name'])),

                ft.DataCell(
                    highlight_text_part(
                        str(product['name']),
                        highlighted_part
                    )
                ),

                ft.DataCell(
                    ft.Row(
                        [
                            ft.Text(
                                "" if product['description'] is None else
                                product['description'][:20] + '...'
                                if len(product['description']) > 20
                                else product['description']
                            ),
                            ft.Tooltip(
                                message=product['description'],
                                content=ft.Icon(
                                    ft.cupertino_icons.INFO_CIRCLE,
                                    color=ft.colors.BLUE
                                ),
                                padding=20,
                                margin=30,
                                text_style=ft.TextStyle(
                                    size=15,
                                    color=ft.colors.WHITE
                                ),
                                bgcolor="#555555",
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    )
                ),

                ft.DataCell(
                    ft.Text(product['cost_price'])
                ),

                ft.DataCell(
                    ft.Text(
                        f"{product['markup_sum']}   "
                        f"({product['markup_percent']}%)"
                    )
                ),

                ft.DataCell(ft.Text(product['final_price'])),

                ft.DataCell(
                    ft.Row(
                        [ft.Text(
                            product['stock_quantity'],
                            text_align=ft.TextAlign.CENTER,
                        )],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ),

                ft.DataCell(
                    ft.IconButton(
                        icon=ft.icons.EDIT_SHARP,
                        bgcolor="#ddddff"
                    )
                )

            ],
        ) for product in product_dicts_list
    ]


Products_DataTable = ft.DataTable(
    columns=[
        ft.DataColumn(
            label=ft.Text(
                "Штрих-код",
                text_align=ft.TextAlign.CENTER,
                weight=ft.FontWeight.BOLD
            )
        ),
        ft.DataColumn(
            label=ft.Text(
                "Наименование",
                text_align=ft.TextAlign.CENTER,
                weight=ft.FontWeight.BOLD
            )
        ),

        ft.DataColumn(
            label=ft.Text(
                "Описание",
                text_align=ft.TextAlign.CENTER,
                weight=ft.FontWeight.BOLD
            )
        ),

        ft.DataColumn(
            label=ft.Text(
                "Себестоимость",
                text_align=ft.TextAlign.CENTER,
                weight=ft.FontWeight.BOLD
            )
        ),

        ft.DataColumn(
            label=ft.Text(
                "Наценка",
                text_align=ft.TextAlign.CENTER,
                weight=ft.FontWeight.BOLD
            )
        ),

        ft.DataColumn(
            label=ft.Text(
                "Цена",
                text_align=ft.TextAlign.CENTER,
                weight=ft.FontWeight.BOLD
            )
        ),

        ft.DataColumn(
            label=ft.Text(
                "В наличии",
                text_align=ft.TextAlign.CENTER,
                weight=ft.FontWeight.BOLD
            )
        ),

        ft.DataColumn(label=ft.Text(""))
    ],
    heading_row_color=ft.colors.LIGHT_BLUE_ACCENT,
    rows=make_product_table_rows_list(db.get_products()),
    vertical_lines=ft.BorderSide(width=0.1),
    # horizontal_lines=ft.BorderSide(width=1),
)

ProductsListView = ft.Container(
    ft.ListView(
        [Products_DataTable],
    ),
    expand=True,
    border=ft.Border(
        top=ft.BorderSide(width=2, color="#000000"),
        bottom=ft.BorderSide(width=2, color="#000000"),
        left=ft.BorderSide(width=2, color="#000000"),
        right=ft.BorderSide(width=2, color="#000000"),
    ),
    border_radius=5,
)

AddNewProductButton = ft.ElevatedButton(
    text="Добавить новый товар",
    icon=ft.cupertino_icons.ADD_CIRCLED,
    bgcolor=ft.colors.BLUE,
    color=ft.colors.WHITE,
    height=50,
    width=300,
    on_click=lambda event: open_product_edit_form(event=event, title="Новый товар")
)

CostPriceTextField = ft.TextField(label="Себестоимость", multiline=False)
MarkupSumTextField = ft.TextField(label="Наценка", multiline=False)
MarkupPercentTextField = ft.TextField(
    label="Наценка (процент)",
    multiline=False,
    # suffix_text="%"
    suffix_icon=ft.icons.PERCENT
)
PriceTextField = ft.TextField(label="Цена", multiline=False)
SaveButton = ft.ElevatedButton(
    text="Сохранить",
    icon=ft.icons.SAVE,
    bgcolor=ft.colors.LIGHT_GREEN,
    color=ft.colors.WHITE,
    width=300,
    height=50,
    disabled=True
)

CancelButton = ft.ElevatedButton(
    text="Отмена",
    icon=ft.icons.CANCEL,
    bgcolor=ft.colors.RED,
    color=ft.colors.WHITE,
    on_click=lambda event: close_product_edit_form(event)
)

TitleText = ft.Text(
    "Редактирование товара",
    text_align=ft.TextAlign.CENTER,
    weight=ft.FontWeight.BOLD,
    size=30,
)

BarCodeTextField = ft.TextField(
    label="Штрих-код",
    multiline=False
)

NameTextField = ft.TextField(
    label="Наименование",
    multiline=False
)

DescriptionTextField = ft.TextField(
    label="Описание",
    multiline=True,
    max_lines=10,
    max_length=800
)

SavedAlert = ft.AlertDialog(
    content=ft.Text("Успешно сохранен!", text_align=ft.TextAlign.CENTER),
    icon=ft.Icon(ft.icons.CHECK),
    bgcolor=ft.colors.GREEN_100,
    surface_tint_color=ft.colors.BLUE
)

SavingErrorAlert = ft.AlertDialog(
    content=ft.Text("Ошибка при сохранении!", text_align=ft.TextAlign.CENTER),
    icon=ft.Icon(ft.icons.WARNING),
    bgcolor=ft.colors.RED_100,
    surface_tint_color=ft.colors.BLUE
)

EditionColumn = ft.Column(
    [
        TitleText,

        BarCodeTextField,
        NameTextField,
        DescriptionTextField,
        ft.Row(
            [
                CostPriceTextField,
                MarkupSumTextField,
                MarkupPercentTextField,
                PriceTextField,
            ]
        ),
        ft.Row(
            [
                SaveButton,
                CancelButton
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        ),
    ],
    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
    # alignment=ft.MainAxisAlignment.SPACE_EVENLY,
    visible=False
)

ProductTableAndButtonDivider = ft.Divider(color=ft.colors.BLACK)

ProductsTabContentColumn = ft.Column(
    [
        ProductTab_ProductSearchTextField,
        ProductsListView,
        # ProductTableAndButtonDivider,
        AddNewProductButton,
        EditionColumn,
        SavedAlert,
        SavingErrorAlert
    ],
    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
)


BarCodeTextField.on_change = \
    lambda event: validate_save_edition_form_setting(event)
NameTextField.on_change = \
    lambda event: validate_save_edition_form_setting(event)
DescriptionTextField.on_change = \
    lambda event: validate_save_edition_form_setting(event)
CostPriceTextField.on_change = \
    lambda event: validate_save_edition_form_setting(event)
MarkupSumTextField.on_change = \
    lambda event: validate_save_edition_form_setting(event)
MarkupPercentTextField.on_change = \
    lambda event: validate_save_edition_form_setting(event)
PriceTextField.on_change = \
    lambda event: validate_save_edition_form_setting(event)

for row in Products_DataTable.rows:
    row.cells[-1].content.on_click = \
        lambda event, nrow=row: open_form_function(event, nrow)



# ProductTab_ProductSearchTextField.visible = False
# ProductsListView.visible = False
# AddNewProductButton.visible = False






