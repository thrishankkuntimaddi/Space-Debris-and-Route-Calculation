class MissionReport:
    def __init__(self, mission_data):
        self.mission_data = mission_data

    def generate_report(self):
        """
        Generates a mission report based on mission data.
        """
        report = f"Mission Report:\n"
        report += f"Rocket Type: {self.mission_data['Rocket_Type']}\n"
        report += f"Launch Site: {self.mission_data['Launch_Site']}\n"
        report += f"Target Orbit: {self.mission_data['Target_Orbit']} km\n"
        if 'Collisions' in self.mission_data:
            report += f"Collisions Detected: {len(self.mission_data['Collisions'])}\n"
            for collision in self.mission_data['Collisions']:
                report += f"- Collision at t={collision[0]:.2f}s with {collision[1]} at {collision[2]:.2f} km\n"
        else:
            report += "No Collisions Detected\n"
        return report

    def save_report(self, file_path):
        """
        Saves the mission report to a file.
        """
        with open(file_path, 'w') as file:
            file.write(self.generate_report())
