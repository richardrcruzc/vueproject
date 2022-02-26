import pytz


def get_timestamp(time_object):
    try:
        sg_tz = pytz.timezone('Asia/Singapore')
        return time_object.astimezone(sg_tz).strftime("%Y-%m-%d %H:%M:%S")
    except:
        return 'N/A'