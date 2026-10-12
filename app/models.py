
from datetime import datetime
from flask_login import UserMixin
from app import db




class Guide(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    languages = db.Column(db.String(200))
    experience_years = db.Column(db.Integer, default=0)
    phone = db.Column(db.String(30))
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    bookings = db.relationship("Booking", backref="customer")
    itineraries = db.relationship("Itinerary", backref="owner")


class Destination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    best_time = db.Column(db.String(100))


class TourPackage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    destination_id = db.Column(
        db.Integer, db.ForeignKey("destination.id"),
        nullable=False
    )
    duration_days = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    max_people = db.Column(db.Integer, default=10)
    is_active = db.Column(db.Boolean, default=True)

    destination = db.relationship("Destination", backref="packages")


class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    star_rating = db.Column(db.Integer, default=3)
    price_per_night = db.Column(db.Numeric(10, 2), nullable=False)


class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    airline = db.Column(db.String(100), nullable=False)
    flight_number = db.Column(db.String(20), nullable=False)
    departure_city = db.Column(db.String(100), nullable=False)
    arrival_city = db.Column(db.String(100), nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    available_seats = db.Column(db.Integer, default=50)


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False
    )
    package_id = db.Column(
        db.Integer, db.ForeignKey("tour_package.id")
    )
    booking_type = db.Column(db.String(20), default="package")
    travel_date = db.Column(db.Date, nullable=False)
    people = db.Column(db.Integer, default=1)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20), default="pending")
    payment_status = db.Column(db.String(20), default="unpaid")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    package = db.relationship("TourPackage", backref="bookings")


class Itinerary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False
    )
    name = db.Column(db.String(200), nullable=False)
    destination = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.Text)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False
    )
    package_id = db.Column(
        db.Integer, db.ForeignKey("tour_package.id"), nullable=False
    )
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Wishlist(db.Model):
    __tablename__ = "wishlists"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    package_id = db.Column(
        db.Integer,
        db.ForeignKey("tour_package.id"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp()
    )

    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "package_id",
            name="unique_user_wishlist_package"
        ),
    )

    package = db.relationship("TourPackage")
    user = db.relationship("User")

    def __repr__(self):
        return f"<Wishlist user={self.user_id} package={self.package_id}>"
