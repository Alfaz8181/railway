from flask import Flask, render_template, request

app = Flask(__name__)


class Train:
    def __init__(self, number, name, origin, destination, capacity):
        self.number, self.name, self.origin, self.destination = number, name, origin, destination
        self.capacity, self.available = capacity, capacity
        self.booked = {}

    def details(self):
        return f"Train {self.number} - {self.name}\nRoute: {self.origin} -> {self.destination}\nSeats: {self.capacity}, Available: {self.available}\n"

    def book(self, seat, passenger):
        if self.available > 0 and seat not in self.booked:
            self.booked[seat] = passenger
            self.available -= 1
            return True
        return False

    def cancel(self, seat):
        if seat in self.booked:
            del self.booked[seat]
            self.available += 1
            return True
        return False


class ReservationSystem:
    def __init__(self):
        self.trains = {}

    def add_train(self, num, name, origin, dest, cap):
        self.trains[num] = Train(num, name, origin, dest, cap)

    def show_trains(self):
        if not self.trains:
            return "No trains available."
        return "\n".join([t.details() for t in self.trains.values()])



rs = ReservationSystem()
rs.add_train("101", "Express", "CityA", "CityB", 3)
rs.add_train("102", "Superfast", "TownX", "TownY", 2)



@app.route("/", methods=["GET", "POST"])
def home():
    message = ""

    if request.method == "POST":
        action = request.form.get("action")
        train_no = request.form.get("train_no")

        if train_no in rs.trains:
            train = rs.trains[train_no]

            if action == "book":
                seat = int(request.form.get("seat"))
                name = request.form.get("name")
                if train.book(seat, name):
                    message = f" Seat {seat} booked for {name} on Train {train_no}"
                else:
                    message = "❌ Booking failed (seat taken or full)."

            elif action == "cancel":
                seat = int(request.form.get("seat"))
                if train.cancel(seat):
                    message = f" Seat {seat} cancelled on Train {train_no}"
                else:
                    message = " Cancellation failed (seat not found)."
        else:
            message = "Train not found."

   
    output = rs.show_trains()

    return render_template("indexx.html", output=output, message=message)


if __name__ == "__main__":
    app.run(debug=True)
