import datetime

login_time = datetime.datetime.now()
lost_time = login_time + datetime.timedelta(hours=+12)
expires_at = lost_time.strftime('%Y-%m-%d %H:%M:%S')
