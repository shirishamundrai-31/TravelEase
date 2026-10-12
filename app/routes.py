
from datetime import date
from app.models import Wishlist


from flask import (

    Blueprint,

    render_template,

    request,

    redirect,

    url_for,

    flash,

)

from flask_login import (

    current_user,

    login_user,

    logout_user,

    login_required,

)



from app import db, bcrypt

from app.models import (

    User,

    Destination,

    TourPackage,

    Booking,

    Hotel,

    Flight,

    Itinerary,

    Guide,

)





main = Blueprint("main", __name__)





# =====================================================

# 1. HOME PAGE

# =====================================================



@main.route("/")

def home():

    destinations = Destination.query.all()



    packages = TourPackage.query.filter_by(

        is_active=True

    ).limit(6).all()



    return render_template(

        "index.html",

        destinations=destinations,

        packages=packages,

    )





# =====================================================

# 2. DESTINATIONS PAGE

# =====================================================






@main.route("/destinations")
def destinations():
    search_query = request.args.get("q", "").strip()
    query = Destination.query

    if search_query:
        query = query.filter(
            db.or_(
                Destination.name.ilike(f"%{search_query}%"),
                Destination.city.ilike(f"%{search_query}%"),
                Destination.country.ilike(f"%{search_query}%")
            )
        )

    destinations_list = query.order_by(Destination.name).all()

    return render_template(
        "destinations.html",
        destinations=destinations_list
    )






# =====================================================

# 3. TOUR PACKAGES PAGE WITH SEARCH

# =====================================================






@main.route("/packages")
def packages():
    search_query = request.args.get("q", "").strip()
    max_price_text = request.args.get("max_price", "").strip()
    duration_text = request.args.get("duration", "").strip()
    sort_by = request.args.get("sort", "price_low")

    query = TourPackage.query.filter_by(is_active=True)

    if search_query:
        query = query.join(
            Destination,
            TourPackage.destination_id == Destination.id
        ).filter(
            db.or_(
                TourPackage.name.ilike(f"%{search_query}%"),
                TourPackage.description.ilike(f"%{search_query}%"),
                Destination.name.ilike(f"%{search_query}%"),
                Destination.city.ilike(f"%{search_query}%"),
                Destination.country.ilike(f"%{search_query}%")
            )
        )

    if max_price_text:
        try:
            max_price = float(max_price_text)
            if max_price >= 0:
                query = query.filter(TourPackage.price <= max_price)
            else:
                flash("Maximum price cannot be negative.", "warning")
        except ValueError:
            flash("Please enter a valid maximum price.", "warning")

    if duration_text:
        try:
            duration = int(duration_text)
            if duration > 0:
                query = query.filter(
                    TourPackage.duration_days <= duration
                )
        except ValueError:
            flash("Please select a valid trip duration.", "warning")

    if sort_by == "price_high":
        query = query.order_by(TourPackage.price.desc())
    elif sort_by == "name":
        query = query.order_by(TourPackage.name.asc())
    else:
        sort_by = "price_low"
        query = query.order_by(TourPackage.price.asc())

    package_list = query.all()

    return render_template(
        "packages.html",
        packages=package_list
    )






# =====================================================

# 4. PACKAGE DETAILS

# =====================================================



@main.route("/packages/<int:package_id>")

def package_detail(package_id):

    package = db.get_or_404(TourPackage, package_id)



    if not package.is_active:

        flash("This package is currently unavailable.", "warning")

        return redirect(url_for("main.packages"))



    return render_template(

        "package_detail.html",

        package=package,

    )





# =====================================================

# 5. USER REGISTRATION

# =====================================================



@main.route("/register", methods=["GET", "POST"])

def register():

    if current_user.is_authenticated:

        return redirect(url_for("main.dashboard"))



    if request.method == "POST":

        username = request.form.get("username", "").strip()

        email = request.form.get("email", "").strip().lower()

        password = request.form.get("password", "")



        if not username or not email or not password:

            flash("Please fill in all required fields.", "danger")



        elif len(password) < 8:

            flash("Password must contain at least 8 characters.", "danger")



        elif User.query.filter_by(username=username).first():

            flash("That username is already registered.", "danger")



        elif User.query.filter_by(email=email).first():

            flash("That email address is already registered.", "danger")



        else:

            password_hash = bcrypt.generate_password_hash(

                password

            ).decode("utf-8")



            user = User(

                username=username,

                email=email,

                password_hash=password_hash,

            )



            db.session.add(user)

            db.session.commit()



            flash("Registration successful! Please log in.", "success")

            return redirect(url_for("main.login"))



    return render_template("auth.html", mode="register")





# =====================================================

# 6. USER LOGIN

# =====================================================



@main.route("/login", methods=["GET", "POST"])

