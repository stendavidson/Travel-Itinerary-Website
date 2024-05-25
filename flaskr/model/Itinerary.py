from typing import Iterator
import math

from flaskr.model.exceptions.RepeatLocationException import RepeatLocationException
from flaskr.model.exceptions.LocationKeyException import LocationKeyException
from flaskr.model.exceptions.InvalidLocationException import InvalidLocationException


class Itinerary :
    """
    The Itinerary class encapsulates a list of location names and coordinates
    in a first-to-last ordered array.
    """


    def __init__(self) -> None :
        """
        Itinerary object initializer
        """

        self.coordinates : list[tuple[str, float, float]] = list()
        self.locations : dict[str, int] = dict()
        self.center : tuple[float, float] = tuple()


    def __getitem__(self, location : str) -> tuple[str, float, float] :
        """
        This method retrieves coordinates using the plain text location name.

        Parameters:
            location (str): a plain text location name.

        Returns:
            tuple[str, float, float]: the coordinates of a given location.
        """
        
        # Validated input types
        if (not isinstance(location, str)) :

            raise TypeError("Invalid input parameters: location => str.")

        # Handle scenario where location can't be retrieved.
        try :

            entry = self.coordinates[self.locations[location]]

        except KeyError :

            raise LocationKeyException(location)

        return entry
    

    def __setitem__(self, location : str, coordinates : tuple[float, float]) -> None :
        """
        This method stores the coordinates and name of a given location.

        Parameters:
            location (str): a plain text location name.
            coordinates (tuple[float, float]): the coordinates of a given location.
        """

        # Validated input types
        if (not isinstance(location, str)) or (not isinstance(coordinates, tuple))\
            or (not isinstance(coordinates[0], float) or (not isinstance(coordinates[1], float))) :

            raise TypeError("Invalid input parameters: location => str and coordinates => tuple[float, float].")
        
        # Coordinates are validated
        if coordinates[0] < -90 or coordinates[0] > 90 or  coordinates[1] < -180 \
            or coordinates[1] > 180 :

            raise InvalidLocationException(coordinates)

        # Conditional assigns location and coordinates if location doesn't already exist.
        if location in self.locations :
            
            # An exception is raised if a location is a duplicate
            raise RepeatLocationException(location)
        
        else :
        
            self.coordinates.append((location, coordinates[0], coordinates[1]))
            self.locations[location] = len(self.coordinates)


    # This method allows the center of the itinerary to be calculated
    def find_center(self)  -> tuple[float, float]:
        """
        This method calculates the center point of all the coordinates in the itinerary,
        this is for mapping purposes.

        Returns:
            tuple[float, float]: the coordinates of the calculated central point.
        """

        x = 0
        y = 0
        z = 0

        if len(self.coordinates) > 0 :

            # Find the average (x, y, z) self.coordinates converted from latitude and longitude
            for i in self.coordinates :

                x += math.cos(i[1] * (math.pi / 180)) * math.cos(i[2] * (math.pi / 180))
                y += math.sin(i[1] * (math.pi / 180))
                z += math.cos(i[1] * (math.pi / 180)) * math.sin(i[2] * (math.pi / 180))

            x /= len(self.coordinates)
            y /= len(self.coordinates)
            z /= len(self.coordinates)

            # The z and x hypotenuse enable you to calculate the latitude and longitude
            hypotenuse = math.sqrt(z * z + x * x)
            # atan() can differentiate between values ~(-0,+0)
            latitude = math.atan(y/hypotenuse) * (180 / math.pi)
            # The (z/abs(z)) handles the scenario in which acos() cannot correctly 
            # differentiate between values of ~(-0,+0) and ~(-180,180)
            longitude = (z/abs(z)) * math.acos(x/hypotenuse) * (180 / math.pi)

            self.center = (latitude, longitude)

        else :

            # If there are no coordinates the center is set by default to the "center"
            # of the UK.
            self.center = (53.7547525,-4.8904832)

        return self.center
    

    def __contains__(self, location : str) -> bool :
        """
        This method checks if the input location can be found in the itinerary.

        Parameters:
            location (str): The location to be validated.

        Returns:
            bool: the checksum representing the location's inclusing in the itinerary.
        """

        return (location in self.locations)
    

    # 
    def __len__(self) -> int :
        """
        This method returns the length of the itinerary

        Returns:
            int: the number of coordinates stored in the Itinerary.
        """

        return self.coordinates.__len__()
    
    
    
    def __iter__(self) -> Iterator:
        """
        This method retrieves the underlying iterator and allows for simplified
        looping.

        Returns:
            Iterator: The underlying iterator object.
        """

        return self.coordinates.__iter__()
        