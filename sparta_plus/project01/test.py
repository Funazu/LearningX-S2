from datetime import datetime

today = datetime.now()
yoy = today.strftime('%Y-%m-%d-%H:%M:%S')
print(yoy)