from utils import typedef


class Point(object):
    """
    A coordinate in a 2D plane with orthogonal axes x & y
    """
    def __init__(self, x, y):
        """
        Initialize the Point class
        :param x: The x coordinate
        :param y: The y coordinate
        """
        self.x = x
        self.y = y
        self.coordinates = (x, y)

    def move(self, delta_x, delta_y):
        """
        Get a new point at (delta_x, delta_y) away from self
        :param delta_x: The delta (change in) x
        :param delta_y: The delta (change in) y
        :return: A Point object
        """
        return Point(self.x + delta_x,
                     self.y + delta_y)

    def move_to(self, x, y):
        """
        Get a new point at (x, y)
        :param x: The x coordinate
        :param y: The y coordinate
        :return: A Point object
        """
        return Point(x, y)

    def distance_from(self, other):
        """
        Use Pythagorean theorem to calculate distance between two points
        :param other: A Point object
        :return: A float distance between self and another Point
        """
        x_distance = self.x - other.x
        y_distance = self.y - other.y
        return (x_distance**2 + y_distance**2)**0.5

    def __str__(self):
        return str(self.coordinates)

    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        if not isinstance(other, Point):
            return True
        return self.__dict__ != other.__dict__


class Location(Point):
    """
    A Point object with the addition of building and clinic name text
    """
    def __init__(self, x, y, building, clinic):
        Point.__init__(self, x, y)
        self.building = building
        self.clinic = clinic

    def __str__(self):
        return str((self.building, self.clinic))


class Grid(object):
    """
    A two-dimensional Cartesian grid
    """
    def __init__(self):
        """
        Initialize the Grid class
        """
        self.locs = {}

    def add_loc(self, person, point):
        """
        Add the location of a person to self.locs. A person can only be
        at a single location. Use self.move_to to move them.
        :param person: A Person object at location
        :param point: The 2D Cartesian coordinates of location
        :return: None
        """
        if person in self.locs:
            raise ValueError('Duplicate ' + typedef(person) + ".")
        else:
            self.locs[person] = point

    def get_loc(self, person):
        """
        Get the location of a person
        :param person: A Person object to locate
        :return: A Point object with the 2D Cartesian coordinates of location
        """
        if person not in self.locs:
            raise ValueError(typedef(person) + ' not in grid.')
        return self.locs[person]

    def move_to(self, person, point):
        """
        Move person to a new location and record that in self.locs
        :param person: A Person object to move
        :param point: A Point object as the reference point
        :return: None
        """
        if person not in self.locs:
            raise ValueError(typedef(person) + ' not in grid.')
        self.locs[person] = Point(point.x, point.y)

    def __eq__(self, other):
        if not isinstance(other, Grid):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        if not isinstance(other, Grid):
            return True
        return self.__dict__ != other.__dict__