def login():

    if current_user.is_authenticated:

        return redirect(url_for("main.dashboard"))



    if request.method == "POST":

        identity = request.form.get(

            "identity",

            request.form.get("email", request.form.get("username", "")),

        ).strip()



        password = request.form.get("password", "")



        user = User.query.filter(

            db.or_(

                User.email == identity.lower(),

                User.username == identity,

            )

        ).first()



        if user and bcrypt.check_password_hash(

            user.password_hash, password

        ):

            login_user(user)



            flash("Welcome back to TravelEase!", "success")



            next_page = request.args.get("next")



            # Only allow local application paths.

            if next_page and next_page.startswith("/") and not next_page.startswith("//"):

                return redirect(next_page)



            return redirect(url_for("main.dashboard"))



        flash("Invalid username/email or password.", "danger")



    return render_template("auth.html", mode="login")





# =====================================================

# 7. USER LOGOUT

# =====================================================



@main.route("/logout", methods=["POST"])

@login_required

def logout():

    logout_user()

    flash("You have been logged out.", "info")

    return redirect(url_for("main.home"))





# =====================================================

# 8. BOOK A TOUR PACKAGE

# =====================================================



@main.route(

    "/book/package/<int:package_id>",

    methods=["POST"],

)

@login_required

def book_package(package_id):

    package = db.get_or_404(TourPackage, package_id)



    if not package.is_active:

        flash("This package is currently unavailable.", "warning")

        return redirect(url_for("main.packages"))



    travel_date_text = request.form.get("travel_date", "").strip()

    people_text = request.form.get("people", "1").strip()



    try:

        travel_date = date.fromisoformat(travel_date_text)

        people = int(people_text)



        if travel_date < date.today():

            flash("Travel date cannot be in the past.", "danger")

            return redirect(

                url_for("main.package_detail", package_id=package.id)

            )



        if people < 1 or people > package.max_people:

            flash(

                f"Choose between 1 and {package.max_people} travellers.",

                "danger",

            )

            return redirect(

                url_for("main.package_detail", package_id=package.id)

            )



        booking = Booking(

            user_id=current_user.id,

            package_id=package.id,

            booking_type="package",

            travel_date=travel_date,

            people=people,

            total_price=float(package.price) * people,

            status="Pending",

            payment_status="Unpaid",

        )



        db.session.add(booking)

        db.session.commit()



        flash("Your tour booking has been created!", "success")

        return redirect(url_for("main.bookings"))



    except (ValueError, TypeError):

        flash("Please enter a valid travel date and number of travellers.", "danger")

        return redirect(

            url_for("main.package_detail", package_id=package.id)

        )





# =====================================================

# 9. MY BOOKINGS

# =====================================================



@main.route("/bookings")

@login_required

def bookings():

    bookings = Booking.query.filter_by(

        user_id=current_user.id

    ).order_by(Booking.id.desc()).all()



    return render_template(

        "bookings.html",

        bookings=bookings,

    )





# =====================================================

# 10. HOTELS PAGE

# =====================================================



@main.route("/hotels")

def hotels():

    hotels = Hotel.query.order_by(

        Hotel.city,

        Hotel.name,

    ).all()



    return render_template(

        "hotels.html",

        hotels=hotels,

    )





# =====================================================

# 11. FLIGHTS PAGE

# =====================================================



@main.route("/flights")

def flights():

    flights = Flight.query.order_by(

        Flight.departure_time

    ).all()



    return render_template(

        "flights.html",

        flights=flights,

    )





# =====================================================

# 12. TOUR GUIDES PAGE

# =====================================================



@main.route("/guides")

def guides():

    guides = Guide.query.order_by(

        Guide.city,

        Guide.name,

    ).all()



    return render_template(

        "guides.html",

        guides=guides,

    )





# =====================================================

# 13. MY ITINERARIES

# =====================================================



@main.route("/itineraries")

@login_required

def itineraries():

    itineraries = Itinerary.query.filter_by(

        user_id=current_user.id

    ).order_by(Itinerary.id.desc()).all()



    return render_template(

        "itineraries.html",

        itineraries=itineraries,

    )





# =====================================================

# 14. CREATE AN ITINERARY

# =====================================================



# CREATE ITINERARY

@main.route("/itineraries/create", methods=["GET", "POST"])

@login_required

def create_itinerary():

    if request.method == "POST":

        name = request.form.get("name", "").strip()

        destination = request.form.get("destination", "").strip()

        start_date_text = request.form.get("start_date", "").strip()

        end_date_text = request.form.get("end_date", "").strip()

        notes = request.form.get("notes", "").strip()



        if not name or not destination or not start_date_text or not end_date_text:

            flash("Please fill in all required fields.", "danger")

            return render_template("create_itinerary.html")



        try:

            start_date = date.fromisoformat(start_date_text)

            end_date = date.fromisoformat(end_date_text)



            if end_date < start_date:

                flash("End date cannot be before start date.", "danger")

                return render_template("create_itinerary.html")



            itinerary = Itinerary(

                user_id=current_user.id,

                name=name,

                destination=destination,

                start_date=start_date,

                end_date=end_date,

                notes=notes,

            )



            db.session.add(itinerary)

            db.session.commit()



            flash("Itinerary created successfully!", "success")

            return redirect(url_for("main.itineraries"))



        except ValueError:

            flash("Please enter valid travel dates.", "danger")



    return render_template("create_itinerary.html")





# EDIT ITINERARY

@main.route("/itineraries/<int:itinerary_id>/edit", methods=["GET", "POST"])

