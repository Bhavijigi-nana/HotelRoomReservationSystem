class RoomDetails:

    #__init__ constructor - runs automatically when creating an object
    # self refers to the current obj that is being called    
    def __init__(self, roomNo, roomType, nightlyRates, maxSize, isCheckIn):
        self.roomNo = int(roomNo)
        self.roomType = roomType
        self.nightlyRates = float(nightlyRates)
        self.maxSize = int(maxSize)
        self.isCheckIn = str(isCheckIn).lower() in ("true", "1") # if true then saves in dbs as true

    #how room is displayed as text
    def __str__(self): #special method for string representation of obj
        status = "Checked In" if self.isCheckIn else "Reserved" 
        return( #the f is f-string, allows variable inside {}
            f"Room {self.roomNo} ({self.roomType}) | "
            f"Rate: ${self.nightlyRates:.2f}/night | " #2 digits after the decimal point
            f"Max People: {self.maxSize} | Status: {status}"
        )

#composition - Reservation has a RoomDetails object
# Reservation can't be done without RoomDetails
class Reservation: 
    def __init__(self, bookingID, guest_first, guest_last, roomNo, roomType, nightlyRates, maxSize, isCheckedIn):
        self.bookingId = bookingID
        self.guest_first = guest_first
        self.guest_last = guest_last
        self.room_details = RoomDetails(roomNo, roomType, nightlyRates, maxSize, isCheckedIn)

    def to_csv_dict(self): #converts objs to dictionary format for csv
        return {
            #key: value
            "BookingID" : self.bookingId,
            "GuestFirstName": self.guest_first,
            "GuestLastName": self.guest_last,
            "RoomNumber": self.room_details.roomNo,
            "RoomType": self.room_details.roomType,
            "NightlyRates": self.room_details.nightlyRates,
            "MaxSize": self.room_details.maxSize,
            "isCheckedIn": self.room_details.isCheckIn
        }

    def __str__(self):
        return(
            f"Booking ID: {self.bookingId} | "
            f"Guest: {self.guest_first} {self.guest_last} | "
            f"{self.room_details}"
        )

        

