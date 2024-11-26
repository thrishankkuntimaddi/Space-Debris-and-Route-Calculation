# TLE-Based Space Debris Detection and Trajectory Optimization Using Double Deep Q-Learning and Dynamic Collision Avoidance 🚀
# Optimized Space Debris Avoidance and Trajectory Planning System

This repository contains the implementation of **TLE-Based Space Debris Detection and Trajectory Optimization** using advanced techniques like **Double Deep Q-Learning** and **Dynamic Collision Avoidance**. The project aims to provide an efficient solution for space debris management and safe route planning for satellites and spacecraft, utilizing data from **Two-Line Elements (TLE)**.

The system includes features for:

- **Space Debris Detection**
- **Trajectory Optimization**
- **Dynamic Collision Avoidance**

Leveraging **Deep Reinforcement Learning** and **orbital mechanics**, the project simulates and optimizes spacecraft trajectories to ensure safe navigation amidst space debris.

---

## 🔧 Features

- **TLE-Based Space Debris Detection**: Utilizes TLE data to detect space debris in orbit, providing accurate tracking of debris positions.
- **Double Deep Q-Learning**: Applies reinforcement learning for optimal trajectory planning, ensuring efficient avoidance of detected debris.
- **Dynamic Collision Avoidance**: Continuously monitors trajectories to dynamically adjust spacecraft routes, avoiding potential collisions.
- **Visualizations**: 3D visualization of the initial trajectory and dynamic updates to highlight the impact of debris detection and avoidance.

---

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/thrishankkuntimaddi/Space-Debris-and-Route-Calculation.git
   cd Space-Debris-and-Route-Calculation
   ```

2. **Install dependencies**:
   Ensure Python is installed, then install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the simulations**:
   - Update the TLE data in `tle_data.csv` for the latest debris information.
   - Run the main script:
   ```bash
   python mission_planner.py
   ```

---

## ⚙️ Configuration

- **TLE Data**: Update the `tle_data.csv` file with the latest Two-Line Elements data to ensure accurate debris detection.
- **Trajectory Parameters**: Configure parameters in `mission_planner.py` for mission-specific trajectory optimization and debris avoidance.
- **Collision Avoidance Sensitivity**: Adjust thresholds for collision detection sensitivity in `double_deep_dynamic_collision_detection.py` to tune the system.

---

## 📂 Project Structure

- `src/`
  - `mission_planner.py` - The main script to plan and execute mission trajectories.
  - `mission_report.py` - Generates mission reports and logs.
  - `orbit_selection.py` - Handles the selection of optimal orbits based on debris data.
  - `rocket_selection.py` - Includes `rocket_parameters.csv` for selecting appropriate rockets.
  - `initial_trajectory.py` - Computes the initial trajectory based on mission parameters.
  - `initial_trajectory_visualization.py` - Provides visualization of the initial computed trajectory.
  - `double_deep_dynamic_collision_detection.py` - Core module for debris detection, collision avoidance, and trajectory optimization using Double Deep Q-Learning.
  - `timestamp.py` - Manages timing and scheduling for mission phases.

---

## 📈 Future Enhancements

- **Advanced Reinforcement Learning Techniques**: Integrate more sophisticated reinforcement learning algorithms to further enhance trajectory optimization.
- **Real-Time TLE Updates**: Automate the updating of TLE data to ensure real-time accuracy in space debris tracking.
- **Mobile Interface**: Develop a mobile application for mission monitoring and real-time trajectory updates.
- **Extended Visualization Tools**: Include interactive visual tools for analyzing debris patterns and optimizing trajectories.

---

## 🤝 Contributing

This project is open for contributions! Feel free to fork the repository, make changes, and submit a pull request. Your suggestions and enhancements are always welcome to improve space safety.

---

## 📞 Contact

For any questions or support, feel free to reach out to [Thrishank Kuntimaddi](https://github.com/thrishankkuntimaddi).
