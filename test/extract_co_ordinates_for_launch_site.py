import requests


class Location:
    def __init__(self, place_name):
        self.place_name = place_name
        self.latitude = None
        self.longitude = None

    def get_coordinates(self):
        base_url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": self.place_name,
            "format": "json",
            "limit": 1
        }
        response = requests.get(base_url, params=params)
        data = response.json()

        if data:
            self.latitude = float(data[0]['lat'])
            self.longitude = float(data[0]['lon'])
            return self.latitude, self.longitude
        else:
            return None, None

    def display_coordinates(self):
        if self.latitude is not None and self.longitude is not None:
            print(f"Latitude: {self.latitude}, Longitude: {self.longitude}")
        else:
            print("Coordinates not found.")


# Example usage:
place = Location("Naro Space Center, South Korea")
latitude, longitude = place.get_coordinates()
place.display_coordinates()
