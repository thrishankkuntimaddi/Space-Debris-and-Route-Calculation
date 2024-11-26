purpose = '''
-> Complete control 
'''

# imports
import pandas as pd
from timestamp import TimestampSelector
from orbit_selection import OrbitSelector
from rocket_orbital_velocity_calculation import VelocityCalculate
from rocket_selection import RocketSelector
from initial_trajectory import TrajectoryCalculator
from initial_trajectory_visualization import TrajectoryVisualizer
from mission_report import MissionReport
from double_deep_dynamic_collision_detection import DeepDynamicCollisionDetection

tle_data_path = '/Users/thrishankkuntimaddi/Documents/Final_Year_Project/Space-Debris-and-Route-Calculation/data/tle_data.csv'
rocket_parameters_path = '/Users/thrishankkuntimaddi/Documents/Final_Year_Project/Space-Debris-and-Route-Calculation/data/rocket_parameters.csv'
tle_data = pd.read_csv(tle_data_path, low_memory=False)

# Structure integration
def main():
    # Initialize mission report
    mission_report = MissionReport()

    # Load rocket parameters from CSV
    rocket_parameters_df = pd.read_csv(rocket_parameters_path)

    # Step 1: timestamp.py
    mission_time = TimestampSelector()
    time_selected = mission_time.run()
    print(time_selected)
    mission_report.add_mission_overview(
        mission_name="Space Debris and Route Calculation Mission",
        orbit_details="To be determined",
        launch_window=time_selected
    )

    # Step 2: orbit_selection.py
    global rocket_type, launch_sites, launch_coordinates, trajectory_equations
    orbit = OrbitSelector()
    altitude, altitude_range, orbit_type = orbit.select_orbit()
    print(altitude, altitude_range, orbit_type)
    mission_report.add_orbital_analysis(
        selected_orbit=f"Altitude: {altitude} km, Type: {orbit_type}",
        feasibility_analysis="To be determined",
        orbital_velocity="To be calculated"
    )

    # Step 2.1: rocket_orbital_velocity_calculation.py
    velocity = VelocityCalculate()
    velocity_to_reach = velocity.calculate_orbital_velocity(altitude)
    print("orbital_velocity:", velocity_to_reach, "m/s")
    mission_report.add_orbital_analysis(
        selected_orbit=f"Altitude: {altitude} km, Type: {orbit_type}",
        feasibility_analysis="Feasible with selected rocket",
        orbital_velocity=f"{velocity_to_reach} m/s"
    )

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

        # Extract rocket parameters from CSV
        rocket_data = rocket_parameters_df[rocket_parameters_df['Rocket_Type'] == rocket_type].iloc[0]
        fuel_consumption = rocket_data['Fuel_Consumption_kg_per_km']

        mission_report.add_rocket_details(
            rocket_type=rocket_type,
            fuel_consumption=f"{fuel_consumption} kg/km",
            compatible_launch_sites=launch_sites,
            launch_site_coordinates=launch_coordinates
        )

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
        mission_report.add_initial_trajectory_info(
            trajectory_equation=trajectory_equations,
            parameters={"selected_altitude": f"{altitude} km"},
            visualization_notes="To be visualized"
        )

        # Step 4.1: visualize_trajectory_equations.py
        # Proceed with visualization only if trajectory_equations is calculated
        if trajectory_equations:
            visualize = TrajectoryVisualizer(trajectory_equations, t_range=(0, 10))
            visualize.plot_trajectory()
            mission_report.add_initial_trajectory_info(
                trajectory_equation=trajectory_equations,
                parameters={"selected_altitude": f"{altitude} km"},
                visualization_notes="Trajectory visualization completed"
            )
        else:
            return

    # DeepDynamicCollisionDetection

    model = DeepDynamicCollisionDetection(
        trajectory_equation=trajectory_equations,
        rocket_type=rocket_type,
        launch_sites=launch_sites,
        launch_coordinates=launch_coordinates,
        altitude=altitude,
        altitude_range=altitude_range,
        orbit_type=orbit_type,
        time_selected=time_selected,
        tle_data=tle_data
    )

    # Ask the user whether to train the model or use the existing model for predictions
    user_choice = input(
        "Do you want to train the model or use the existing model for predictions? (train/use): ").strip().lower()

    if user_choice == 'train':
        num_episodes = int(input("Enter total number of episodes: "))
        max_steps = int(input("Enter max steps per episode: "))
        evaluation_metrics, collision_data, optimized_trajectory = model.train(num_episodes=num_episodes,
                                                                               max_steps=max_steps)
        print(f"\nOptimized Trajectory: {optimized_trajectory}")
        print(f"\nEvaluation Metrics: {evaluation_metrics}")
        if collision_data:
            print(f"\nCollisions Detected: {collision_data}")
    elif user_choice == 'use':
        for t in range(5):  # Example of using the model for prediction over time steps
            action = model.predict(t)
            print(f"Predicted action at time {t}: {action}")

        # Also return the optimized trajectory and evaluation metrics from the existing model
        optimized_trajectory = model.optimize_trajectory()
        evaluation_metrics = model.evaluate_model()
        print(f"\nOptimized Trajectory: {optimized_trajectory}")
        print(f"\nEvaluation Metrics: {evaluation_metrics}")
    else:
        print("Invalid choice. Please enter 'train' or 'use'.")

    # visualize_trajectory_equations.py
    if trajectory_equations:
        after_optimization = TrajectoryVisualizer(optimized_trajectory, t_range=(0, 10))
        after_optimization.plot_trajectory()
        mission_report.add_optimized_trajectory_info(
            optimized_trajectory_equation=optimized_trajectory,
            visualization_notes="Post-optimization trajectory visualization completed"
        )
    else:
        return

    # Step 6: mission_report.py
    mission_report.save_report_to_file("mission_report.txt")


# Run main function
if __name__ == "__main__":
    main()
