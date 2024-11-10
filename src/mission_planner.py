purpose = '''
-> Complete control 
'''

tle_data_path = '/Users/thrishank/Documents/Projects/Project_Space_Debris_&_Route_Calculation/Space-Debris-and-Route-Calculation/datasets/tle_data.csv'

# imports
from timestamp import TimestampSelector
from orbit_selection import OrbitSelector
from rocket_orbital_velocity_calculation import VelocityCalculate
from rocket_selection import RocketSelector
from initial_trajectory import TrajectoryCalculator
from initial_trajectory_visualization import TrajectoryVisualizer
from collision_detection import CollisionDetection
from choose_collision_module import choose_module
from collision_detection_evaluation_matrix import CollisionDetectionEval
from dynamics_collision_detection import CollisionDetectionDynamics

# Structure integration
def main():
    # Step 1: timestamp.py
    mission_time = TimestampSelector()
    time_selected = mission_time.run()
    print(time_selected)

    # Step 2: orbit_selection.py
    global rocket_type, launch_sites, launch_coordinates, trajectory_equations
    orbit = OrbitSelector()
    altitude, altitude_range, orbit_type = orbit.select_orbit()
    print(altitude, altitude_range, orbit_type)

    # Step 2.1: rocket_orbital_velocity_calculation.py
    velocity = VelocityCalculate()
    velocity_to_reach = velocity.calculate_orbital_velocity(altitude)
    print("orbital_velocity:", velocity_to_reach, "m/s")

    # Step 3: rocket_selection.py
    rocket_selector = RocketSelector()

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

        # Proceed with trajectory calculation only if rocket details are valid
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
        # Proceed with visualization only if trajectory_equations is calculated
        if trajectory_equations:
            visualize = TrajectoryVisualizer(trajectory_equations, t_range=(0, 10))
            visualize.plot_trajectory()
        else:
            return

    model = choose_module()
    print(model)

    # Step 5: Choosing Module, collision_detection.py
    # Test the collision calculation and optimization
    if model[1] == "CollisionDetectionEval":
        collision_detector = CollisionDetectionEval(time_selected, trajectory_equations, rocket_type, launch_sites,
                                                launch_coordinates, altitude, altitude_range, orbit_type, tle_data_path)
        optimized_trajectory, metrics = collision_detector.optimize_trajectory()
        print(f"Optimized Trajectory: {optimized_trajectory}")
        print(f"Metrics: {metrics}")
    elif model[1] == "CollisionDetectionDynamics":
        collision_detector = CollisionDetectionDynamics(time_selected, trajectory_equations, rocket_type, launch_sites,
                                                        launch_coordinates, altitude, altitude_range, orbit_type,
                                                        tle_data_path)
        optimized_trajectory = collision_detector.optimize_trajectory()
        print(f"Optimized Trajectory: {optimized_trajectory}")
    else:
        collision_detector = CollisionDetection(time_selected, trajectory_equations, rocket_type, launch_sites,
                                                launch_coordinates, altitude, altitude_range, orbit_type, tle_data_path)
        optimized_trajectory = collision_detector.optimize_trajectory()
        print(f"Optimized Trajectory: {optimized_trajectory}")


    # visualize_trajectory_equations.py
    if trajectory_equations:
        after_optimization = TrajectoryVisualizer(optimized_trajectory, t_range=(0, 10))
        after_optimization.plot_trajectory()
    else:
        return

    # Step 6: impact_analysis.py

    # Step 8: mission_report.py


# Run main function
if __name__ == "__main__":
    main()
