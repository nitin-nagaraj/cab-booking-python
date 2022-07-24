import time
import math

# Main DB to store Driver Details
def Master_Data_Driver(Driver_Name, Driver_Contact_no, Driver_x_y_coordinates, Driver_Status, Vehicle_no,
                       Vehicle_Model_Name, Driver_Trip_Status):
    global Master_Driver
    Master_Driver[Driver_Contact_no] = [Driver_Name, Driver_x_y_coordinates, Driver_Contact_no, Driver_Status,
                                        Vehicle_no, Vehicle_Model_Name, Driver_Trip_Status]

# Main DB to store Rider Details
def Master_Data_Rider(Customer_Name, Customer_ContactNO, Status, Cust_x_y_coordinates):
    global Master_Rider
    Master_Rider[Customer_ContactNO] = [Customer_Name, Status, Cust_x_y_coordinates, Customer_ContactNO]

# Driver class
class Driver():
    def __init__(self, Driver_Name, Driver_Contact_no, Driver_Current_x_y_coordinates_in_ListFormat, Vehicle_no,
                 Vehicle_Model_Name, Driver_Status):
        self.Driver_Name = Driver_Name
        self.Driver_Contact_no = Driver_Contact_no
        self.Driver_x_y_coordinates = Driver_Current_x_y_coordinates_in_ListFormat
        self.Vehicle_Model_Name = Vehicle_Model_Name
        self.Vehicle_no = Vehicle_no
        self.Driver_Status = Driver_Status
        self.Driver_Trip_Status = False
        Master_Data_Driver(self.Driver_Name, self.Driver_Contact_no, self.Driver_x_y_coordinates, self.Driver_Status,
                           self.Vehicle_no, self.Vehicle_Model_Name, self.Driver_Trip_Status)

    # Driver account login interface
    def Driver_Account_Login_Page(self):
        print(
            f"-----------------------------\nHello, {self.Driver_Name}.Welcome to your account.Please find the account details below.\n-----------------------------\nName : {self.Driver_Name} \nContactNo : {self.Driver_Contact_no} \nVehicle No : {self.Vehicle_no}\nVehicle Model Name: {self.Vehicle_Model_Name}\nCab location : {self.Driver_x_y_coordinates}")
        if self.Driver_Status:
            print("Current Status : Available to accept a ride-----------------------------")
        else:
            print("Current Status : Unavailable to accept a ride\n-----------------------------")
    
        while True:
            try:
                x = int(input(
                    f"Please select an option from below and given option number as input \n 1.To change your Status \n 2.To update your Cabs location \n 3.To exit from your account and go to Main interface\n"))
                break
            except Exception:
                print("XXXX - Wrong input. Please try again - XXXX\n")
            
        if x == 1:
            self.Driver_Status_Updation()

        elif x == 2:
            self.Driver_Location_Updation()

        elif x == 3:
            Main_Interface()

        else:
            print("XXXX - Wrong input. Please try again - XXXX\n")
            self.Driver_Account_Login_Page()
        
    # Function to update availability status of driver
    def Driver_Status_Updation(self):
        global Master_Driver
        if Master_Driver[self.Driver_Contact_no][6] == True:
            print(
                "----------------------------------------------------\nYou currently have an ongoing trip. You can only change your status once your trip is completed. Please try when this trip ends.\n----------------------------------------------------")
            self.Driver_Account_Login_Page()
        else:
            y = input("Please enter AVAILABLE OR UNAVAILABLE : ").upper()
            if y == "UNAVAILABLE":
                Master_Driver[self.Driver_Contact_no][3] = False
                self.Driver_Status = False
                print(
                    "Your current status is : UNAVAILABLE, \n To recieve bookings please change your status.Thank you")
                print("----------------------------------------------------")
                self.Driver_Account_Login_Page()
            elif y == "AVAILABLE":
                Master_Driver[self.Driver_Contact_no][3] = True
                self.Driver_Status = True
                print(
                    "Your current status is : AVAILABLE, \n You will be assigned to the nearest rider as soon as a new booking requirement comes.\n Thank You")
                print("----------------------------------------------------")
                self.Driver_Account_Login_Page()
            else:
                print("XXXX - Wrong input. Please try again - XXXX\n")
                self.Driver_Status_Updation()
    
    # Function to update driver location
    def Driver_Location_Updation(self):
        if Master_Driver[self.Driver_Contact_no][6] == True:
            print(
                "----------------------------------------------------\nYou cannot update coordinates while your current trip is not ended.\n Please try after customer ends the trip\n----------------------------------------------------")
            self.Driver_Account_Login_Page()

        else:
            while True:
                try:
                    self.Driver_x_y_coordinates = list(
                        map(float, input("To update your location -> Please enter x , y coordinates with spaces").split()))
                    if self.Driver_x_y_coordinates == [] or self.Driver_x_y_coordinates[0] == None or \
                            self.Driver_x_y_coordinates[1] == None:
                        raise Exception()
                    break
                except Exception:
                    print("XXXX - Wrong input. Please try again - XXXX\n")
            Master_Driver[self.Driver_Contact_no][1] = self.Driver_x_y_coordinates
            print("Cool, Your new coordinates have been updated sucessfully.")
            self.Driver_Account_Login_Page()

