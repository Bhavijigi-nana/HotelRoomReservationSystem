import csv 
import os
from model import Reservation

class HotelManager:
    FILENAME = "reservations.csv"
    FIELDNAMES = [
        "BookingID",
        "GuestFirstName",
        "GuestLastName",
        "RoomNumber",
        "RoomType",
        "NightlyRates",
        "MaxSize",
        "isCheckedIn",
    ]

    def __init__(self):
        self.reservations = [] #empty list
        self.load_data()

    def load_data(self):
        if not os.path.exists(self.FILENAME):
            self._create_sample_file()

        try:
            with open(self.FILENAME, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                self.reservations = [
                    Reservation(
                        row["BookingID"].strip(),
                        row["GuestFirstName"].strip(),
                        row["GuestLastName"].strip(),
                        row["RoomNumber"].strip(),
                        row["RoomType"].strip(),
                        row["NightlyRates"].strip(),
                        row["MaxSize"].strip(),
                        row["isCheckedIn"].strip(),
                    )
                    for row in reader
                ]
        except Exception as e:
            print(f"Error reading file: {e}")

    def _create_sample_file(self): #private to class
        sample_data = [
           {
                "BookingID": "B101",
                "GuestFirstName": "John",
                "GuestLastName": "Doe",
                "RoomNumber": 101,
                "RoomType": "Single",
                "NightlyRates": 120.00,
                "MaxSize": 1,
                "isCheckedIn": True,
            },
            {
                "BookingID": "B102",
                "GuestFirstName": "Sarah",
                "GuestLastName": "Connor",
                "RoomNumber": 202,
                "RoomType": "Suite",
                "NightlyRates": 350.00,
                "MaxSize": 4,
                "isCheckedIn": False,
            },
            {
                "BookingID": "B103",
                "GuestFirstName": "Michael",
                "GuestLastName": "Scott",
                "RoomNumber": 105,
                "RoomType": "Double",
                "NightlyRates": 180.50,
                "MaxSize": 2,
                "isCheckedIn": True,
            },
        ]
        with open(self.FILENAME, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.FIELDNAMES)
            writer.writeheader()
            writer.writerows(sample_data)

    def save_data(self):
        try:
            with open(self.FILENAME, "w", newline="",encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=self.FIELDNAMES)
                writer.writeheader()
                writer.writerows([res.to_csv_dict() for res in self.reservations])
            print("Changes have been saved successfully")
        except Exception as e:
            print(f"Error writing to file: {e}")

    def prompt_valid_input(self, prompt, cast_type=str, validator=None, err_msg="Invalid input"):
        #cast_type=str - tells python what type of input it should be, strin default
        while True:
            try:
                val = cast_type(input(prompt).strip())
                if validator and not validator(val): # validator - checks if input is acceptable
                    print(f"Error: {err_msg}")
                    continue
                return val
            except ValueError:
                print(f"Error: {err_msg}")

    def add_reservation(self):
        print("===New Reservation===")
        existing_ids = {r.bookingID.lower() for r in self.reservations}
        bookingID=self.prompt_valid_input(
            "Enter Booking ID: ",
            validator=lambda x: len(x)>0 and x.lower() not in existing_ids,
            err_msg="Booking ID can't be empty and must be unique",
        )

        first_name = self.prompt_valid_input("Enter First Name: ", validator=lambda x: len(x)>0)
        last_name = self.prompt_valid_input("Enter Last Name: ", validator=lambda x: len(x)>0)

        existing_rooms = {r.room_details.roomNo for r in self.reservations}
        roomNo = self.prompt_valid_input(
            "Enter Room Number (100-999): ",
            cast_type=int,
            validator=lambda x: 100<= x <=999 and x not in existing_rooms,
            err_msg = "Room number must be 100-999 and not assigned to anyone"
        )

        valid_roomTypes = ["Single", "Double", "Suite"]
        roomType = self.prompt_valid_input(
            "Enter room Type (Single/Double/Suite): ",
            validator=lambda x: x.capitalize() in valid_roomTypes,
            err_msg="Room type can be Single/Double/Suite only",
        ).capitalize()

        nightlyRates = self.prompt_valid_input(
            "Enter Nightly Rates: ",
            cast_type=float,
            validator=lambda x: 50.0 <= x <=2000.0,
            err_msg="Rate must be between $50.00 and $2000.00",
        )
        maxSize = self.prompt_valid_input(
            "Enter Max Size: ",
            cast_type=int,
            validator=lambda x: 1<=x<=6,
            err_msg="Max number of people is from 1 to 6 only"
        )

        new_res = Reservation(
            bookingID,first_name,last_name,roomNo,roomType, nightlyRates,maxSize, False)
        self.reservations.append(new_res)
        self.save_data()
        print("Reservation has been added")

    def toggle_check_in_status(self):
        print("===Check In / Check Out===")
        bookingID = input("Enter bookingID: ").strip().lower()

        res = next((r for r in self.reservations if r.bookingId.lower() == bookingID), None)
        if not res:
            print("Booking ID not found.")
            return
        res.room_details.isCheckIn = not res.room_details.isCheckIn
        status_str = "Checked In" if res.room_details.isCheckIn else "Checked Out"
        self.save_data()
        print(f"Status has been updated for {res.guest_first} {res.guest_last}. {status_str}")

    def view_all_reservations(self):
        print("===All Reservations===")
        if not self.reservations:
            print("No records available")
            return
        for r in self.reservations:
            print(r)

    def filter_by_roomType(self):
        print("===Filter By Room Type===")
        queryType = input("Enter Room Type (Single/Double/Suite): ")
        match = [r for r in self.reservations if r.room_details.roomType.lower() == queryType]

        if match:
            for r in match:
                print(r)
        else:
            print("No matches found as per room type")

    def filter_by_status(self):
        print("===Filter by status===")
        print("1. Checked In\n2. Reserved")
        choice = input("Option: ")

        target_stat = choice =="1"
        match = [r for r in self.reservations if r.room_details.isCheckIn==target_stat]
        if match:
            for r in match:
                print(r)
        else:
            print("No rooms are checked in")

    def highest_rate_room(self):
        print("===Most Expensive Room===")
        if not self.reservations:
            print("No data in records")
            return

        max_rate = max(r.room_details.nightlyRates for r in self.reservations)
        print(f"Highest Nightly Rate: ${max_rate:.2f}")
        for r in self.reservations:
            if r.room_details.nightlyRates==max_rate:
                print(r)

    def revenue_analysis(self):
        print("===Revenue Analysis===")
        if not self.reservations:
            print("No data in records")
            return
        total_count = len(self.reservations)
        checked_in = [r for r in self.reservations if r.room_details.isCheckIn]
        checked_in_count = len(checked_in)

        active_revenue = sum(r.room_details.nightlyRates for r in checked_in)
        total_potential = sum(r.room_details.nightlyRates for r in self.reservations)
        occ_rate = (checked_in_count/total_count) * 100

        print(f"Total Reservations  : {total_count}")
        print(f"Currently Checked In: {checked_in_count}")
        print(f"Occupancy Rate      : {occ_rate:.1f}%")
        print(f"Current Daily Rev.  : ${active_revenue:.2f}")
        print(f"Max Potential Rev.  : ${total_potential:.2f}")

    def run(self):
        options = {
            "1": self.add_reservation,
            "2": self.toggle_check_in_status,
            "3": self.view_all_reservations,
            "4": self.filter_by_roomType,
            "5": self.filter_by_status,
            "6": self.highest_rate_room,
            "7": self.revenue_analysis,
        }

        while True:
            print("\n")
            print("   Grand Hotel Reservation System   ")
            print("=" * 35)
            print("1> Add new reservation.")
            print("2> Toggle Check-In / Check-Out status.")
            print("3> View all reservations.")
            print("4> Filter by room type.")
            print("5> Filter by status.")
            print("6> Highest rate room analysis.")
            print("7> Revenue & Occupancy Analysis.")
            print("8> Exit.")

            choice = input("\nEnter choice (1-8): ").strip()

            if choice == "8":
                print("Exiting system. Goodbye!")
                break
            elif choice in options:
                options[choice]()
            else:
                print("Invalid choice. Please select an option from 1 to 8.")

if __name__=="__main__":
    app = HotelManager()
    app.run()