@login_required

def edit_itinerary(itinerary_id):

    itinerary = db.get_or_404(Itinerary, itinerary_id)



    # Users can only edit their own itineraries.

    if itinerary.user_id != current_user.id:

        flash("You cannot edit someone else's itinerary.", "danger")

        return redirect(url_for("main.itineraries"))



    if request.method == "POST":

        name = request.form.get("name", "").strip()

        destination = request.form.get("destination", "").strip()

        start_date_text = request.form.get("start_date", "").strip()

        end_date_text = request.form.get("end_date", "").strip()

        notes = request.form.get("notes", "").strip()



        if not name or not destination or not start_date_text or not end_date_text:

            flash("Please fill in all required fields.", "danger")

            return render_template(

                "edit_itinerary.html", itinerary=itinerary

            )



        try:

            start_date = date.fromisoformat(start_date_text)

            end_date = date.fromisoformat(end_date_text)



            if end_date < start_date:

                flash("End date cannot be before start date.", "danger")

                return render_template(

                    "edit_itinerary.html", itinerary=itinerary

                )



            itinerary.name = name

            itinerary.destination = destination

            itinerary.start_date = start_date

            itinerary.end_date = end_date

            itinerary.notes = notes



            db.session.commit()



            flash("Itinerary updated successfully!", "success")

            return redirect(url_for("main.itineraries"))



        except ValueError:

            flash("Please enter valid travel dates.", "danger")



    return render_template(

        "edit_itinerary.html", itinerary=itinerary

    )





# DELETE ITINERARY

@main.route("/itineraries/<int:itinerary_id>/delete", methods=["POST"])

@login_required

def delete_itinerary(itinerary_id):

    itinerary = db.get_or_404(Itinerary, itinerary_id)



    # Users can only delete their own itineraries.

    if itinerary.user_id != current_user.id:

        flash("You cannot delete someone else's itinerary.", "danger")

        return redirect(url_for("main.itineraries"))



    db.session.delete(itinerary)

    db.session.commit()



    flash("Itinerary deleted successfully.", "success")

    return redirect(url_for("main.itineraries"))
    # DASHBOARD
@main.route("/dashboard")
@login_required
def dashboard():
    booking_count = Booking.query.filter_by(
        user_id=current_user.id
    ).count()

    itinerary_count = Itinerary.query.filter_by(
        user_id=current_user.id
    ).count()

    destination_count = Destination.query.count()

    recent_bookings = Booking.query.filter_by(
        user_id=current_user.id
    ).order_by(Booking.id.desc()).limit(5).all()

    return render_template(
        "dashboard.html",
        booking_count=booking_count,
        itinerary_count=itinerary_count,
        destination_count=destination_count,
        recent_bookings=recent_bookings
    )
    
# ==========================================
# ADD PACKAGE TO WISHLIST
# ==========================================

@main.route("/wishlist/add/<int:package_id>", methods=["POST"])
@login_required
def add_to_wishlist(package_id):
    package = db.get_or_404(TourPackage, package_id)

    if not package.is_active:
        flash("This package is currently unavailable.", "warning")
        return redirect(url_for("main.packages"))

    existing = Wishlist.query.filter_by(
        user_id=current_user.id,
        package_id=package.id
    ).first()

    if existing:
        flash("This package is already in your wishlist.", "info")
    else:
        item = Wishlist(
            user_id=current_user.id,
            package_id=package.id
        )
        db.session.add(item)
        db.session.commit()
        flash("Package added to your wishlist!", "success")

    return redirect(
        request.referrer or url_for("main.packages")
    )


# ==========================================
# MY WISHLIST
# ==========================================

@main.route("/wishlist")
@login_required
def wishlist():
    items = Wishlist.query.filter_by(
        user_id=current_user.id
    ).order_by(Wishlist.id.desc()).all()

    return render_template("wishlist.html", items=items)


# ==========================================
# REMOVE FROM WISHLIST
# ==========================================

@main.route("/wishlist/remove/<int:wishlist_id>", methods=["POST"])
@login_required
def remove_from_wishlist(wishlist_id):
    item = db.get_or_404(Wishlist, wishlist_id)

    if item.user_id != current_user.id:
        flash("You cannot remove another user's wishlist item.", "danger")
        return redirect(url_for("main.wishlist"))

    db.session.delete(item)
    db.session.commit()

    flash("Package removed from your wishlist.", "success")
    return redirect(url_for("main.wishlist"))

@main.route("/bookings/cancel/<int:booking_id>", methods=["POST"])
@login_required
def cancel_booking(booking_id):
    booking = db.get_or_404(Booking, booking_id)

    # Users can cancel only their own bookings.
    if booking.user_id != current_user.id:
        flash("You cannot cancel another user's booking.", "danger")
        return redirect(url_for("main.bookings"))

    # Prevent cancelling an already cancelled booking.
    if booking.status == "cancelled":
        flash("This booking is already cancelled.", "info")
        return redirect(url_for("main.bookings"))

    booking.status = "cancelled"
    db.session.commit()

    flash("Your booking has been cancelled successfully.", "success")
    return redirect(url_for("main.bookings"))

