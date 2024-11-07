from orbit_selection import OrbitSelector
from rocket_parameters import RocketParameters
from trajectory_to_selected_orbit import TrajectoryCalculator
from collision_avoidance import CollisionDetection
from orbital_dynamics import OrbitalDynamics
from mission_report import MissionReport
from trajectory_visualization import TrajectoryVisualization
from trajectory_optimizer import TrajectoryOptimizer
from datetime import datetime

def main():
    # Step 1: Input timestamp for the mission
    mission_timestamp = input("Enter the launch timestamp (YYYY-MM-DDTHH:MM:SS): ")  # Example: 2024-10-30T12:00:00
    try:
        mission_datetime = datetime.strptime(mission_timestamp, "%Y-%m-%dT%H:%M:%S")
        print(f"Mission timestamp is valid: {mission_datetime}")
    except ValueError:
        print("Invalid timestamp format. Please use YYYY-MM-DDTHH:MM:SS format.")
        return

    # Step 2: Select orbit(distance away from Earth's surface) for the mission
    selected_altitude = OrbitSelector()
    altitude = selected_altitude.select_orbit()
    user_select_orbit = altitude[0]
    print(altitude)

    # Step 3: Rocket Parameters
    params = RocketParameters()
    summary = params.check_rocket_criteria(user_select_orbit, altitude[1], altitude[2])
    if isinstance(summary, str):
        print(summary)
        return
    print(summary)

    # Step 4: Trajectory Calculation for Rocket
    trajectory_calculator = TrajectoryCalculator()
    trajectory_equation = trajectory_calculator.calculate_trajectory(
        rocket_type=summary['Rocket_Type'],
        launch_site=summary['Launch_Site'],
        target_orbit=altitude[0]
    )
    if isinstance(trajectory_equation, str):
        print(trajectory_equation)
        return
    print(trajectory_equation)  # Important

    # Step 5: Orbital Dynamics
    orbital_dynamics = OrbitalDynamics(target_orbit=altitude[0])
    orbital_velocity = orbital_dynamics.calculate_orbital_velocity()
    print(f"Calculated orbital velocity for maintaining the target orbit: {orbital_velocity:.2f} m/s")

    # Step 6: Collision Detection
    collision_detector = CollisionDetection(altitude[0], trajectory_equation)

    # Perform Collision Detection
    collisions = collision_detector.check_collision()

    # Display the results and handle collisions
    if collisions:
        for collision in collisions:
            t, satellite_name, distance = collision
            print(f"Collision detected at t={t:.2f}s with {satellite_name} at a distance of {distance:.2f} km.")

        # Step 6.1: Optimize Trajectory to Avoid Collision
        print("Collision detected, optimizing trajectory...")
        trajectory_optimizer = TrajectoryOptimizer(trajectory_equation, collisions)
        optimized_trajectory = trajectory_optimizer.optimize_trajectory()
        print("Optimized Trajectory Calculated.")
    else:
        print("No collisions detected.")
        optimized_trajectory = trajectory_equation

    # Step 7: Trajectory Visualization
    trajectory_visualizer = TrajectoryVisualization(optimized_trajectory)
    trajectory_visualizer.plot_trajectory()

    # Step 8: Generate Mission Report
    mission_data = {
        "Rocket_Type": summary['Rocket_Type'],
        "Launch_Site": summary['Launch_Site'],
        "Target_Orbit": altitude[0],
        "Collisions": collisions
    }
    mission_report = MissionReport(mission_data)
    report = mission_report.generate_report()
    print(report)

    # Save report to file
    mission_report.save_report("mission_report.txt")

    # Step 9: Development of Website (Placeholder)
    print("Website development is in progress...")

if __name__ == "__main__":
    main()
