import datetime

import flocx_market.db.sqlalchemy.api as db_api
import flocx_market.db.sqlalchemy.models as models
from flocx_market.objects.offer import Offer
from flocx_market.common.service import prepare_service
from flocx_market.conf import CONF
from flocx_market.api.app import create_app
from flocx_market.db.orm import orm

from oslo_db.exception import DBDuplicateEntry


CONF.clear()
prepare_service()
CONF.set_override("auth_enable", False, group='api')
CONF.set_override(
    'connection',
    'mysql+pymysql://flocx_market:qwerty123@localhost:3306/flocx_market',
    group='database')

app = create_app('flocx-market')
orm.init_app(app)
ctx = app.app_context()
ctx.push()

db_api.setup_db()

start_time = datetime.datetime.strptime('2019-08-01 UTC',
                                        '%Y-%m-%d %Z')
end_time = start_time + datetime.timedelta(days=14)

try:
    offer = db_api.offer_create(dict(
        provider_offer_id='1234',
        project_id='1234',
        server_id='1234',
        start_time=start_time,
        end_time=end_time,
        timeslots=[
            models.Timeslot(start_time=start_time, end_time=start_time + datetime.timedelta(days=2)),
            models.Timeslot(start_time=start_time + datetime.timedelta(days=4), end_time=start_time + datetime.timedelta(days=6)),
            models.Timeslot(start_time=start_time + datetime.timedelta(days=10), end_time=end_time)
        ],
        server_config={'foo': 'bar'},
        cost=0,
    ), None)
except DBDuplicateEntry:
    offer = db_api.offer_get_by_provider_offer_id('1234', None)

sess = db_api.get_session()

for timerange in [['2019-07-25 00:00:00', '2019-07-31 00:00:00'],
                  ['2019-08-03 00:00:00', '2019-08-03 00:00:00']]:
    available_offers = sess.query(models.Offer).join(models.Timeslot).filter(
        models.Timeslot.start_time <= timerange[0]).filter(
            models.Timeslot.end_time >= timerange[1]).all()

    print('For timerange from {} to {} there were {} offers'.format(
        timerange[0], timerange[1], len(available_offers)))
