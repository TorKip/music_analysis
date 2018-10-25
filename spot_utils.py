def parse_date(datestring):
    months = {
        "Dec": "12",
        "Nov": "11",
        "Okt": "10",
        "Sep": "09",
        "Aug": "08",
        "Jul": "07",
        "Jun": "06",
        "May": "05",
        "Apr": "04",
        "Mar": "03",
        "Feb": "02",
        "Jan": "01"
        }
    date = datestring.split()
    year = date[2].strip(",")
    month = months[date[1]]
    day = date[0]
    time = date[3]
    new_date = "{}-{}-{} {}".format(year, month, day, time)
    return new_date