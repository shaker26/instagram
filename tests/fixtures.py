from src.models.users import User
from src.models.posts import Posts
from src import utils, db


default_amenity_event = {
    'timestamp': 1547281508,
    'user_id': 2835680135910998,
    'amenity_id': 967149002
}

default_hotel_event = {
    'timestamp': 1547281508,
    'user_id': 2835680135910998,
    'hotel_id': 429536,
    'hotel_region': 'unknown'
}


def createAmenityPreferenceEvent(**kwargs):
    return utils.mergeDicts(default_amenity_event, kwargs)


def dbCreateAmenityPreferenceEvent(**kwargs):
    event_kwargs = createAmenityPreferenceEvent(**kwargs)
    event = User(**event_kwargs)
    db.session.add(event)
    db.session.commit()
    return event


def createHotelPreferenceEvent(**kwargs):
    return utils.mergeDicts(default_hotel_event, kwargs)


def dbCreateHotelPreferenceEvent(**kwargs):
    event_kwargs = createHotelPreferenceEvent(**kwargs)
    event = Posts(**event_kwargs)
    db.session.add(event)
    db.session.commit()
    return event