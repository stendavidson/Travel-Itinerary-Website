from flaskr.model.Itinerary import Itinerary
from flaskr.model.exceptions.ItineraryRequestException import ItineraryRequestException

from os.path import exists
from os import listdir, remove


class ItineraryConnector():
    """
    This class provides a mechanism by which itinerary information can be
    retrieved, created and destroyed.
    """

    
    def __init__(self, dir_path : str) -> None :

        """
        ItineraryConnector object initializer

        Parameters:
            dir_path (str): the path to the itinerary saves folder.
        """

        self.dir_path : str = dir_path


    # This method retrieves a list of itineraries by name
    def get_names(self) -> list[str]:

        """
        This method retrieves all the valid itinerary names.

        Returns:
            list[str]: the names of all the itineraries.
        """

        files = listdir(self.dir_path)

        names = []

        # The itinerary names are retrieved.
        for file in files :

            # The file types are minimally validated
            if file[-5:] == ".save" :
                
                names.append(file[:-5])

        return names
    

    # This method generates an Itinerary object from a saved itinerary file.
    def read(self, name : str) -> Itinerary :
        """
        This method retrieves the itinerary information from a save file.

        Parameters:
            name (str): The name of the itinerary.

        Returns:
            Itinerary: an Itinerary object corresponding to the data retrieved
            from the save file.
        """

        # Validated input types
        if not isinstance(name, str) :

            raise TypeError("Invalid input parameter: name => str.")

        itinerary = Itinerary()
        coordinates  = []

        # File path is created
        file_path = self.dir_path + f"/{name}.save"

        # The file path is validated
        if not exists(file_path) :

            raise ItineraryRequestException("This itinerary can no longer be found, please reload the page.")
        
        # The file is read
        with open(file_path, "r") as file :
            
            lines = file.readlines()

            for line in lines :
                
                # The coordinates are parsed
                coordinates.append([i.strip().replace("\n", "") for i in line.split(",")])

        # The file is parsed into an Itinerary object
        for data in coordinates :
            
            # The data is validated
            if len(data) != 3 :

                raise ItineraryRequestException("The stored itinerary has been corrupted.")

            latitude = 0
            longitude = 0
            
            # The request data is converted to numerical data
            try :
                
                latitude = float(data[1])
                longitude = float(data[2])

            except TypeError as e :
    
                raise ItineraryRequestException("The stored itinerary has been corrupted.")

            
            itinerary[data[0]] = (latitude, longitude)

        # The center is re-calculated upon re-creation of the itinerary.
        itinerary.find_center()
                
        return itinerary


    def write(self, name : str, itinerary : Itinerary) -> None :
        """
        This method creates or overwrites an itinerary save file.

        Parameters:
            name (str): The name of the itinerary.
            itinerary (Itinerary): An itinerary object encapsulating the itinerary
            information.
        """

        # Input validation
        if not isinstance(name, str) or not isinstance(itinerary, Itinerary) :

            raise TypeError("Invalid input parameters: name => str and itinerary => Itinerary.")

        lines = ""

        # The itinerary is converted into a csv format
        for coordinates in itinerary :
            
            lines += ",".join([str(word) for word in coordinates]) + "\n"

        # The itinerary is written to the file
        try:

            with open(self.dir_path + f"/{name}.save", "w") as file :

                file.write(lines)

        except OSError as e :

            raise ItineraryRequestException("The server experienced an error while saving, please try again.")
        

    # This method deletes a given itinerary
    def delete(self, name : str) -> None :
        """
        This method deletes an itinerary save file.

        Parameters:
            name (str): The name of the itinerary to be deleted
        """

        # Validated input types
        if (not isinstance(name, str)) :

            raise TypeError("Invalid input parameter: name => str.")
        
        # File path is created
        file_path = self.dir_path + f"/{name}.save"
        
        # The file path is validated
        if not exists(file_path) :

            raise ItineraryRequestException("This itinerary can no longer be found, please reload the page.")
        
        # The file is deleted
        try :
            
            remove(file_path)

        except OSError as e :

            raise ItineraryRequestException("The server experienced an error while deleting this resource.")
            

            