# Rider class
class Rider(Driver):
    def __init__(self, Cust_name, Cust_Contact_no, Cust_x_y_coordinates):
        self.Cust_name = Cust_name
        self.Cust_Contact_no = Cust_Contact_no
        self.Cust_x_y_coordinates = Cust_x_y_coordinates
        self.Trip_Details = {}
        self.Trip_ID = None
        self.Search_Status = None
        self.Cust_Status = True
        self.Cur_Driver_Key = None
        Master_Data_Rider(self.Cust_name, self.Cust_Contact_no, self.Cust_Status, self.Cust_x_y_coordinates)

    # Rider account login interface
    def Rider_Account_Login_Page(self):
        print(
            f"----------------------------------------------------\nHello, {self.Cust_name}.Welcome to your account.Please find your account details below.\n----------------------------------------------------")
        print(
            f"Name : {self.Cust_name}\nContact No : {self.Cust_Contact_no}\nYour current Position : {self.Cust_x_y_coordinates} ")
        while True:
            try:
                no = int(input(
                    "Please select an option from below. Please choose option number as your input \n 1 - New Booking \n 2 - History of all previous rides \n 3 - End current ongoing trip  \n 4 - Exit from your account\n"))
                break
            except Exception:
                print("XXXX - Wrong input. Please try again - XXXX\n")

        if no == 1:
            self.Booking()

        if no == 2:
            self.History()

        if no == 3:
            self.End_Trip()

        if no == 4:
            Main_Interface()
        else:
            print("XXXX - Wrong input. Please try again - XXXX\n")
            self.Rider_Account_Login_Page()
    
    # Function to search the nearest available Driver
    def Availability_Search(self):
        global Master_Driver
        flag = 0
        for key, value in Master_Driver.items():
            if value[3] == True:
                Distance_Calculator = math.sqrt(
                    ((Master_Driver[key][1][0] - Master_Rider[self.Cust_Contact_no][2][0]) ** 2) + (
                                (Master_Driver[key][1][1] - Master_Rider[self.Cust_Contact_no][2][1]) ** 2))
                if Distance_Calculator > 10:
                    flag = 1
                    continue
                else:
                    value[3] = False
                    value[6] = True
                    return key
        return flag

    # Function to book a nearest driver for the rider
    def Booking(self):
        global Master_Driver
        while True:
            try:
                self.Cust_x_y_coordinates = list(map(float, (input(
                    "----------------------------------------------------\nPlease enter your current cordinates x , y with spaces: ").split())))
                if self.Cust_x_y_coordinates == [] or self.Cust_x_y_coordinates[0] == None or self.Cust_x_y_coordinates[
                    1] == None:
                    raise Exception
                break
            except Exception:
                print("XXXX - Wrong input. Please try again - XXXX\n")
        Master_Rider[self.Cust_Contact_no][2] = self.Cust_x_y_coordinates
        self.Search_Status = self.Availability_Search()

        if Master_Rider[self.Cust_Contact_no][1] == False:
            print(
                "----------------------------------------------------\nYou cannot book another ride while your current ride is still ongoing.\n Please end the trip to finish current ride and book another\n----------------------------------------------------")
            self.Rider_Account_Login_Page()
        elif self.Search_Status == 0:
            print(
                "----------------------------------------------------\nNo Cab Drivers are available at this time.Please try after sometime.We regret the inconvenice caused\n----------------------------------------------------")
            self.Rider_Account_Login_Page()
        elif self.Search_Status == 1:
            print(
                "----------------------------------------------------\nThere are no nearest Cabs available.Please try after Sometime\n----------------------------------------------------")
            self.Rider_Account_Login_Page()
        else:
            global x
            global Current_Live_Booking_Data
            Master_Rider[self.Cust_Contact_no][1] = False
            Master_Driver[self.Search_Status][5] = True
            Master_Driver[self.Search_Status][3] = False
            self.Trip_ID = int(str(self.Cust_Contact_no)[6:10])
            for y in self.Trip_Details.keys():
                if self.Trip_ID == y:
                    self.Trip_ID += 1

            Current_Live_Booking_Data[self.Trip_ID] = {"Trip_ID": self.Trip_ID,
                                                       "Driver_Name": Master_Driver[self.Search_Status][0],
                                                       "Rider_name": self.Cust_name,
                                                       "Vehicle_No": Master_Driver[self.Search_Status][4], "Date": x}
            self.Trip_Details[self.Trip_ID] = {"Trip_ID": self.Trip_ID,
                                               "Driver_Name": Master_Driver[self.Search_Status][0],
                                               "Vehicle_No": Master_Driver[self.Search_Status][4],
                                               "Driver_Contact_no": Master_Driver[self.Search_Status][2], "Date": x}
            print("Your Booking is confirmed \n", "Trip_ID is : ", self.Trip_ID, "\n", "Driver name is : ",
                  Master_Driver[self.Search_Status][0], "\n", "Vehicle No : ", Master_Driver[self.Search_Status][4],
                  "\n", "Driver Contact No :", Master_Driver[self.Search_Status][2], "\n", "Date : ", x)
            self.Cur_Driver_Key = self.Search_Status
            self.Rider_Account_Login_Page()
    
    # Function to end Rider trip
    def End_Trip(self):
        if Master_Rider[self.Cust_Contact_no][1] == True:
            print(
                "----------------------------------------------------\nThere is no ogoing trip to end.\n----------------------------------------------------")
            self.Rider_Account_Login_Page()
        else:
            Master_Rider[self.Cust_Contact_no][1] = True
            Master_Driver[self.Cur_Driver_Key][3] = True
            Master_Driver[self.Cur_Driver_Key][5] = False
            Current_Live_Booking_Data.pop(self.Trip_ID)

            print(
                "----------------------------------------------------\nYour Trip is ended.Thank you.\n----------------------------------------------------")
            self.Rider_Account_Login_Page()

    # Function to show ride history of the rider
    def History(self):
        if self.Trip_Details == {}:
            print(
                "----------------------------------------------------\nOops,You haven't taken a ride with us yet and there seems to be no ride history to show now. Start riding with us.\n----------------------------------------------------")
            self.Rider_Account_Login_Page()
        else:
            print("Your Ride history is as below : ")
            for keys, values in self.Trip_Details.items():
                print("----------------------------------------------------\nTrip_ID : ",
                      self.Trip_Details[keys]["Trip_ID"], "--", "Driver_Name : ",
                      self.Trip_Details[keys]["Driver_Name"], "--", "Vehicle_No : ",
                      self.Trip_Details[keys]["Vehicle_No"], "--", "Driver_Contact_no : ",
                      self.Trip_Details[keys]["Driver_Contact_no"], "--", "Date : ", self.Trip_Details[keys]["Date"],
                      "\n----------------------------------------------------")
            self.Rider_Account_Login_Page()


