class Automobile:
    def __init__(self,dictionary):
        self.auto_desc_dict = dictionary

    def __str__(self):
        string = ''
        for k,v in self.auto_desc_dict.items():
            string = '{}{}: {}\n'.format(string,k,v)
        return string 



dictionary = {'Make':'Toyota','Model':'Sienna','Engine':'3.4L','Transmission':'CVT','Radio':'AM/FM/Sirius/CD/Bluetooth','Cruise Control':'Adaptive cruise control','Heated Seats':'Driver and Passenger heated seats','Tilt Wheel':'Power','Telescoping Column':'Manual','Width':'62 inches','Length':'120 inches','Weight':'3700 lbs','Suspension':'Independent wishbone'}

car1 = print(Automobile(dictionary))
