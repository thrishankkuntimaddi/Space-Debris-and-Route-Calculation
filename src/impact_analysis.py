# def generate_report(self):
#     """
#     Generates a mission report based on mission data.
#     """
#     report = f"Mission Report:\n"
#     report += f"====================\n"
#     report += f"Rocket Type: {self.mission_data['Rocket_Type']}\n"
#     report += f"Launch Site: {self.mission_data['Launch_Site']}\n"
#     report += f"Target Orbit Altitude: {self.mission_data['Target_Orbit']} km\n"
#     report += f"--------------------\n"
#     if self.mission_data['Collisions']:
#         report += f"Collisions Detected: {len(self.mission_data['Collisions'])}\n"
#         report += "Details of Collisions:\n"
#         for collision in self.mission_data['Collisions']:
#             t, name, distance = collision
#             report += f"- Time of Collision: t={t:.2f} seconds\n"
#             report += f"  Colliding Object: {name}\n"
#             report += f"  Distance at Collision: {distance:.2f} km\n"
#             report += "--------------------\n"
#         report += "Impact Analysis:\n"
#         for impact in self.mission_data['Impact_Data']:
#             report += f"- Time of Impact: t={impact['Time']:.2f} seconds\n"
#             report += f"  Colliding Object: {impact['Object']}\n"
#             report += f"  Impact Energy: {impact['Impact_Energy']:.2e} J\n"
#             report += "--------------------\n"
#     else:
#         report += "No Collisions Detected\n"
#     report += "====================\n"
#     return report