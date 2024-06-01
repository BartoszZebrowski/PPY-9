import json
import numpy as np
import streamlit as st
from booking import Booking
from car import Car
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

cars = [
    Car(1, "Toyota", "Corolla", 500),
    Car(2, "Volkswagen", "Golf", 600),
    Car(3, "Ford", "Focus", 550),
    Car(4, "BMW", "3 Series", 800),
    Car(5, "Audi", "A6", 750),
]

bookings = []


with open("bookings.json", 'r') as file:
    data = json.loads(file.read())
    [bookings.append(Booking.mapFromJson(x, cars)) for x in data]



st.title("Wyoporzyczanie samochodow")

menu = ["Sprawdź dostępne samochody", "Wypożycz samochod", "Sprawdź swoje wypożyczenia", "Wykres wypożyczeń"]
choice = st.sidebar.selectbox("Menu", menu)

    
if choice == "Sprawdź dostępne samochody":
    st.header("Sprawdź dostępne samochody")
    st.table(pd.DataFrame([(car.id, car.brand, car.model, car.costPerDay) for car in cars], columns=("ID", "Marka", "Model","Koszt za dzien")))
    
    
elif choice == "Wypożycz samochod":
    st.header("Wypożycz samochod")
    
    st.write("Dostepne samochody")
    st.table(pd.DataFrame([(car.id, car.brand, car.model, car.costPerDay) for car in cars], columns=("ID", "Marka", "Model","Koszt za dzien")))
    
    userId = st.number_input("ID uzytkownika", 0, 1000, 0)
    carId = st.number_input("ID samochodu", 0, 1000, 0)
    dateFrom = st.date_input("Od dnia")
    days = st.number_input("Ilosc dni", 0, 1000, 0)
    
    book = st.button("Wyporzycz")
    
    car = cars[carId - 1]
    
    if(book):
        booking = Booking(userId, car, dateFrom, days)
        bookings.append(booking)
        
            
elif choice == "Sprawdź swoje wypożyczenia":
    st.header("Sprawdź wypozyczenia")
    
    userId = st.number_input("Podaj ID uzytkownika", 0, 1000, 0)
    nextt = st.button("Dalej")
    
    if nextt:
        userBookings = []
        for booking in bookings:
            if booking.userId == userId:
                userBookings.append(booking)
    
        if len(userBookings) > 0: 
            st.table(pd.DataFrame([(booking.userId, booking.car.brand + booking.car.model, booking.dateFrom, booking.days, booking.cost) for booking in userBookings], columns=("ID Uzytkownika", "Samochod","Od dnia", "Ilosc dni", "Koszt")))
        else:
            st.write("Brak wyporzyczen dla tego uzytkownika") 
    
    
elif choice == "Wykres wypożyczeń":
    st.header("Wykres wypożyczeń")
    
    currentMonth = datetime.now().month
    bookingsForCurrentMonth = [booking for booking in bookings if datetime.strptime(booking.dateFrom, "%Y-%m-%d").month == currentMonth]
    
    days = {}
    
    for day in range(1, 31):
        days[day] = 0
    
    for day in range(1, 31):
        for booking in bookingsForCurrentMonth:
            if datetime.strptime(booking.dateFrom, "%Y-%m-%d").day == day:
                x = days[day]
                days[day] = x + 1

    st.line_chart(days)
    


with open("bookings.json", 'w') as file:
    json.dump([booking.getJson() for booking in bookings], file)
    


# if(goToMenu)

# st.write(userID)

