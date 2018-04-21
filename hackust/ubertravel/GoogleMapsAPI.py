from datetime import datetime, timedelta


def get_dist_and_duration(geolocator, gmaps, start, end, getText):
    """
    Get the distance and duration
    :param geolocator: used to convert address to coordinates
    :param gmaps: used for gmaps retrieving
    :param start: string of the start point (address) of journey
    :param end: string of the end point (address) of journey
    :param getText: boolean (true returns string values, false return int values)
    :return: tuple of distance, duration (string, string) or (int - distance in meters, int - time in seconds) pair
    """
    now = datetime.now()
    # origins = []
    # destinations = []
    #orig_text = '25 lower kent ridge road'
    #dest_text = 'Changi airport'
    location_orig = geolocator.geocode(start)
    location_dest = geolocator.geocode(end)

    # string with start/end coordinates (x, y)
    orig_coordinates_text = location_orig.raw['lat'] + ', ' + location_orig.raw['lon']
    dest_coordinates_text = location_dest.raw['lat'] + ', ' + location_dest.raw['lon']

    # call google maps mpi
    directions_result = gmaps.directions(orig_coordinates_text,
                                         dest_coordinates_text,
                                         mode="driving",
                                         avoid="ferries",
                                         departure_time=now
                                        )

    # type -> datetime.timedelta
    # duration_val = timedelta(seconds=directions_result[0]['legs'][0]['duration']['value'])
    duration_val = directions_result[0]['legs'][0]['duration']['value']
    duration_text = directions_result[0]['legs'][0]['duration']['text']
    dist_val = directions_result[0]['legs'][0]['distance']['value']
    dist_text = directions_result[0]['legs'][0]['distance']['text']

    if getText:
        return dist_text, duration_text
    else:
        return dist_val, duration_val

    # print(duration_val)
    # print(duration_text)
    # print(dist_val)
    # print(dist_text)
