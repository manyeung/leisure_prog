from ics import Calendar, Event
import requests
import datetime
import re

URL = 'https://www.lcsd.gov.hk/datagovhk/event/leisure_prog.json'

VENUE_DICT = {}
ACTIVITY_DICT = {}

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

def slugify(s):
    s = s.lower().strip()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_-]+', '_', s)
    s = re.sub(r'^_+|_+$', '', s)
    return s

def sprint_html(ics, venue, activity):
    return '<li><a href="%s">%s - %s</a></li>' % (ics, VENUE_DICT[venue], ACTIVITY_DICT[activity])

def print_html(ics, venue, activity):
    print(sprint_html(ics, venue, activity))

def create_ics(file, data):
    c = Calendar()

    for d in data:
        date = d['ENROL_START_DATE']
        date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

        e = Event()
        e.name = ' | '.join(
            [d['PGM_CODE'],
             d['TC_VENUE'],
             d['TC_DAY'],
             d['PGM_START_TIME']])
        e.description = sprint_data(d)
        e.begin = date
        e.make_all_day()
        e.url = d['TC_URL']
        c.events.add(e)

    # print(c.serialize())
    with open(file, 'w') as f:
        f.writelines(c.serialize_iter())


def main():
    res = requests.get(URL)
    data = res.json()

    for d in data:
        VENUE_DICT[d['EN_VENUE']] = d['TC_VENUE']
        ACTIVITY_DICT[d['EN_ACT_TYPE_NAME']] = d['TC_ACT_TYPE_NAME']

    venues = {d['EN_VENUE'] for d in data}
    # print('Total venues: %s' % (len(venues)))

    now = datetime.datetime.now()
    html = '<html><body>\n'
    html = html + ('<p>更新時間 %s</p>\n' % (now.strftime('%c UTC')))
    html = html + '<ul>\n'

    for venue in sorted(venues):
        activities = {
            d['EN_ACT_TYPE_NAME'] for d in data
            if 
            d['EN_VENUE'] == venue
        }
        # print('Total activities for %s : %s' % (venue, len(activities)))

        for activity in sorted(activities):
            ics = '%s--%s.ics' % (slugify(venue), slugify(activity))
            selected_data = [
                d for d in data
                if
                d['EN_VENUE'] == venue and
                d['EN_ACT_TYPE_NAME'] == activity
            ]
            create_ics(ics, selected_data)
            print('Create ICS: %s' % (ics))
            html = html + sprint_html(ics, venue, activity) + '\n'

    html = html + '</ul></body></html>\n'
    f = open('index.html', 'w')
    f.write(html)
    f.close()

    print('OK!')


if __name__ == '__main__':
    main()
