str_seconds = input("Please enter the number of seconds you wish to convert: ")
total_secs = int(str_seconds)

seconds_in_one_minute = 60
seconds_in_one_hour = seconds_in_one_minute * 60
seconds_in_one_day = seconds_in_one_hour * 24
seconds_in_one_week = seconds_in_one_hour * 24 * 7
seconds_in_one_year = seconds_in_one_day * 365


seconds_in_one_year = seconds_in_one_day * 365
output = ""

if (total_secs > seconds_in_one_year):
    years = total_secs // seconds_in_one_year
    total_secs = total_secs - (seconds_in_one_year * years)
    output = "Years= " + str(years)
if (total_secs > seconds_in_one_week):
    weeks = total_secs // seconds_in_one_week
    total_secs = total_secs - (seconds_in_one_week * weeks)
    output += "\nWeeks= " + str(weeks)
if (total_secs > seconds_in_one_day):
    days = total_secs // seconds_in_one_day
    total_secs = total_secs - (seconds_in_one_day * days)
    output += "\nDays= " + str(days)
if (total_secs > seconds_in_one_hour):
    hours = total_secs // seconds_in_one_hour
    total_secs = total_secs - (seconds_in_one_hour * hours)
    output += "\nHours= " + str(hours)
if (total_secs > seconds_in_one_minute):
    minutes = total_secs // seconds_in_one_minute
    total_secs = total_secs - (seconds_in_one_minute * minutes)
    output += "\nMinutes= " + str(minutes)

print(output + "\nSeconds= " + str(total_secs))                


