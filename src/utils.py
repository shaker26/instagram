import copy
import datetime
import re

import pytz
import sqlalchemy
from sqlalchemy import schema
from sqlalchemy.engine import reflection


DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H:%M:%S'
UTC_RFC_3339_FORMAT = '{}T{}Z'.format(DATE_FORMAT, TIME_FORMAT)
UTC_RFC_3339_WITH_MICROSECONDS_FORMAT = '{}T{}.%fZ'.format(DATE_FORMAT, TIME_FORMAT)


def is_date_on_day_of_week(date, day_index):
    """Return True if ISO 8601 weekday for `date` equals `day_index`."""
    if type(day_index) is not int:
        raise TypeError('`day_index` must be of type int')
    elif not (1 <= day_index <= 7):
        raise ValueError('`day_index` must fall between 1 and 7 inclusive.')
    elif not isinstance(date, datetime.date):
        raise TypeError('`date` must be an instance of datetime.date')

    return date.isoweekday() == day_index


def validate_utc_datetime(dt):
    try:
        utc_tz = pytz.utc
        utc_datetime = utc_tz.localize(
            datetime.datetime.strptime(dt, UTC_RFC_3339_FORMAT))
        return utc_datetime
    except (ValueError, TypeError):
        return None


def rfc3339UTCDateTime(dt):
    utc_tz = pytz.utc
    try:
        utc_datetime = utc_tz.localize(
            datetime.datetime.strptime(dt, UTC_RFC_3339_WITH_MICROSECONDS_FORMAT))
        return utc_datetime
    except (ValueError, TypeError):
        try:
            utc_datetime = utc_tz.localize(datetime.datetime.strptime(dt, UTC_RFC_3339_FORMAT))
            return utc_datetime
        except:
            raise ValueError('RFC3339-formatted DateTime string is required')


def convertLocalToUTCDatetime(local_date, local_time, timezone_id):
    """Convert date, time, and timezone_id to a utc_datetime"""
    if not isinstance(local_date, datetime.date):
        raise TypeError('`local_date` must be of type datetime.date')
    if not isinstance(local_time, datetime.time):
        raise TypeError('`local_time` must be of type datetime.time')

    location_tz = pytz.timezone(timezone_id)

    local_datetime = location_tz.localize(
        datetime.datetime.combine(local_date, local_time))
    utc_datetime = local_datetime.astimezone(pytz.utc)

    return utc_datetime


def convertToLocalDatetime(utc_datetime, timezone):
    """Convert a UTC datetime to a local datetime for the given timezone.

    :param utc_datetime: (datetime.datetime or None) A datetime
    :param timezone: (datetime.tzinfo or string) A timezone object or Olson timezone identifier
    :returns: (datetime.datetime or None) The localized datetime.
    """
    if utc_datetime is None:
        return None

    location_tz = timezone
    if not isinstance(location_tz, datetime.tzinfo):
        location_tz = pytz.timezone(location_tz)
    local_datetime = utc_datetime.astimezone(location_tz)
    return local_datetime


def isoFormatDatetime(dt):
    """Converts the given datetime to an RFC-3339-formatted string.

    The timezone of the datetime is used in the representation.
    The datetime may be None, in which case this function simply
    returns None.
    """
    if dt is None:
        return None
    return re.sub(r'\+00:00$', 'Z', dt.isoformat())


def utcFormatDatetime(dt):
    """Converts the given datetime to a RFC-3339-formatted string in UTC.

    The datetime is assumed to be timezone-aware. It may be None, in which
    case this function simply returns None.
    """
    if dt is None:
        return None
    return isoFormatDatetime(dt.astimezone(pytz.utc))


def utcnow():
    """Returns the current UTC datetime. For easy replacement during testing."""
    return datetime.datetime.now(pytz.utc)


def startOfDayUTC(dt):
    """Return a timezone-aware datetime.datetime instance for the given day at 00:00:00 UTC.

    NOTE: the datetime instance passed must be in UTC.
    """
    if dt.tzinfo != pytz.utc:
        raise ValueError('Datetime must be in UTC')
    return pytz.utc.localize(datetime.datetime(dt.year, dt.month, dt.day))


def startDatetimeIsBeforeEndDatetime(start_datetime, end_datetime):
    """Return True if `start` is before `end`.

    :param start_datetime: (datetime.datetime) A timezone-aware datetime object.
    :param end_datetime: (datetime.datetime) A timezone-aware datetime object.
    """
    return start_datetime < end_datetime


def nonnegative_int(s):
    """Converts a string to a nonnegative integer."""
    n = int(s)
    if n < 0:
        raise ValueError('Nonnegative number is required')
    return n


def dropAllTables(db):
    """Drop all tables from the database. For testing only!

    Recipe from http://www.sqlalchemy.org/trac/wiki/UsageRecipes/DropEverything .
    Adapted for Flask-SQLAlchemy by http://www.mbeckler.org/blog/?p=218 .

    :param db: (flask.sqlalchemy.SQLAlchemy) The object representing the DB
    """
    conn=db.engine.connect()

    # the transaction only applies if the DB supports
    # transactional DDL, i.e. Postgresql, MS SQL Server
    trans = conn.begin()

    inspector = reflection.Inspector.from_engine(db.engine)

    # gather all data first before dropping anything.
    # some DBs lock after things have been dropped in
    # a transaction.
    metadata = sqlalchemy.MetaData()

    tables = []
    all_fks = []

    for table_name in inspector.get_table_names():
        fks = []
        for fk in inspector.get_foreign_keys(table_name):
            if not fk['name']:
                continue
            fks.append(sqlalchemy.ForeignKeyConstraint((), (), name=fk['name']))
        table = sqlalchemy.Table(table_name, metadata, *fks)
        tables.append(table)
        all_fks.extend(fks)

    for constraint in all_fks:
        conn.execute(schema.DropConstraint(constraint))

    for table in tables:
        conn.execute(schema.DropTable(table))

    trans.commit()


def resetDB(db):
    """Resets the database. For testing only!"""
    # WARNING: Flask-SQLAlchemy's db.drop_all() does not handle
    # foreign-key constraintts properly in all cases, and we've found
    # that one of the workarounds suggested online, calling db.reflect(),
    # doesn't always help either. The result is a DB exxception.
    # Trying this recipe instead.
    dropAllTables(db)
    db.create_all()


def mergeDicts(d1, *args):
    """Returns a dict that is the result of merging dicts together.

    One or more dicts may be provided. In the sequence of dicts passed to this
    function, values in later dict override values in earlier dicts.

    This function copies the initial dict deeply. It does not merge
    nested dicts or sequences recursively.
    """
    out = copy.deepcopy(d1)
    for d in args:
        out.update(d)
    return out
