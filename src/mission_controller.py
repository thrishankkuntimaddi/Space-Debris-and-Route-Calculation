purpose = "Controls the entire mission flow, calling each module sequentially and managing input/output."

steps = ''' 

1. Declare Constants
2. Initialize Input Parameters
   - Gather `timestamp` (launch date & time).
   - Determine `orbit selection` (distance from Earth’s atmosphere).
3. Invoke Rocket_Description Module
4. Invoke Orbital_Mechanism Module 
   - Pass `timestamp` to calculate current orbital parameters.
5. Invoke Calculate_Route Module
   - Provide data from `orbital mechanism`, `rocket description`, `timestamp`, and `orbit distance`.
6. Invoke Collision_Detection Module
   - Send `orbital mechanism` and calculated route path.
   - If collision is detected, re invoke Calculate_Route for optimization.
7. Generate Report
   - If no collisions are detected, invoke Generate_Report to output results.

'''


from rocket_parameters import RocketParameters
from orbital_dynamics import OrbitalDynamics
from trajectory_to_selected_orbit import TrajectoryPlanner
from collision_avoidance import CollisionAvoidance
from trajectory_optimizer import TrajectoryOptimizer
from mission_report import MissionReport
from trajectory_visualization import TrajectoryVisualization

def main():
    # Step 1: Set up Rocket Parameters
    rocket_params = RocketParameters()
    rocket_params.setup_rocket_parameters()

    # Step 2: Retrieve TLE Data for Orbital Dynamics
    tle_data = [  # TLE data for 6 objects
        ('1 25544U 98067A   23056.52976417  .00000246  00000-0  13600-4 0  9994',
         '2 25544  51.6445 44.7525 0006907  83.5106 276.5852 15.48916369257430'),
        ('1 27691U 03004A   23056.53875874  .00000027  00000-0  37995-4 0  9992',
         '2 27691  98.2076 75.2345 0014025  96.2123 264.0261 14.57105424564794'),
        ('1 38734U 12048A   23056.52786865  .00001269  00000-0  71723-4 0  9993',
         '2 38734  55.0012 221.5678 0012345  34.5678 325.6789 15.03456789123456'),
        ('1 41025U 15075A   23056.51234567  .00000567  00000-0  45678-4 0  9997',
         '2 41025  97.1234 150.6789 0003456 120.4567 239.8765 14.67890123456789'),
        ('1 43210U 18090A   23056.51234567  .00000891  00000-0  56789-4 0  9990',
         '2 43210  98.7654 210.1234 0016789  78.9012 281.2345 14.45678901234567'),
        ('1 50000U 21000A   23056.52976417  .00000246  00000-0  15000-4 0  9991',  # This TLE is intended to cause a collision
         '2 50000  51.6445 100.7525 0007000  80.0000 276.5852 15.48916369257430')
    ]

    # Step 3: Calculate Initial Positions (Orbital Dynamics)
    orbital_dynamics = OrbitalDynamics()
    positions = orbital_dynamics.calculate_positions(tle_data, rocket_params.launch_time)

    # Step 4: Plan Initial Trajectory
    trajectory_planner = TrajectoryPlanner()
    trajectory = trajectory_planner.plan_trajectory(rocket_params, positions)

    # Step 5: Collision Detection and Avoidance
    collision_avoidance = CollisionAvoidance()
    adjusted_trajectory = collision_avoidance.detect_and_adjust(trajectory, positions)

    # Step 6: Optimize Trajectory
    trajectory_optimizer = TrajectoryOptimizer()
    optimized_trajectory = trajectory_optimizer.optimize_trajectory(adjusted_trajectory)

    # Step 7: Visualize Trajectory
    trajectory_visualization = TrajectoryVisualization()
    trajectory_visualization.visualize_collision_trajectory(trajectory, adjusted_trajectory, optimized_trajectory, positions)
    trajectory_visualization.visualize_no_collision_trajectory(trajectory, optimized_trajectory)

    # Step 8: Generate Mission Report
    mission_report = MissionReport()
    mission_report.generate_report(rocket_params, adjusted_trajectory, optimized_trajectory, tle_data)

if __name__ == "__main__":
    main()
