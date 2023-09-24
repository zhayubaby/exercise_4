import sqlite3
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# Function to add reservations to the database
def add_reservation():
    reservation_id = input("Enter ReservationID: ")
    book_id = input("Enter BookID: ")
    user_id = input("Enter UserID: ")
    reservation_date = input("Enter ReservationDate: ")
    
    cursor.execute("INSERT INTO Reservations VALUES (?, ?, ?, ?)", (reservation_id, book_id, user_id, reservation_date))
    conn.commit()

add_reservation()

# add_reservation('LR001', 'LB001', 'LU001', '2020-01-01')
# add_reservation('LR002', 'LB002', 'LU002', '2020-01-02')
# add_reservation('LR003', 'LB003', 'LU003', '2020-01-03')
# add_reservation('LR004', 'LB004', 'LU005', '2020-01-04')
# add_reservation('LR005', 'LB005', 'LU004', '2020-01-05')


