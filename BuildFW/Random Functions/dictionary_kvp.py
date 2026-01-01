def search_car(*,make=None,model=None,trim=None,country_of_origin=None):

        # --- Text fields ---
        for field, value in {"make": make, "model": model, "trim": trim, "country_of_origin": country_of_origin}.items():
            if value:
                print(f"Searching {field} for value: {value}")


car_dictionary = [
    {"make": "Toyota", "model": "Avalon", "trim": "Limited", "country_of_origin": ""},
    {"make": "Honda", "model": "Civic", "trim": "EX", "country_of_origin": "Japan"},
    {"make": "Ford", "model": "Mustang", "trim": "", "country_of_origin": "USA"},
                ]
    
for car in car_dictionary:
    search_car(**car)    
    
def find_country_capital(**kwargs):
    for key, value in kwargs.items():
        if value:
            print(f"The capital of {key} is {value}")
        else:
            print(f"The capital of {key} is not defined")
        
# Creating a dictionary
country_capitals = {
   "Germany": "Berlin",
   "Canada": "Ottawa",
   "England": "London",
    "France": ""
}

find_country_capital(**country_capitals)