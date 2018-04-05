import alert_distractions
import datetime

def test_should_notify ():
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    # more seconds
    assert alert_distractions.should_notify(alert_distractions.SECONDS_TO_NOTIFY,0, datetime.datetime.now()) == True
    # no notification since yesterday
    assert alert_distractions.should_notify(0, 0, yesterday) == True
