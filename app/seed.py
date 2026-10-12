
from datetime import datetime, timedelta

from app import create_app, db
from app.models import Destination, TourPackage, Hotel, Flight, Guide


app = create_app()


def seed_database():
    print("\nStarting TravelEase database seeding...")

    # -------------------------------------------------
    # 1. DESTINATIONS
    # -------------------------------------------------
    destinations_data = [
        {
            "name": "Goa Beach",
            "country": "India",
            "city": "Goa",
            "description": "Beautiful beaches, nightlife, water sports and Portuguese heritage.",
            "best_time": "November to February"
        },
        {
            "name": "Taj Mahal",
            "country": "India",
            "city": "Agra",
            "description": "Explore the iconic Taj Mahal and Mughal architecture.",
            "best_time": "October to March"
        },
        {
            "name": "Manali",
            "country": "India",
            "city": "Manali",
            "description": "Enjoy mountains, snow, adventure sports and scenic valleys.",
            "best_time": "October to June"
        },
        {
            "name": "Jaipur Heritage",
            "country": "India",
            "city": "Jaipur",
            "description": "Discover royal palaces, forts, markets and Rajasthani culture.",
            "best_time": "October to March"
        },
        {
            "name": "Kerala Backwaters",
            "country": "India",
            "city": "Alappuzha",
            "description": "Experience peaceful backwaters, houseboats and lush greenery.",
            "best_time": "September to March"
        }
    ]

    for item in destinations_data:
        destination = Destination.query.filter_by(
            name=item["name"],
            city=item["city"]
        ).first()

        if not destination:
            destination = Destination(**item)
            db.session.add(destination)
            print("Added destination:", item["name"])
        else:
            print("Destination already exists:", item["name"])

    db.session.flush()

    # -------------------------------------------------
    # 2. TOUR PACKAGES
    # -------------------------------------------------
    packages_data = [
        {
            "name": "Goa Beach Adventure",
            "destination": "Goa Beach",
            "duration_days": 4,
            "price": 8999,
            "max_people": 10,
            "description": "Four days of beach visits, sightseeing and water activities."
        },
        {
            "name": "Agra Heritage Tour",
            "destination": "Taj Mahal",
            "duration_days": 2,
            "price": 4999,
            "max_people": 15,
            "description": "Visit the Taj Mahal, Agra Fort and local heritage sites."
        },
        {
            "name": "Manali Mountain Escape",
            "destination": "Manali",
            "duration_days": 5,
            "price": 12999,
            "max_people": 12,
            "description": "Explore mountain scenery, valleys and adventure activities."
        },
        {
            "name": "Jaipur Royal Experience",
            "destination": "Jaipur Heritage",
            "duration_days": 3,
            "price": 7499,
            "max_people": 15,
            "description": "Explore forts, royal palaces and traditional markets."
        },
        {
            "name": "Kerala Houseboat Holiday",
            "destination": "Kerala Backwaters",
            "duration_days": 3,
            "price": 9999,
            "max_people": 8,
            "description": "Enjoy backwater cruises, local cuisine and peaceful scenery."
        }
    ]

    for item in packages_data:
        destination = Destination.query.filter_by(
            name=item["destination"]
        ).first()

        if not destination:
            print("Destination missing for package:", item["name"])
            continue

        package = TourPackage.query.filter_by(
            name=item["name"]
        ).first()

        if not package:
            package = TourPackage(
                name=item["name"],
                description=item["description"],
                destination_id=destination.id,
                duration_days=item["duration_days"],
                price=item["price"],
                max_people=item["max_people"],
                is_active=True
            )
            db.session.add(package)
            print("Added package:", item["name"])
        else:
            print("Package already exists:", item["name"])

    # -------------------------------------------------
    # 3. HOTELS
    # -------------------------------------------------
    hotels_data = [
        {
            "name": "Ocean Pearl Hotel",
            "city": "Goa",
            "country": "India",
            "star_rating": 4,
            "price_per_night": 3500
        },
        {
            "name": "Taj View Residency",
            "city": "Agra",
            "country": "India",
            "star_rating": 4,
            "price_per_night": 2800
        },
        {
            "name": "Mountain Breeze Resort",
            "city": "Manali",
            "country": "India",
            "star_rating": 5,
            "price_per_night": 4500
        },
        {
            "name": "Royal Pink City Hotel",
            "city": "Jaipur",
            "country": "India",
            "star_rating": 4,
            "price_per_night": 3200
        },
        {
            "name": "Backwater Comfort Stay",
            "city": "Alappuzha",
            "country": "India",
            "star_rating": 3,
            "price_per_night": 2200
        }
    ]

    for item in hotels_data:
        hotel = Hotel.query.filter_by(
            name=item["name"],
            city=item["city"]
        ).first()

        if not hotel:
            db.session.add(Hotel(**item))
            print("Added hotel:", item["name"])
        else:
            print("Hotel already exists:", item["name"])

    # -------------------------------------------------
    # 4. FLIGHTS
    # -------------------------------------------------
    now = datetime.now().replace(second=0, microsecond=0)
    tomorrow = now + timedelta(days=1)

    flights_data = [
        {
            "airline": "IndiGo",
            "flight_number": "6E101",
            "departure_city": "Hyderabad",
            "arrival_city": "Goa",
            "departure_time": tomorrow.replace(hour=8, minute=0),
            "arrival_time": tomorrow.replace(hour=9, minute=30),
            "price": 4500,
            "available_seats": 45
        },
        {
            "airline": "Air India",
            "flight_number": "AI202",
            "departure_city": "Hyderabad",
            "arrival_city": "Delhi",
            "departure_time": tomorrow.replace(hour=10, minute=0),
            "arrival_time": tomorrow.replace(hour=12, minute=30),
            "price": 6500,
            "available_seats": 40
        },
        {
            "airline": "IndiGo",
            "flight_number": "6E303",
            "departure_city": "Delhi",
            "arrival_city": "Jaipur",
            "departure_time": tomorrow.replace(hour=14, minute=0),
            "arrival_time": tomorrow.replace(hour=15, minute=0),
            "price": 3200,
            "available_seats": 35
        },
        {
            "airline": "Air India Express",
            "flight_number": "IX404",
            "departure_city": "Hyderabad",
            "arrival_city": "Kochi",
            "departure_time": tomorrow.replace(hour=16, minute=0),
            "arrival_time": tomorrow.replace(hour=17, minute=30),
            "price": 4000,
            "available_seats": 30
        },
        {
            "airline": "IndiGo",
            "flight_number": "6E505",
            "departure_city": "Delhi",
            "arrival_city": "Manali",
            "departure_time": tomorrow.replace(hour=7, minute=0),
            "arrival_time": tomorrow.replace(hour=8, minute=30),
            "price": 5000,
            "available_seats": 25
        }
    ]

    for item in flights_data:
        flight = Flight.query.filter_by(
            flight_number=item["flight_number"]
        ).first()

        if not flight:
            db.session.add(Flight(**item))
            print("Added flight:", item["flight_number"])
        else:
            print("Flight already exists:", item["flight_number"])

    # -------------------------------------------------
    # 5. TOUR GUIDES
    # -------------------------------------------------
    guides_data = [
        {
            "name": "Arjun Sharma",
            "city": "Goa",
            "country": "India",
            "languages": "English, Hindi, Konkani",
            "experience_years": 5,
            "phone": "9000000001"
        },
        {
            "name": "Priya Verma",
            "city": "Agra",
            "country": "India",
            "languages": "English, Hindi",
            "experience_years": 7,
            "phone": "9000000002"
        },
        {
            "name": "Rahul Thakur",
            "city": "Manali",
            "country": "India",
            "languages": "English, Hindi",
            "experience_years": 4,
            "phone": "9000000003"
        },
        {
            "name": "Meera Singh",
            "city": "Jaipur",
            "country": "India",
            "languages": "English, Hindi, French",
            "experience_years": 6,
            "phone": "9000000004"
        },
        {
            "name": "Anjali Nair",
            "city": "Alappuzha",
            "country": "India",
            "languages": "English, Hindi, Malayalam",
            "experience_years": 5,
            "phone": "9000000005"
        }
    ]

    for item in guides_data:
        guide = Guide.query.filter_by(
            name=item["name"],
            city=item["city"]
        ).first()

        if not guide:
            db.session.add(Guide(**item))
            print("Added guide:", item["name"])
        else:
            print("Guide already exists:", item["name"])

    # Save all changes together
    db.session.commit()

    print("\nTravelEase sample data added successfully!")
    print("Destinations:", Destination.query.count())
    print("Tour packages:", TourPackage.query.count())
    print("Hotels:", Hotel.query.count())
    print("Flights:", Flight.query.count())
    print("Guides:", Guide.query.count())


if __name__ == "__main__":
    with app.app_context():
        try:
            seed_database()
        except Exception as error:
            db.session.rollback()
            print("\nDatabase seeding failed.")
            print("Error:", error)
            raise

