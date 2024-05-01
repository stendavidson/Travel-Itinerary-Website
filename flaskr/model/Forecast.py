from Weather import Weather

# The Forecast class encapsulates a time ordered list of Weather information.
class Forecast :

    def __init__(self) -> None :

        self.forecast : list[Weather] = []


    def __getitem__(self, index : int) -> tuple[float, float] :

        return self.forecast[index]


    def append(self, weather : Weather) -> None :

        # Raise TypeError for invalid input Type
        if not isinstance(weather, Weather) :

            raise TypeError("Invalid argument, the weather parameter must by an instance of the Weather class.")

        self.forecast.append(weather)

    