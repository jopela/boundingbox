#!/usr/bin/python3

from geopy.geocoders import GoogleV3
import argparse
import sys

# TODO: exception handling.

def main():

    program_name = sys.argv[0]

    parser = argparse.ArgumentParser()

    parser.add_argument(
            'place',
            type=str,
            help='The name of the place for which limit should be queried'\
                    ' (e.g:Paris). The result is a limit tuple that indicate'\
                    ' the (north,east,south,west) frontier of the bounding' \
                    ' box.',
            )

    parser.add_argument(
            '-t',
            '--test',
            action='store_true',
            default=False,
            help='Run the doctests test suite.')

    parser.add_argument(
            '-v',
            '--version',
            action='store_true',
            default=False,
            help='Display the version number and exit.')

    parser.add_argument(
            '-i',
            '--inside',
            type=str,
            help='a coordinate string of the form "lat,lng" in WGS84. When'\
                    ' specified on the command line, {0} will return True if'\
                    ' the point is inside the found boundingbox and False'\
                    ' otherwise. In both cases, program exit with 0')

    args = parser.parse_args()

    if args.test:
        import doctest
        doctest.testmod(verbose=True)
        exit(0)

    if args.version:
        print(version)
        exit(0)

    place = args.place

    box = boundingbox(place)

    if args.inside:
        lat, lng = lat_n_lng(args.inside)
        result = inside(lat,lng,box)
        print(result)
    else:
        print(box)

    return

def lat_n_lng(s):
    """
    return the lattitude and longitude tuple from the given string
    representation. Return None if the string representation is
    invalid.

    EXAMPLE
    =======

    >>> lat_n_lng("50,2.67")
    >>> (50.0,2.67)

    >>> lat_n_lng("lat and long")
    >>> None
    """

    lat,lng = s.split(",")

    result = (float(lat), float(lng))

    return result

def boundingbox(place):
    """
    Get a suggested bounding box for the given place.

    Example
    =======

    >>> boundingbox("Montreal, CA")
    (45.7058381, -73.47426, 45.410246, -73.9488652)
    >>> boundingbox("Paris, FR")
    (48.9021449, 2.4699208, 48.815573, 2.224199)
    """

    googlemap = GoogleV3()
    box = googlemap.geocode(place)[2]
    return box


def inside(lat, lng, box):
    """ Returns true if the given (`lat`,`lng`) point falls within the boundary
    of `box`. False otherwise.

    Example
    =======

    >>> inside(48.86, 2.33, (48.9021449, 2.4699208, 48.815573, 2.224199))
    True
    >>> inside(48.86, 2.33, (45.7058381, -73.47426, 45.410246, -73.9488652))
    False

    """
    NORTH,EAST,SOUTH,WEST = (0,1,2,3)

    if not box:
        # impossible to be inside a non existant box. Just return False
        # in that case.
        return False
    else:
        return lat < box[NORTH] and lat > box[SOUTH] and lng < box[EAST] and \
                lng > box[WEST]

if __name__ == '__main__':
    main()
