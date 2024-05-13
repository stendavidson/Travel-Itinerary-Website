from Itinerary import Itinerary
from exceptions.ItineraryRequestException import ItineraryRequestException

from os.path import exists


class ItineraryConnector():


    def __init__(self, file_path : str) :

        self.file_path = file_path


    def read(self) -> Itinerary :

        itinerary = Itinerary()
        coordinates  = []

        if not exists(self.file_path) :

            raise ItineraryRequestException() # 500
        
        with open(self.file_path, "r") as file :
            
            lines = file.readlines()

            for line in lines :

                coordinates.append(line.split())

        for data in coordinates :
            
            if len(data) != 3 :

                raise ItineraryRequestException() # 500

            latitude = 0
            longitude = 0
            
            try :
                
                latitude = float(data)
                longitude = float(data)

            except ValueError as e :
    
                raise ItineraryRequestException() # 500


            if data[0] in itinerary :
                
                raise ItineraryRequestException() # 500
            
            itinerary[data[0]] = (latitude, longitude)
                
        return itinerary



    def write(self, itinerary : Itinerary) -> None :

        lines = ""

        for i in itinerary :

            lines += ",".join(i) + "\n"

        try:

            with open(self.file_path, "w") as file :

                file.write(lines)

        except OSError as e :

            return ItineraryRequestException() # 500
            

            



