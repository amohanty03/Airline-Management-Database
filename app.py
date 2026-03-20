import streamlit as st
import pandas as pd
import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

def get_setting(secret_key, env_key, default=None):
    secret_value = st.secrets.get(secret_key)
    if secret_value is not None:
        return secret_value
    env_value = os.getenv(env_key)
    if env_value is not None:
        return env_value
    return default

@st.cache_resource
def connect_db():
    try:
        db_user = get_setting("PGUSER", "PGUSER")
        db_password = get_setting("PGPASSWORD", "PGPASSWORD")
        db_host = get_setting("PGHOST", "PGHOST")
        db_port = "5432"
        db_name = get_setting("PGDATABASE", "PGDATABASE")

        missing = [
            key for key, value in {
                "PGUSER": db_user, "PGPASSWORD": db_password, "PGHOST": db_host
            }.items() if not value
        ]
        
        if missing:
            st.error(f"Missing required database settings: {', '.join(missing)}")
            return None

        engine = create_engine(
            URL.create(
                "postgresql+psycopg2",
                username=db_user,
                password=db_password,
                host=db_host,
                port=int(db_port),
                database=db_name,
                query={"sslmode": "require"}
            )
        )
        return engine
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return None

engine = connect_db()
if engine is None:
    st.stop()

st.set_page_config(page_title="AM Airlines Management System", page_icon="✈️", layout="wide")
st.title("AM Airlines Management System")
st.markdown("Welcome to the Flight Management Dashboard.")


st.sidebar.header("Navigation Menu")
option = st.sidebar.radio(
    "Select an Operation:",
    ("1. View Flight Passenger Roster", 
     "2. Book a New Flight", 
     "3. Busiest Airports", 
     "4. Retrieve Flight Manifest", 
     "5. Airline Fleet Statistics",
     "6. Cancel a Booking")
)

def run_query(query, params=None):
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query), params or {})
            rows = result.fetchall()
            df = pd.DataFrame(rows, columns=result.keys())
        st.dataframe(df, width='stretch')
    except Exception as e:
        st.error(f"Query Error: {e}")

if option == "1. View Flight Passenger Roster":
    st.subheader("Flight Passenger Roster")
    
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT DISTINCT flightnum FROM flight ORDER BY flightnum"))
            flight_numbers = pd.DataFrame(result.fetchall(), columns=result.keys())
        
        flight_num = st.selectbox("Select Flight Number:", flight_numbers['flightnum'].tolist())
        if st.button("Search"):
            query = """
                SELECT p.Name AS "Passenger Name", p.Phone AS "Phone Number", b.SeatNum AS "Seat Number" 
                FROM Passenger p
                JOIN Booking b ON p.PassportNum = b.PassportNum
                WHERE b.FlightNum = :flight_num
                ORDER BY b.SeatNum;
            """
            run_query(query, {"flight_num": flight_num})
    except Exception as e:
        st.error(f"Error fetching flight numbers: {e}")

elif option == "2. Book a New Flight":
    st.subheader("Book a New Flight")
    st.markdown("Book a flight to your next destination now! Please fill in the details below. If you're a new passenger, make sure to provide your name and phone number as well.")
    
    with st.form("booking_form"):
        passport = st.text_input("Passenger Passport Number:").strip().upper()
        name = st.text_input("Passenger Name (Required for new passengers):").strip()
        phone = st.text_input("Passenger Phone (Required for new passengers):").strip()
        flight = st.text_input("Flight Number (e.g., DL1234):").strip().upper()
        seat = st.text_input("Seat Number (e.g., 12A):").strip().upper()
        submit = st.form_submit_button("Confirm Booking")

        if submit:
            if not passport or not flight or not seat:
                st.error("Passport, Flight, and Seat are strictly required.")
            else:
                try:
                    with engine.begin() as conn:
                        existing_passenger = conn.execute(
                            text("SELECT PassportNum FROM Passenger WHERE PassportNum = :passport"),
                            {"passport": passport},
                        ).fetchone()

                        if not existing_passenger:
                            if not name:
                                st.error("This is a new passport number! Please provide a Passenger Name to register them.")
                                st.stop()

                            conn.execute(
                                text("INSERT INTO Passenger (PassportNum, Name, Phone) VALUES (:passport, :name, :phone)"),
                                {"passport": passport, "name": name, "phone": phone},
                            )
                            st.info(f"Registered new passenger: {name}")

                        conn.execute(
                            text("INSERT INTO Booking (PassportNum, FlightNum, SeatNum) VALUES (:passport, :flight, :seat)"),
                            {"passport": passport, "flight": flight, "seat": seat},
                        )

                    st.success("✅ Booking successfully confirmed!")
                    
                except Exception as e:
                    st.error(f"❌ Booking failed. Error: {e}")

