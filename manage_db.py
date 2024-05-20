import sqlite3

# db_con = sqlite3.connect('ProductSales.db')
# db_con.row_factory = sqlite3.Row
# cursor = db_con.cursor()


def get_products():
    db_con = sqlite3.connect('ProductSales.db')
    db_con.row_factory = sqlite3.Row
    cursor = db_con.cursor()

    cursor.execute(
        f"""SELECT * FROM Products """
    )
    products_list = cursor.fetchall()
    db_con.commit()
    return [dict(product) for product in products_list]


def get_products_by_barcode_or_name(text: str):
    db_con = sqlite3.connect('ProductSales.db')
    db_con.row_factory = sqlite3.Row
    cursor = db_con.cursor()

    cursor.execute(
        f"""
        SELECT * FROM Products 
        WHERE barcode LIKE '{text}%'
        OR barcode LIKE '%{text}'
        OR name LIKE '{text}%'
        OR name LIKE '%{text}'
        """
    )
    products_list = cursor.fetchall()
    db_con.commit()
    return [dict(product) for product in products_list]


# mylist = get_products_by_barcode_or_name("Те")
# for d in mylist:
#     print(d)


def get_products_dict():
    db_con = sqlite3.connect('ProductSales.db')
    db_con.row_factory = sqlite3.Row
    cursor = db_con.cursor()

    cursor.execute(
        f"""SELECT * FROM Products """
    )
    products_list = cursor.fetchall()
    db_con.commit()

    products_dict = {}

    for product in products_list:
        products_dict[product['barcode']] = dict(product)

    return products_dict


def add_product(
        barcode: str,
        name: str,
        description: str,
        cost_price: str,
        markup_sum: str,
        markup_percent: str,
        final_price: str
):
    db_con = sqlite3.connect('ProductSales.db')
    db_con.row_factory = sqlite3.Row
    cursor = db_con.cursor()

    cursor.execute(
        """INSERT INTO Products 
        (barcode, name, description, cost_price, 
        markup_sum, markup_percent, final_price) 
        VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (
            barcode,
            name,
            description,
            cost_price,
            markup_sum,
            markup_percent,
            final_price
        )
    ),
    db_con.commit()


def update_product(
        id: str,
        barcode: str,
        name: str,
        description: str,
        cost_price: str,
        markup_sum: str,
        markup_percent: str,
        final_price: str
):
    db_con = sqlite3.connect('ProductSales.db')
    db_con.row_factory = sqlite3.Row
    cursor = db_con.cursor()

    cursor.execute(
        """UPDATE Products 
        SET barcode = ?, 
        name = ?, 
        description = ?, 
        cost_price = ?, 
        markup_sum = ?, 
        markup_percent = ?, 
        final_price = ? 
        WHERE id = ?
        """,
        (
            barcode,
            name,
            description,
            cost_price,
            markup_sum,
            markup_percent,
            final_price,
            id
        )
    ),
    db_con.commit()


# def search_product_by_barcode_or_name(text:str):


