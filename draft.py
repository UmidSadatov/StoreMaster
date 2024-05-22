from datetime import datetime, timedelta

today = datetime.today().date()

# Список дат за последнюю неделю включая сегодняшнюю дату
last_month_dates = [today - timedelta(days=i) for i in range(30, -1, -1)]

# Выводим список дат
for date in last_month_dates:
    print(date.strftime("%d.%m.%Y"))