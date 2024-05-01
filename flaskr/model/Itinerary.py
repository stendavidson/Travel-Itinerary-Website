from exceptions.RepeatLocationException import RepeatLocationException
from exceptions.LocationKeyException import LocationKeyException
from collections import OrderedDict

# The Itinerary class encapsulates Location information.
class Itinerary :

    def __init__(self) -> None :

        self.coordinates : OrderedDict[str, tuple[float, float]] = OrderedDict()


    def __getitem__(self, location : str) -> tuple[float, float] :

        coords : None | tuple[float, float] = None

        # Coordinates are retrieved - where possible
        try :

            coords = self.coordinates[location]

        except KeyError :

            # Raise LocationKeyException if a location does not appear on the itinerary.
            raise LocationKeyException(location)
        
        return coords

    

    def __setitem__(self, location : str, coordinates : tuple[float, float]) -> None :

        # Raise TypeError for invalid input type
        if (not isinstance(coordinates, tuple)) or (not isinstance(coordinates[0], float)) :

            raise TypeError("Invalid argument, coordinates parameter must by of type tuple[float, float].")

        # Conditional assigns location and coordinates if location doesn't already exist.
        if location in self.coordinates :
            
            # Raise LocationKeyException if a location already appears on the itinerary.
            raise RepeatLocationException(location)
        
        else :
        
            self.coordinates[location] = coordinates

    