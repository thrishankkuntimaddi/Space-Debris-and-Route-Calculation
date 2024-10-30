purpose = "Generates and saves a comprehensive report of the mission, summarizing the flight details."

'''
1. Collect Data for Report
   - Gather launch time, path, avoided debris, total time of journey, and time when the rocket enters selected orbit.
2. Generate and Save Report
   - Save report in `final-report.txt` with all details.
'''

class MissionReport:
    def __init__(self):
        self.report_content = ""  # Stores the generated mission report content
    def generate_report(self, rocket_params, adjusted_trajectory, optimized_trajectory, tle_data):
        """
        Generate a report of the mission.
        """
        launch_time_formatted = rocket_params.launch_time.replace('T', ' ').replace('-', '/')
        if adjusted_trajectory['collision_detected']:
            collision_status = "Collision detected and optimized"
            colliding_object_info = f"Collision with TLE Object {adjusted_trajectory['colliding_object']} at position {tle_data[adjusted_trajectory['colliding_object']][0]}"
        else:
            collision_status = "No collision detected"
            colliding_object_info = ""

        report = f"""
        Mission Report:

        Initial Launch Parameters:
        Launch Time: {launch_time_formatted}
        Launch Site: {rocket_params.launch_site['name']}, {rocket_params.launch_site['address']}
        Rocket Type: {rocket_params.rocket_type}
        Target Orbit Range: {rocket_params.target_orbit_min} km - {rocket_params.target_orbit_max} km

        Collision Status:
        {collision_status}
        {colliding_object_info}

        Adjusted Trajectory (if collision detected):
        Initial Position: {adjusted_trajectory['adjusted_trajectory']['initial_position']}
        Adjusted Velocity: {adjusted_trajectory.get('adjusted_velocity', 'N/A')}
        Target Orbit Range: {adjusted_trajectory['adjusted_trajectory']['target_orbit_range']}

        Optimized Trajectory:
        Optimization Status: {'Yes' if optimized_trajectory.get('optimized') else 'No'}
        """
        with open("mission_report.txt", "w") as file:
            file.write(report)
        print("Mission report generated.")