class Admin:
    def __init__(self, Admin_Name, Admin_ContactNo):
        self.Admin_Name = Admin_Name
        self.Admin_ContactNo = Admin_ContactNo
    
    # Function for Admin panel
    def Admin_Account_Login_Page(self):
        print(
            f"-----------------------------\nHello, {self.Admin_Name}.Welcome to your account.Please find your account details below.\n-----------------------------\nName : {self.Admin_Name} \nContactNo : {self.Admin_ContactNo}")

        while True:
            try:
                x = int(input(
                    f"Please select an option from below. Please choose option number as your input \n 1 - To view all the Current Ongoing Trips\n 2 - To view all the registered Riders and Drivers data\n 3 - To exit from your account and go to Main interface\n"))
                break
            except Exception:
                print("XXXX - Wrong input. Please try again - XXXX\n")

        if x == 1:
            self.All_Ongoing_Trips()

        elif x == 2:
            self.All_RidersAndDrivers_Info()

        elif x == 3:
            Main_Interface()

        else:
            print("XXXX - Wrong input. Please try again - XXXX\n")
            self.Admin_Account_Login_Page()
    
    # Function to display all current ongoing trips
    def All_Ongoing_Trips(self):
        print(
            "-----------------------------\nPlease find below the list of all ongoing Trips :\n-----------------------------")
        if Current_Live_Booking_Data == {}:
            print("Currently there seems to be no on-going trips")
        else:
            for key, value in Current_Live_Booking_Data.items():
                print(value)
        self.Admin_Account_Login_Page()
    
    # Function to display all Riders and Drivers Details
    def All_RidersAndDrivers_Info(self):
        print(
            "-----------------------------\nPlease find the list of all Registered Riders and Drivers :\n-----------------------------")
        if Master_Rider_Users == {}:
            print("Currently there are no Riders registered in the system")
        else:
            print("Riders info : \n-----------------")
            for key, value in Master_Rider_Users.items():
                print("[Rider name : ", value.Cust_name, ",", "Rider Contact No : ", value.Cust_Contact_no, "]")
        if Master_Driver_Users == {}:
            print("Currently there are no Drivers registered in the system")
        else:
            print("Drivers info : \n-----------------")
            for key, value in Master_Driver_Users.items():
                print("[Driver name: ", value.Driver_Name, ",", "Driver Contact No : ", value.Driver_Contact_no,
                      ", Driver Vehicle No : ", value.Vehicle_no, ", Vehicle Model Name : ", value.Vehicle_Model_Name,
                      "]")

        self.Admin_Account_Login_Page()


