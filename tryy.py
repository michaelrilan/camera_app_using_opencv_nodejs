from datetime import datetime
current_dateTime = datetime.now()
file_name =str(current_dateTime.hour)+str(current_dateTime.minute) + str(current_dateTime.second) + str(current_dateTime.microsecond)

print(file_name)