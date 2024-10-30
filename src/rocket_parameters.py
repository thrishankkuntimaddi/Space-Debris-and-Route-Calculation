purpose = "Gathers and defines essential rocket parameters (e.g., type, launch site)."

'''
1. Select Rocket Parameters
   - Input type of rocket, launch site, and any additional attributes.
2. Store Parameters for Route Calculation
'''

class RocketParameters:
    def __init__(self):
        self.launch_time = None
        self.launch_site = None
        self.target_orbit_min = None
        self.target_orbit_max = None
        self.rocket_type = None

    def setup_rocket_parameters(self):
        """
        Set up the rocket parameters such as launch time, site, target orbit range, and rocket type.
        """
        self.launch_time = '2024-10-29T12:00:00'  # Example launch time without 'Z'
        self.launch_site = {
            'name': 'Cape Canaveral',
            'address': 'Cape Canaveral, Florida, USA',  # Detailed address
            'state': 'Florida',
            'country': 'USA'
        }
        self.target_orbit_min = 500  # Minimum altitude in km (e.g., 500 km)
        self.target_orbit_max = 800  # Maximum altitude in km (e.g., 800 km)
        self.rocket_type = 'Falcon 9'  # Example rocket type