# Function for Rider interface
def Rider_Interface():
    print("-----------------------------\nWelcome to the Rider Interface\n-----------------------------")
    New_Existing = input(
        "--> If you are a new user, Enter [new] \n--> If you are an already Existing user, Enter [existing] \n--> If you wish to Exit, please enter [exit] to go to main interface\n").upper()
    if New_Existing == "NEW":
        while True:
            try:
                name = input("Please enter your Name : ")
                if name.strip() == "":
                    raise Exception()
                else:
                    break
            except Exception:
                print("Name cannot be blank.Please try again")
        while True:
            try:
                ContactNo = int(input("Please enter your 10-digit Contact no : "))
                if len(str(ContactNo)) < 10:
                    raise Exception()
                break
            except Exception:
                print("XXXX - You have entered an incorrect input. Please input your 10-digit mobile no again. - XXXX")
        while True:
            try:
                Cust_coordinates = list(
                    map(float, (input("Please enter your current location cordinates x , y with spaces : ").split())))
                if Cust_coordinates == [] or Cust_coordinates[0] == None or Cust_coordinates[1] == None:
                    raise Exception()
                break
            except Exception:
                print("XXXX - Incorrect input.Please try again - XXXX")
        Master_Rider_Users[ContactNo] = Rider(name, ContactNo, Cust_coordinates)
        Master_Rider_Users[ContactNo].Rider_Account_Login_Page()
    elif New_Existing == "EXISTING":
        while True:
            try:
                contactno = int(input("Please enter your 10-digit registered contact no : "))
                if len(str(contactno)) < 10:
                    raise Exception()
                break
            except Exception:
                print("XXXX - You have entered an incorrect input. Please input your 10-digit mobile no again. - XXXX")
        if contactno not in Master_Rider_Users.keys():
            print(
                "-----------------------------\nYou dont seem to be a registered user. Please create a account to continue.\n You will now be routed to the Rider interface again.\n-----------------------------")
            Rider_Interface()
        else:
            Master_Rider_Users[contactno].Rider_Account_Login_Page()

    elif New_Existing == "EXIT":
        Main_Interface()

    else:
        print("-----------------------------\nWrong input.You will now be routed back to the Rider Interface.")
        Rider_Interface()

