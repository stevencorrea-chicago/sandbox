class VariableManager:
    def __init__(self, variables=None):
        """
        Initialize the VariableManager with an optional dictionary of variables.
        """
        if variables is None:
            variables = {}
        if not isinstance(variables, dict):
            raise TypeError("variables must be a dictionary")
        self._variables = variables

    def get_variables(self):
        """
        Return the entire dictionary of variables.
        """
        return self._variables

    def get_variable(self, key_path):
        """
        Get the value of a variable by key path (supports nested keys with dot notation).
        Example: "engine.type" -> returns "V6"
        """
        keys = key_path.split(".")
        value = self._variables
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return None
        return value

    def set_variables(self, variables):
        """
        Replace the entire dictionary of variables.
        """
        if not isinstance(variables, dict):
            raise TypeError("variables must be a dictionary")
        self._variables = variables

    def set_variable(self, key_path, value):
        """
        Set or update a variable by key path (supports nested keys with dot notation).
        Example: "engine.horsepower" -> sets horsepower to new value.
        """
        keys = key_path.split(".")
        d = self._variables
        for k in keys[:-1]:
            if k not in d or not isinstance(d[k], dict):
                d[k] = {}
            d = d[k]
        d[keys[-1]] = value

    def add_variable(self, key_path, value):
        """
        Add a new variable (nested if needed).
        """
        self.set_variable(key_path, value)

    def delete_variable(self, key_path):
        """
        Delete a variable by key path. Returns True if deleted, False if not found.
        Example: "engine.type" -> deletes the 'type' key inside 'engine'.
        """
        keys = key_path.split(".")
        d = self._variables
        for k in keys[:-1]:
            if k not in d or not isinstance(d[k], dict):
                return False
            d = d[k]
        if keys[-1] in d:
            del d[keys[-1]]
            return True
        return False
    

if __name__ == "__main__":
    # Example usage with car parts dictionary
    car_parts = {
        "engine": {"type": "V6", "horsepower": 300, "fuel": "gasoline"},
        "wheels": {"count": 4, "size_in_inches": 18, "material": "alloy"},
        "interior": {"seats": "leather", "infotainment": "touchscreen", "airbags": 6}
    }

    manager = VariableManager(car_parts)
    print("Initial variables:", manager.get_variables())

    # Get nested variable
    print("Engine type:", manager.get_variable("engine.type"))

    # Update nested variable
    manager.set_variable("engine.horsepower", 350)
    print("Updated horsepower:", manager.get_variable("engine.horsepower"))

    # Add new nested variable
    manager.add_variable("lights.headlights", "LED")
    print("Added headlights:", manager.get_variable("lights.headlights"))

    # Delete nested variable
    deleted = manager.delete_variable("interior.seats")
    print("Deleted seats:", deleted)
    print("Final variables:", manager.get_variables())