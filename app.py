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
        db_user = get_setting("DB_USER", "DB_USER")
        db_password = get_setting("DB_PASSWORD", "DB_PASSWORD")
        db_host = get_setting("DB_HOST", "DB_HOST", "localhost")
        db_port = get_setting("DB_PORT", "DB_PORT", "5432")
        db_name = get_setting("DB_NAME", "DB_NAME", "postgres")

        missing = [
            key
            for key, value in {
                "DB_USER": db_user,
                "DB_PASSWORD": db_password,
            }.items()
            if not value
        ]
        if missing:
            st.error(f"Missing required database settings: {', '.join(missing)}")
            st.info("Set them in .streamlit/secrets.toml or as environment variables.")
            return None

        engine = create_engine(
            URL.create(
                "postgresql+psycopg2",
                username=db_user,
                password=db_password,
                host=db_host,
                port=int(db_port),
                database=db_name,
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
     "5. Airline Fleet Statistics",)
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
    with st.form("booking_form"):
        passport = st.text_input("Passenger Passport Number:").strip().upper()
        flight = st.text_input("Flight Number:").strip().upper()
        seat = st.text_input("Seat Number (e.g., 12A):").strip().upper()
        submit = st.form_submit_button("Confirm Booking")

        if submit:
            try:
                with engine.begin() as conn:
                    conn.execute(
                        text("INSERT INTO Booking (PassportNum, FlightNum, SeatNum) VALUES (:passport, :flight, :seat)"),
                        {"passport": passport, "flight": flight, "seat": seat},
                    )
                st.success("✅ Booking successfully confirmed!")
            except Exception as e:
                st.error(f"❌ Booking failed. Please ensure Passport and Flight exist. Error: {e}")

elif option == "3. Busiest Airports":
    st.subheader("📊 Top 5 Busiest Airports (By Passenger Traffic)")
    if st.button("Load Statistics"):
        query = """
            SELECT a.IATACode as "Airport Code", 
                   a.City, 
                   COUNT(b.PassportNum) as "Total Transiting Passengers"
            FROM Airport a
            JOIN Flight f ON a.IATACode = f.OriginCode OR a.IATACode = f.DestCode
            JOIN Booking b ON f.FlightNum = b.FlightNum
            GROUP BY a.IATACode, a.City
            ORDER BY "Total Transiting Passengers" DESC
            LIMIT 5;
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
                SELECT p.Name, 'Passenger' as Role
                FROM Passenger p
                JOIN Booking b ON p.PassportNum = b.PassportNum
                WHERE b.FlightNum = :flight_num
                UNION
                SELECT e.Name, e.Role
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