from voluptuous import Schema, All, Range, Coerce, Required


class Schema:

    vehicle_id = Schema({
        Required('vehicle_id'): All(Coerce(int), Range(min=1))
    })

    booking = Schema({
        Required('vehicle_id'): All(Coerce(int), Range(min=1)),
        Required('user_id'): All(Coerce(int), Range(min=1))
    })