# function for Driver Interface
def Driver_Interface():
    print("-----------------------------\nWelcome to the Driver Interface.\n-----------------------------")
    New_Existing = input(
        "--> If you are a new user, Enter [new] \n--> If you are an already Existing user, Enter [existing] \n--> If you wish to Exit, please enter [exit] to go to main interface\n").upper()

    if New_Existing == "NEW":
        while True:
            try:
                name = input("Please enter your name : ")
                if name.strip() == "":
                    raise Exception()
                else:
                    break
            except Exception:
                print("Name cannot be blank.Please try again")
        while True:
            try:
                ContactNo = int(input("Please enter your 10-digit Contact no : "))
                if len(str(ContactNo)) < 10:
                    raise Exception()
                break
            except Exception:
                print("XXXX - You have entered an incorrect input. Please input your 10-digit mobile no again. - XXXX")
        while True:
            try:
                cur_cordinates = list(map(float, input("Please enter your current location cordinates x , y with spaces : ").split()))
                if cur_cordinates == [] or cur_cordinates[0] == None or cur_cordinates[1] == None:
                    raise Exception()
                break
            except Exception:
                print("XXXX - Incorrect input.Please try again - XXXX")
        while True:
            try:
                vehicleNo = input("Please enter your vehicle no : ")
                if vehicleNo.strip() == "":
                    raise Exception()
                else:
                    break
            except Exception:
                print("Vehicle name cannot be blank.Please try again")
        while True:
            try:
                ModelName = input("Please enter your Vehicle Model Name : ")
                if ModelName.strip() == "":
                    raise Exception()
                else:
                    break
            except Exception:
                print("Vehicle Model Name cannot be blank.Please try again")

        while True:
            try:
                availability = input("Please enter your Availability. Enter YES if available, NO if not available : ").upper()
                if availability.strip() == "":
                    raise Exception()
                elif availability != "YES" and availability != "NO":
                    raise Exception()
                else:
                    break
            except Exception:
                print("XXXX - Incorrect input.Please try again - XXXX")
        if availability == "YES":
            availability = True
        else:
            availability = False
        Master_Driver_Users[ContactNo] = Driver(name, ContactNo, cur_cordinates, vehicleNo, ModelName, availability)
        Master_Driver_Users[ContactNo].Driver_Account_Login_Page()


    elif New_Existing == "EXISTING":
        while True:
            try:
                contactno = int(input("Please enter your 10-digit registered contact no : "))
                if len(str(contactno)) < 10:
                    raise Exception()
                break
            except Exception:
                print("XXXX - You have entered an incorrect input. Please input your 10-digit mobile no again. - XXXX")
        if contactno not in Master_Driver_Users.keys():
            print(
                "-----------------------------\nYou dont seem to be a registered user. Please create a account to continue.\n You will now be routed to the Driver interface again.")
            Driver_Interface()
        else:
            Master_Driver_Users[contactno].Driver_Account_Login_Page()
    elif New_Existing == "EXIT":
        Main_Interface()

    else:
        print("-----------------------------\nWrong input.You will now be routed back to the Driver Interface.\n-----------------------------")
        Driver_Interface()


# Function for the Admin interface
def Admin_Interface():
    print("-----------------------------\nWelcome to the Admin Interface.\n-----------------------------")
    New_Existing = input(
        "--> If you are a new user, Enter [new] \n--> If you are an already Existing user, Enter [existing] \n--> If you wish to Exit, please enter [exit] to go to main interface\n").upper()
    if New_Existing == "NEW":
        while True:
            try:
                name = input("Please enter your name : ")
                if name.strip() == "":
                    raise Exception()
                else:
                    break
            except Exception:
                print("Name cannot be blank.Please try again")
        while True:
            try:
                ContactNo = int(input("Please enter your contact no : "))
                if len(str(ContactNo)) < 10:
                    raise Exception()
                break
            except Exception:
                print("You have entered wrong input or Mobile no is not 10 digits.Please try again")

        Master_Admin[ContactNo] = Admin(name, ContactNo)
        Master_Admin[ContactNo].Admin_Account_Login_Page()
    elif New_Existing == "EXISTING":
        while True:
            try:
                contactno = int(input("Please enter your 10-digit Contact no : "))
                if len(str(contactno)) < 10:
                    raise Exception()
                break
            except Exception:
                print("XXXX - You have entered an incorrect input. Please input your 10-digit mobile no again. - XXXX")
        if contactno not in Master_Admin.keys():
            print(
                "-----------------------------\nYou dont seem to be a registered user. Please create a account to continue.\n You will now be routed to the Admin interface again.\n-----------------------------")
            Admin_Interface()
        else:
            Master_Admin[contactno].Admin_Account_Login_Page()

    elif New_Existing == "EXIT":
        Main_Interface()

    else:
        print("-----------------------------\nWrong input.You will now be routed back to Admin Interface.")
        Admin_Interface()


# Function for the Main interface.
def Main_Interface():
    global Master_Driver_Users
    global Master_Rider_Users
    print("------------ ************ ------------ \nHello & Welcome to Cab Booking Service Interface\n------------ ************ ------------ ")
    user = input(
        "--> If you are a rider, Please enter[RIDER] \n--> If you are a driver, Please enter [DRIVER] \n--> If you are the Admin, Please enter[ADMIN] \n--> If you wish to exit from the application, Please enter [EXIT] \n").upper()
    if user == "RIDER":
        Rider_Interface()

    elif user == "DRIVER":
        Driver_Interface()

    elif user == "ADMIN":
        Admin_Interface()

    elif user == "EXIT":
        quit()

    else:
        print("XXXX - Wrong input. Please try again - XXXX\n\n")
        Main_Interface()

if __name__ == "__main__":
    x = time.strftime("%d/%m/%y")
    Master_Rider_Users = {}
    Master_Driver_Users = {}
    Master_Rider = {}
    Master_Driver = {}
    Master_Admin = {}
    Current_Live_Booking_Data = {}
    Main_Interface()

#  