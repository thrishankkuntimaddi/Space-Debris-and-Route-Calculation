def choose_module():
    print("Select the collision detection module:")
    print("1. collision_detection.py")
    print("2. dynamic_collision_detection.py")
    print("3. collision_detection_evaluation_matrix.py")
    print("4. collision_detection_deep_q_approach")

    choice = input("Enter the number of your choice: ")

    module_name = None
    name = None
    if choice == '1':
        module_name = "collision_detection"
        name = "CollisionDetection"
    elif choice == '2':
        module_name = "dynamic_collision_detection"
        name = "CollisionDetectionDynamics"
    elif choice == '3':
        module_name = "collision_detection_evaluation_matrix"
        name = "CollisionDetectionEval"
    elif choice == '4':
        module_name = "collision_detection_deep_q_approach."
        name = "CollisionDetectionDeep"
    else:
        print("Invalid choice. Please select a valid option.")

    if module_name:
        print(f"You selected: {module_name}")
    return module_name, name

# Call the function to choose a module
# selected_module = choose_module()
