from ics import Calendar, Event
import requests
import datetime

URL = 'https://www.lcsd.gov.hk/datagovhk/event/leisure_prog.json'


def sprint_data(d):
    attr = [
        'PGM_CODE',
        'TC_PGM_NAME',
        'TC_VENUE',
        'PGM_START_DATE',
        'PGM_END_DATE',
        'TC_DAY',
        'PGM_START_TIME',
        'PGM_END_TIME',
        'ENROL_START_DATE'
    ]
    val = map(lambda k: d[k],  attr)
    s = ' | '.join(val)
    return s


def print_data(d):
    print(sprint_data(d))


def create_ics(data):
    c = Calendar()

    for d in data:
        date = d['ENROL_START_DATE']
        date = datetime.datetime.strptime(date+'+0800', '%Y-%m-%d %H:%M:%S%z')
        date = date.replace(hour=8, minute=30)

        e = Event()
        e.name = ' | '.join(
            [d['PGM_CODE'],
             d['TC_PGM_NAME'],
             d['TC_DAY'],
             d['PGM_START_TIME']])
        e.description = sprint_data(d)
        e.begin = date
        e.duration = datetime.timedelta(hours=12)
        c.events.add(e)

    print(c.serialize())
    with open('my.ics', 'w') as f:
        f.writelines(c.serialize_iter())


def main():
    res = requests.get(URL)
    data = res.json()

    selected_venue = [
        '深水埗運動場',
        '深水埗公園',
        '北河街體育館',
        '大角咀體育館(六樓健身室)'
    ]
    selected_act_type = ['器械健體',  '長跑']

    selected_data = [
        d for d in data
        if
        d['TC_VENUE'] in selected_venue and
        d['TC_ACT_TYPE_NAME'] in selected_act_type]

    create_ics(selected_data)


if __name__ == '__main__':
    main()
