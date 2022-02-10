from datetime import date

today = str(date.today())
print("Today's date:", today)
year = today.split("-")
print(year[0])