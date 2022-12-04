from datetime import datetime
from calendar import monthrange
import time

current_year = datetime.now().year

month = int(time.strftime('%m'))
days_in_month = monthrange(current_year, month)[1]

current_day = int(time.strftime('%d'))
