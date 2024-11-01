from orbit_selection import OrbitSelector
from rocket_parameters import RocketParameters
from trajectory_to_selected_orbit import TrajectoryCalculator
from collision_avoidance import CollisionDetection

def main():
    # Step 1: Input timestamp for the mission
    # mission_timestamp = input("Enter the launch timestamp (YYYY-MM-DDTHH:MM:SS): ")  # 2024-10-30T12:00:00

    # Step 2: Select orbit(distance away from Earth's surface) for the mission
    selected_altitude = OrbitSelector()
    altitude = selected_altitude.select_orbit()
    user_select_orbit = altitude[0]
    # print(str(altitude[0]) + "km")
    print(altitude)

    # Step 3: Rocket Parameters
    params = RocketParameters()
    # rocket_list = params.get_rockets_for_range(altitude[0], altitude[1], altitude[2])
    # # print(rocket_list)
    summary = params.check_rocket_criteria(altitude[0], altitude[1], altitude[2])
    print(summary)

    # rocket_type = summary['Rocket_Type']
    # launch_site = summary['Launch_Site']
    # target_orbit = altitude[0]

    # Step 4: Trajectory Calculation for Rocket
    trajectory_calculator = TrajectoryCalculator()
    trajectory_equation = trajectory_calculator.calculate_trajectory(
            rocket_type= summary['Rocket_Type'],
            launch_site= summary['Launch_Site'],
            target_orbit= altitude[0]
        )
    print(trajectory_equation) # Important

    # Step 5: Orbital Dynamics

    # Step 6: Collision Detection
    collision_detector = CollisionDetection(altitude[0], trajectory_equation)

    # Perform Collision Detection
    collisions = collision_detector.check_collision()

    # Display the results
    if collisions:
        for collision in collisions:
            t, satellite_name, distance = collision
            print(f"Collision detected at t={t:.2f}s with {satellite_name} at a distance of {distance:.2f} km.")
    else:
        print("No collisions detected.")

    # Step 7: Mission_report.py



if __name__ == "__main__":
    main()
