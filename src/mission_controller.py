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
   - If collision is detected, reinvoke Calculate_Route for optimization.
7. Generate Report
   - If no collisions are detected, invoke Generate_Report to output results.

'''
