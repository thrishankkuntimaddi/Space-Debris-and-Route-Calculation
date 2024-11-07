purpose = '''
inputs: space object, Future position, Future Velocity, co-ordinates(x, y, z) } as a dataset;  Trajectory equations utilising timestamp as main source 
outputs: 

    possibility 1: if collision detected - go to trajectory_optimizer.py
                    i/p: Trajectory Equation, TimeStamp
                    o/p: optimized Trajectory Equation 

                    ƒor more report: calling impact_analysis.py 
                    
    possibility 2: if no collision detected - go to mission_report.py 

'''

