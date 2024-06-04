class SystemAdministrator:
    def __init__(self):
        self.movies_list = []
        self.screens = []
        self.timeslots = []

    def add_movie(self, title, available_seats):
        movie = Movie(title, available_seats)
        self.movies_list.append(movie)
        return movie

    def add_screen(self, screen_number):
        screen = Screen(screen_number)
        self.screens.append(screen)
        return screen

    def add_timeslot(self, starting, ending, screen, movie):
        timeslot = Timeslot(starting, ending, screen, movie)
        self.timeslots.append(timeslot)
        screen.add_timeslot(timeslot)
        return timeslot


class User:
    def __init__(self, username):
        self.username = username

    def select_movie(self, movie):
        return movie

    def select_seats(self, movie, seats):
        return seats

    def make_reservation(self, movie, seats, timeslot):
        return BookingDetails(movie, seats, timeslot)


class Movie:
    def __init__(self, title, available_seats):
        self.title = title
        self.available_seats = available_seats
        self.bookings = []

    def book(self, user, seats):
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

    def __init__(self, movie, seats, timeslot):
        BookingDetails.bookingID += 1
        self.bookingId = BookingDetails.bookingID
        self.movie = movie
        self.seats = seats
        self.timeslot = timeslot


def save_data(filename, admin):
    with open(filename, 'w') as file:
        for movie in admin.movies_list:
            file.write(f"Movie: {movie.title}, Available Seats: {movie.available_seats}\n")
            for booking in movie.bookings:
                user = booking['user']
                seats = ', '.join(booking['seats'])
                file.write(f"Booking ID: {user.username}-{BookingDetails.bookingID}, Movie: {movie.title}, Seats: {seats}\n")


def load_data(filename):
    admin = SystemAdministrator()
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('Movie:'):
                movie_info = line.strip().split(',')
                title = movie_info[0].split(':')[1].strip()
                available_seats = int(movie_info[1].split(':')[1].strip())
                admin.add_movie(title, available_seats)
            elif line.startswith('Booking ID:'):
                booking_info = line.strip().split(',')
                username = booking_info[0].split(':')[1].strip().split('-')[0]
                movie_title = booking_info[1].split(':')[1].strip()
                seats = booking_info[2].split(':')[1].strip().split(', ')
                movie = next((m for m in admin.movies_list if m.title == movie_title), None)
                if movie:
                    user = User(username)
                    movie.book(user, seats)
    return admin



admin = SystemAdministrator()

movie1 = admin.add_movie("Avengers 'Endgame'", 150)
movie2 = admin.add_movie("Avengers 'Infinity War'", 200)
screen1 = admin.add_screen(1)
screen2 = admin.add_screen(2)
timeSlot1 = admin.add_timeslot("02:00", "05:00", screen1, movie1)
timeSlot2 = admin.add_timeslot("07:00", "10:00", screen2, movie2)

user = User("xyz")
selectedMovie = user.select_movie(movie1)
selectedSeats = user.select_seats(selectedMovie, ["FD1", "FT2", "FN3"])
reservation = user.make_reservation(selectedMovie, selectedSeats, timeSlot1)
if selectedMovie.book(user, selectedSeats):
    print("Booking successful!")
else:
    print("Booking failed! Not enough seats available.")

print("Booking ID:", reservation.bookingId)
print("Movie:", reservation.movie.title)
print("Seats:", reservation.seats)
print("Screening Time:", reservation.timeslot.starting)

save_data('data.txt', admin)
loaded_admin = load_data('data.txt')
