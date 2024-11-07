purpose = '''
-> Complete control 
'''

# imports
from timestamp import TimestampSelector
from orbit_selection import OrbitSelector
from rocket_orbital_velocity_calculation import VelocityCalculate
from rocket_selection import RocketSelector
from initial_trajectory import TrajectoryCalculator
from initial_trajectory_visualization import TrajectoryVisualizer


# Structure integration
def main():
    # Step 1: timestamp.py
    mission_time = TimestampSelector()
    time_selected = mission_time.run()
    print(time_selected)

    # Step 2: orbit_selection.py
    global rocket_type, launch_sites, launch_coordinates
    orbit = OrbitSelector()
    altitude, altitude_range, orbit_type = orbit.select_orbit()
    print(altitude, altitude_range, orbit_type)

    # Step 2.1: rocket_orbital_velocity_calculation.py
    velocity = VelocityCalculate()
    velocity_to_reach = velocity.calculate_orbital_velocity(altitude)
    print("orbital_velocity:", velocity_to_reach, "m/s")

    # Step 3: rocket_selection.py
    rocket_selector = RocketSelector()

    rockets_for_target_altitude = rocket_selector.get_rockets_for_orbit_and_altitude(altitude, orbit_type)
    print("Rockets for Target Altitude and Orbit Type:", rockets_for_target_altitude)

    # Check rocket criteria based on user dynamic input of rocket type
    rocket_details = rocket_selector.check_rocket_criteria(altitude, orbit_type)
    if isinstance(rocket_details, str):
        print(rocket_details)
    else:
        rocket_type, launch_sites, launch_coordinates = rocket_details['Rocket_Type'], rocket_details['Launch_Site'], \
        rocket_details['Launch_Site_Coordinates']
        print(f"Rocket Type: {rocket_type}")
        print(f"Launch Site: {launch_sites}")
        print(f"Launch Site Coordinates: {launch_coordinates}")

    # Step 4: initial_trajectory.py
    trajectory_calculator = TrajectoryCalculator()
    trajectory_equations = trajectory_calculator.calculate_trajectory(
        rocket_type=rocket_type,
        launch_site=launch_sites,
        launch_site_coordinates=launch_coordinates,
        selected_altitude_to_reach=altitude
    )
    print(trajectory_equations)

    # Step 4.1: visualize_trajectory_equations.py
    visualize = TrajectoryVisualizer(trajectory_equations, t_range=(0, 10))
    visualize.plot_trajectory()

    # Step 5: orbital_dynamics.py


    # Step 6: collision_detection.py

    # Step 6.1: impact_analysis.py

    # Step 7: trajectory_optimizer.py

    # step 8: mission_report.py


# Run main function
if __name__ == "__main__":
    main()
