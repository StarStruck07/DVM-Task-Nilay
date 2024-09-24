"""
I have created two excel sheets, one for data of all the
rooms added, and one for all the bookings made. This allows
us to see data of any room which may not have been booked
"""
import pandas as pd
from datetime import datetime, timedelta, date
excel_bookings = 'Bookings.xlsx'
excel_rooms = 'rooms.xlsx'
class Hotel:
    def __init__(self,name):
        self.name  = name
        self.rooms = []
        self.df_bookings = pd.read_excel(excel_bookings) if pd.ExcelFile(excel_bookings) else pd.DataFrame()
        self.df_rooms = pd.read_excel(excel_rooms) if pd.ExcelFile(excel_rooms) else pd.DataFrame()
    def load_rooms(self):
        for _, row in self.df_rooms.iterrows():
            room = Room(self, row['Room Number'], row['Price'], row['Room Type'])
            self.rooms.append(room)
    def load_bookings(self):
        for _, row in self.df_bookings.iterrows():
            room = next((r for r in self.rooms if r.room_number == row['Room Number']), None)
            if room:
                room.booked_dates.append(pd.date_range(start=row['Start Date'], end=row['End Date']).to_list())
    
    
    def add_room(self,room):
        self.rooms.append(room)
        self.df_rooms = self.df_rooms._append({'Hotel': str(room.hotel.name),'Room Number': int(room.room_number), 'Room Type': str(room.room_type), 'Price': int(room.price)}, ignore_index=True)
        self.df_rooms.to_excel(excel_rooms, index=False)
    def available_rooms(self,start_date,end_date):
        available = [room for room in self.rooms if room.avail(start_date,end_date)]
        return  available
    def book_room(self,customer,booking,room,start_date,end_date):
        self.df_bookings = self.df_bookings._append({'Hotel': str(room.hotel.name), 'Customer Name': str(customer.name),'Room Number': int(room.room_number),'Start Date': start_date,'End Date': end_date,'Total Price': booking.price(),'Room Type': str(room.room_type),'Price': int(room.price)}, ignore_index = True)
        self.df_bookings.to_excel(excel_bookings, index=False)
    
class Customer:
    def __init__(self,name,email,phone):
        self.name = name
        self.email = email
        self.phone = phone
        self.bookings = []
    def add_booking(self,booking):
        self.bookings.append(booking)
class Booking:
    def __init__(self,room,customer,start_date,end_date):
        self.room = room
        self.start_date =  start_date
        self.end_date = end_date
        self.booking_id = len(customer.bookings) + 1
        self.total_price = self.price()
        self.customer = customer
    def price(self):
        total_price = int(self.room.price) * int(len(pd.date_range(start = self.start_date,end = self.end_date)))
        return total_price     
class Room:
    def __init__(self,hotel,room_number,price,room_type):
        self.room_number = room_number
        self.price = price
        self.room_type = room_type
        self.booked_dates = []
        self.df = pd.read_excel('Bookings.xlsx')
        self.hotel = hotel
    def avail(self, start_date, end_date):
        req = pd.date_range(start=start_date, end=end_date).to_list()
        for dates in self.booked_dates:
            if any(date in dates for date in req):
                return False
        return True

    def book(self,start_date,end_date):
        self.booked_dates.append(pd.date_range(start=start_date,end=end_date).to_list())
def main():
    hotels = {}
    while True:
        print("1.Add room")
        print("2.View rooms")
        print("3.Book room")
        print("4.Exit")

        choice = input("Enter your choice number: ")
        if choice == "1":
            hotel_name = input("Enter hotel name: ")
            if hotel_name not in hotels:
                hotels[hotel_name] = Hotel(hotel_name)
            hotel = hotels[hotel_name]
            room_number = input("Enter room number: ")
            price = input("Enter price: ")
            room_type = input("Enter room type: ")
            room = Room(hotel,room_number,price,room_type)
            hotel.add_room(room)
            print("Room added!")
        elif choice == "2":
            start_date = date.fromisoformat(input("Enter start date (YYYY-MM-DD): "))
            end_date = date.fromisoformat(input("Enter end date (YYYY-MM-DD): "))
            available_rooms_found = False
            for hotel in hotels.values():
                available_rooms = hotel.available_rooms(start_date, end_date)
                if available_rooms:
                    available_rooms_found = True
                    print(f"\nAvailable rooms in {hotel.name}:")
                    for room in available_rooms:
                        print(f"Room number: {room.room_number}, Room type: {room.room_type}, Price: {room.price}")
            if  not available_rooms_found:
                print("\nNo available rooms found.")
        elif choice == "3":
            custumer_name = input("Enter custimer name: ")
            email = input("Enter your email: ")
            phone = input("Enter your phone number: ")
            customer = Customer(custumer_name,email,phone)
            hotel_name =  input("Enter hotel name: ")
            hotel = hotels[hotel_name]
            room_number = input("Enter room numbe: ")
            start_date = date.fromisoformat(input("Enter start date (YYYY-MM-DD): "))
            end_date = date.fromisoformat(input("Enter end date (YYYY-MM-DD): "))
            for room in hotel.rooms:
                if room.room_number == room_number:
                    booking =  Booking(room,customer,start_date,end_date)
                    room.book(start_date,end_date)
                    hotel.book_room(customer, booking, room, start_date, end_date)
                    print("Room booked successfully!")
                    break
            else:
                print("Room not found!")
        elif choice == "4":
            break
        else:
            print("Invalid choice!")
if __name__ == "__main__":
    main()