elif option == "3. Busiest Airports":
    st.subheader("Top Busiest Airports (By Passenger Traffic)")
    limit_num = st.number_input("How many top airports do you want to see?", min_value=1, max_value=50, value=5, step=1)
    if st.button("Load Statistics"):
        query = """
            SELECT a.IATACode as "Airport Code", 
                   a.City as "City",
                   a.State as "State", 
                   COUNT(b.PassportNum) as "Total Transiting Passengers"
            FROM Airport a
            JOIN Flight f ON a.IATACode = f.OriginCode OR a.IATACode = f.DestCode
            JOIN Booking b ON f.FlightNum = b.FlightNum
            GROUP BY a.IATACode, a.City, a.State
            ORDER BY "Total Transiting Passengers" DESC
            LIMIT """ + str(int(limit_num)) + """;
        """
        run_query(query)

elif option == "4. Retrieve Flight Manifest":
    st.subheader("Full Flight Manifest")
    
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT DISTINCT flightnum FROM flight ORDER BY flightnum"))
            flight_numbers = pd.DataFrame(result.fetchall(), columns=result.keys())
        
        
        flight_num = st.selectbox("Select Flight Number for Full Manifest:", flight_numbers['flightnum'].tolist())
        if st.button("Generate Manifest"):
            query = """
                SELECT p.Name as "Name", 'Passenger' as Role
                FROM Passenger p
                JOIN Booking b ON p.PassportNum = b.PassportNum
                WHERE b.FlightNum = :flight_num
                UNION
                SELECT e.Name as "Name", e.Role as "Role"
                FROM Employee e
                JOIN Staffing s ON e.EmployeeID = s.EmployeeID
                WHERE s.FlightNum = :flight_num
                ORDER BY Role;
            """
            run_query(query, {"flight_num": flight_num})
    except Exception as e:
        st.error(f"Error fetching flight numbers: {e}")

elif option == "5. Airline Fleet Statistics":
    st.subheader("Airline Fleet Statistics")
    if st.button("Load Fleet Data"):
        query = """
            SELECT al.Name as "Airline", 
                   COUNT(f.FlightNum) as "Total Flights",
                   ROUND((SELECT AVG(Capacity) FROM Aircraft ac JOIN Flight f2 ON ac.TailNum = f2.TailNum WHERE f2.AirlineCode = al.AirlineCode), 1) as "Avg Plane Capacity"
            FROM Airline al
            JOIN Flight f ON al.AirlineCode = f.AirlineCode
            GROUP BY al.Name, al.AirlineCode
            ORDER BY "Total Flights" DESC;
        """
        run_query(query)

elif option == "6. Cancel a Booking":
    st.subheader("Cancel a Booking")
    st.markdown("Enter the details of the booking you wish to remove.")
    
    with st.form("cancel_form"):
        passport = st.text_input("Passenger Passport Number:").strip().upper()
        flight = st.text_input("Flight Number (e.g., DL1234):").strip().upper()
        submit = st.form_submit_button("Cancel Booking")

        if submit:
            if not passport or not flight:
                st.error("Please fill in both fields.")
            else:
                try:
                    with engine.begin() as conn:
                        result = conn.execute(
                            text("DELETE FROM Booking WHERE PassportNum = :passport AND FlightNum = :flight"),
                            {"passport": passport, "flight": flight},
                        )

                    if result.rowcount and result.rowcount > 0:
                        st.success(f"✅ Booking for Passport {passport} on Flight {flight} has been successfully canceled!")
                    else:
                        st.warning("⚠️ No matching booking found. Please check the Passport and Flight numbers.")
                except Exception as e:
                    st.error(f"❌ Error canceling booking: {e}")