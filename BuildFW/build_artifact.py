from variable_manager import VariableManager
import pprint

def main():
    # Example usage with car parts dictionary
    car_parts = {
        "engine": {"type": "V6", "horsepower": 300, "fuel": "gasoline"},
        "wheels": {"count": 4, "size_in_inches": 18, "material": "alloy"},
        "interior": {"seats": "leather", "infotainment": "touchscreen", "airbags": 6}
    }

    pp = pprint.PrettyPrinter(indent=3)

    manager = VariableManager(car_parts)
    print("Initial variables:\n")
    pp.pprint(manager.get_variables())
    print("-" * 50)
    
    # Get nested variable    
    print("Engine Type:")
    pp.pprint(manager.get_variable("engine.type"))
    
    print("-" * 50)
    
    manager.set_variable("engine.horsepower", 350)
    print("Updated horsepower:")
    pp.pprint(manager.get_variable("engine.horsepower"))

    print("-" * 50)
    
    manager.set_variable("exterior.body_style", "sedan")
    print("Added body_style:")
    pp.pprint(manager.get_variable("exterior.body_style"))

    print("-" * 50)

    manager.set_variable("exterior.color", "green")
    print("Added color:")
    pp.pprint(manager.get_variable("exterior.color"))

    print("-" * 50)

    # Add new nested variable
    manager.add_variable("lights.headlights", "LED")
    print("Added headlights:")
    pp.pprint(manager.get_variable("lights.headlights"))

    print("-" * 50)

    # Delete nested variable
    deleted = manager.delete_variable("interior.seats")
    print("Deleted seats:", deleted)
    print("Final variables:")
    pp.pprint(manager.get_variables())

if __name__ == "__main__":
    main()
