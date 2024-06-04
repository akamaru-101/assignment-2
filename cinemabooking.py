class SystemAdministrator:
    def __init__(self):
        self.moviesList = []
        self.screens = []
        self.timeslots = []

    def movieList(self, title, available_seats):
        movie = Movie(title, available_seats)
        self.moviesList.append(movie)
        return movie

    def screen(self, screen_number):
        screen = Screen(screen_number)
        self.screens.append(screen)
        return screen

    def timeSlot(self, starting, ending, screen, movie):
        timeslot = Timeslot(starting, ending, screen, movie)
        self.timeslots.append(timeslot)
        return timeslot

class User:
    def __init__(self, username):
        self.username = username

    def selectMovie(self, movie):
        return movie

    def selectSeats(self, movie, seats):
        return seats

    def reservation(self, movie, seats, screening):
        return BookingDetails(movie, seats, screening)


class Movie:
    def __init__(self, title, available_seats):
        self.title = title
        self.available_seats = available_seats
        self.bookings = []

    def Booking(self, user, seats):
        if len(seats) <= self.available_seats:
            self.bookings.append({
                'user': user,
                'seats': seats
            })
            self.available_seats -= len(seats)
            return True
        else:
            return False


class Screen:
    def __init__(self, number):
        self.number = number
        self.timeslots = []

    def add_timeslot(self, timeslot):
        self.timeslots.append(timeslot)


class Timeslot:
    def __init__(self, starting, ending, screen, movie):
        self.starting = starting
        self.ending = ending
        self.screen = screen
        self.movie = movie


class BookingDetails:
    bookingID = 0

    def __init__(self, movie, seats, screening):
        BookingDetails.bookingID += 1
        self.bookingId = BookingDetails.bookingID
        self.movie = movie
        self.seats = seats
        self.screening = screening
        


def save_data(filename, admin):
    with open(filename, 'w') as file:
        for movie in admin.moviesList:
            file.write(f"Movie: {movie.title}, Available Seats: {movie.available_seats}\n")
            for booking in movie.bookings:
                user = booking['user']
                booking_details = booking['booking']  
                file.write(f"Booking ID: {user.username}-{booking_details.bookingId}, Movie: {movie.title}, Seats: {booking['seats']}, Screening Time: {booking['screening']}\n")


def load_data(filename):
    admin = SystemAdministrator()
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('Movie:'):
                movie_info = line.strip().split(',')
                title = movie_info[0].split(':')[1].strip()
                available_seats = int(movie_info[1].split(':')[1].strip())
                movie = admin.movieList(title, available_seats)
            elif line.startswith('Booking ID:'):
                booking_info = line.strip().split(',')
                booking_id = booking_info[0].split(':')[1].strip().split('-')[1]
                movie_title = booking_info[1].split(':')[1].strip()
                seats = booking_info[2].split(':')[1].strip()
                screening = booking_info[3].split(':')[1].strip()
                movie = next((mov for mov in admin.moviesList if mov.title == movie_title), None)
                if movie:
                    username = booking_info[0].split(':')[1].strip().split('-')[0]
                    user = User(username)
                    booking = BookingDetails(movie, seats, screening)
                    booking.bookingId = booking_id  # Set the booking ID
                    movie.bookings.append({'user': user, 'booking': booking, 'seats': seats, 'screening': screening})
                    movie.available_seats -= len(seats)
    return admin




admin = SystemAdministrator()

movie1 = admin.movieList("Avengers 'Endgame'", 150)
movie2 = admin.movieList("Avengers 'Infinity War'", 200)
screen1 = admin.screen(1)
screen2 = admin.screen(2)
timeSlot1 = admin.timeSlot("02:00", "05:00", screen1, movie1)
timeSlot2 = admin.timeSlot("07:00", "10:00", screen2, movie2)


user = User("xyz")
selectedMovie = user.selectMovie(movie1)
selectedSeats = user.selectSeats(selectedMovie, ["FD1", "FT2", "FN3"])
reservation = user.reservation(selectedMovie, selectedSeats, "02:00")
if selectedMovie.Booking(user, selectedSeats):
    print("Booking successful!")
else:
    print("Booking failed! Not enough seats available.")

print("Booking ID:", reservation.bookingId)
print("Movie:", reservation.movie.title)
print("Seats:", reservation.seats)
print("Screening Time:", reservation.screening)


save_data('data.txt', admin)
loaded_admin = load_data('data.txt')
