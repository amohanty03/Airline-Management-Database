import csv
import random
from faker import Faker

fake = Faker()

# List of real US airports (code, name, state)
real_airports = [
    ("BHM", "Birmingham International Airport", "AL"), ("DHN", "Dothan Regional Airport", "AL"),
    ("HSV", "Huntsville International Airport", "AL"), ("MOB", "Mobile", "AL"), ("MGM", "Montgomery", "AL"),
    ("ANC", "Anchorage International Airport", "AK"), ("FAI", "Fairbanks International Airport", "AK"),
    ("JNU", "Juneau International Airport", "AK"), ("FLG", "Flagstaff", "AZ"), 
    ("PHX", "Phoenix Sky Harbor International Airport", "AZ"), ("TUS", "Tucson International Airport", "AZ"),
    ("YUM", "Yuma International Airport", "AZ"), ("FYV", "Fayetteville", "AR"), 
    ("LIT", "Little Rock National Airport", "AR"), ("XNA", "Northwest Arkansas Regional Airport", "AR"),
    ("BUR", "Burbank", "CA"), ("FAT", "Fresno", "CA"), ("LGB", "Long Beach", "CA"),
    ("LAX", "Los Angeles International Airport", "CA"), ("OAK", "Oakland", "CA"), ("ONT", "Ontario", "CA"),
    ("PSP", "Palm Springs", "CA"), ("SMF", "Sacramento", "CA"), ("SAN", "San Diego", "CA"),
    ("SFO", "San Francisco International Airport", "CA"), ("SJC", "San Jose", "CA"), ("SNA", "Santa Ana", "CA"),
    ("ASE", "Aspen", "CO"), ("COS", "Colorado Springs", "CO"), ("DEN", "Denver International Airport", "CO"),
    ("GJT", "Grand Junction", "CO"), ("PUB", "Pueblo", "CO"), ("BDL", "Hartford", "CT"),
    ("HVN", "Tweed New Haven", "CT"), ("IAD", "Washington Dulles International Airport", "DC"), 
    ("DCA", "Washington National Airport", "DC"), ("DAB", "Daytona Beach", "FL"),
    ("FLL", "Fort Lauderdale-Hollywood International Airport", "FL"), ("RSW", "Fort Meyers", "FL"),
    ("JAX", "Jacksonville", "FL"), ("EYW", "Key West International Airport", "FL"), 
    ("MIA", "Miami International Airport", "FL"), ("MCO", "Orlando", "FL"), ("PNS", "Pensacola", "FL"),
    ("PIE", "St. Petersburg", "FL"), ("SRQ", "Sarasota", "FL"), ("TPA", "Tampa", "FL"),
    ("PBI", "West Palm Beach", "FL"), ("PFN", "Panama City-Bay County International Airport", "FL"),
    ("ATL", "Atlanta Hartsfield International Airport", "GA"), ("AGS", "Augusta", "GA"),
    ("SAV", "Savannah", "GA"), ("ITO", "Hilo", "HI"), ("HNL", "Honolulu International Airport", "HI"),
    ("OGG", "Kahului", "HI"), ("KOA", "Kailua", "HI"), ("LIH", "Lihue", "HI"), ("BOI", "Boise", "ID"),
    ("MDW", "Chicago Midway Airport", "IL"), ("ORD", "Chicago O'Hare International Airport", "IL"),
    ("MLI", "Moline", "IL"), ("PIA", "Peoria", "IL"), ("EVV", "Evansville", "IN"), ("FWA", "Fort Wayne", "IN"),
    ("IND", "Indianapolis International Airport", "IN"), ("SBN", "South Bend", "IN"), ("CID", "Cedar Rapids", "IA"),
    ("DSM", "Des Moines", "IA"), ("ICT", "Wichita", "KS"), ("LEX", "Lexington", "KY"), 
    ("SDF", "Louisville", "KY"), ("BTR", "Baton Rouge", "LA"), ("MSY", "New Orleans International Airport", "LA"),
    ("SHV", "Shreveport", "LA"), ("AUG", "Augusta", "ME"), ("BGR", "Bangor", "ME"), ("PWM", "Portland", "ME"),
    ("BWI", "Baltimore", "MD"), ("BOS", "Boston Logan International Airport", "MA"), ("HYA", "Hyannis", "MA"),
    ("ACK", "Nantucket", "MA"), ("ORH", "Worcester", "MA"), ("BTL", "Battlecreek", "MI"), 
    ("DTW", "Detroit Metropolitan Airport", "MI"), ("DET", "Detroit", "MI"), ("FNT", "Flint", "MI"),
    ("GRR", "Grand Rapids", "MI"), ("AZO", "Kalamazoo-Battle Creek International Airport", "MI"),
    ("LAN", "Lansing", "MI"), ("MBS", "Saginaw", "MI"), ("DLH", "Duluth", "MN"), 
    ("MSP", "Minneapolis/St.Paul International Airport", "MN"), ("RST", "Rochester", "MN"), 
    ("GPT", "Gulfport", "MS"), ("JAN", "Jackson", "MS"), ("MCI", "Kansas City", "MO"),
    ("STL", "St Louis Lambert International Airport", "MO"), ("SGF", "Springfield", "MO"), ("BIL", "Billings", "MT"),
    ("LNK", "Lincoln", "NE"), ("OMA", "Omaha", "NE"), ("LAS", "Las Vegas McCarran International Airport", "NV"),
    ("RNO", "Reno-Tahoe International Airport", "NV"), ("MHT", "Manchester", "NH"),
    ("ACY", "Atlantic City International Airport", "NJ"), ("EWR", "Newark International Airport", "NJ"),
    ("TTN", "Trenton", "NJ"), ("ABQ", "Albuquerque International Airport", "NM"), ("ALM", "Alamogordo", "NM"),
    ("ALB", "Albany International Airport", "NY"), ("BUF", "Buffalo", "NY"), ("ISP", "Islip", "NY"),
    ("JFK", "John F Kennedy International Airport", "NY"), ("LGA", "La Guardia Airport", "NY"), 
    ("SWF", "Newburgh", "NY"), ("ROC", "Rochester", "NY"), ("SYR", "Syracuse", "NY"), 
    ("HPN", "Westchester", "NY"), ("AVL", "Asheville", "NC"), ("CLT", "Charlotte/Douglas International Airport", "NC"),
    ("FAY", "Fayetteville", "NC"), ("GSO", "Greensboro", "NC"), ("RDU", "Raleigh", "NC"),
    ("INT", "Winston-Salem", "NC"), ("BIS", "Bismark", "ND"), ("FAR", "Fargo", "ND"),
    ("CAK", "Akron", "OH"), ("CVG", "Cincinnati", "OH"), ("CLE", "Cleveland", "OH"), 
    ("CMH", "Columbus", "OH"), ("DAY", "Dayton", "OH"), ("TOL", "Toledo", "OH"), 
    ("OKC", "Oklahoma City", "OK"), ("TUL", "Tulsa", "OK"), ("EUG", "Eugene", "OR"),
    ("PDX", "Portland International Airport", "OR"), ("HIO", "Portland Hillsboro Airport", "OR"),
    ("SLE", "Salem", "OR"), ("ABE", "Allentown", "PA"), ("ERI", "Erie", "PA"), ("MDT", "Harrisburg", "PA"),
    ("PHL", "Philadelphia", "PA"), ("PIT", "Pittsburgh", "PA"), ("AVP", "Scranton", "PA"), 
    ("PVD", "Providence - T.F. Green Airport", "RI"), ("CHS", "Charleston", "SC"), ("CAE", "Columbia", "SC"),
    ("GSP", "Greenville", "SC"), ("MYR", "Myrtle Beach", "SC"), ("PIR", "Pierre", "SD"),
    ("RAP", "Rapid City", "SD"), ("FSD", "Sioux Falls", "SD"), ("TRI", "Bristol", "TN"),
    ("CHA", "Chattanooga", "TN"), ("TYS", "Knoxville", "TN"), ("MEM", "Memphis", "TN"),
    ("BNA", "Nashville", "TN"), ("AMA", "Amarillo", "TX"), ("AUS", "Austin Bergstrom International Airport", "TX"),
    ("CRP", "Corpus Christi", "TX"), ("DAL", "Dallas Love Field Airport", "TX"), 
    ("DFW", "Dallas/Fort Worth International Airport", "TX"), ("ELP", "El Paso", "TX"), 
    ("HOU", "Houston William B Hobby Airport", "TX"), ("IAH", "Houston George Bush Intercontinental Airport", "TX"),
    ("LBB", "Lubbock", "TX"), ("MAF", "Midland", "TX"), ("SAT", "San Antonio International Airport", "TX"),
    ("SLC", "Salt Lake City", "UT"), ("BTV", "Burlington", "VT"), ("MPV", "Montpelier", "VT"), 
    ("RUT", "Rutland", "VT"), ("PHF", "Newport News", "VA"), ("ORF", "Norfolk", "VA"), 
    ("RIC", "Richmond", "VA"), ("ROA", "Roanoke", "VA"), ("PSC", "Pasco/Tri-Cities Airport", "WA"),
    ("SEA", "Seattle Tacoma International Airport", "WA"), ("GEG", "Spokane International Airport", "WA"),
    ("CRW", "Charleston", "WV"), ("CKB", "Clarksburg", "WV"), ("HTS", "Huntington Tri-State Airport", "WV"),
    ("GRB", "Green Bay", "WI"), ("MSN", "Madison", "WI"), ("MKE", "Milwaukee", "WI"),
    ("CPR", "Casper", "WY"), ("CYS", "Cheyenne", "WY"), ("JAC", "Jackson Hole", "WY"), 
    ("RKS", "Rock Springs", "WY")
]

airports = [airport[0] for airport in real_airports]

with open('airport.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    for code, name, state in real_airports:
        writer.writerow([code, name, state, "USA"])

# Generate Aircraft Tail Numbers
aircrafts = []
existing_tail_numbers = set()
while len(aircrafts) < 150:
    tail = f"N{random.randint(100, 999)}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}"
    if tail not in existing_tail_numbers:
        existing_tail_numbers.add(tail)
        aircrafts.append(tail)
with open('aircraft.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    for tail in aircrafts:
        writer.writerow([tail, random.choice(['Boeing 737', 'Airbus A320', 'Boeing 777', 'Airbus A321', 'Airbus A319', 'Boeing 787', 'Airbus A350', 'Boeing 747', 
                                              'Boeing 787', 'Boeing 767', 'Embraer 190', 'Canadair CRJ900']), random.randint(150, 300)])

# Generate Passenger Information
passengers = [fake.unique.bothify(text='??#######').upper() for _ in range(3000)]
with open('passenger.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    for p in passengers:
        writer.writerow([p, fake.name(), fake.phone_number()[:20]])

# Generate Employees
employees = list(range(1, 201))
with open('employee.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    for e in employees:
        writer.writerow([e, fake.name(), random.choice(['Pilot', 'Flight Attendant', 'Ground Crew']), random.randint(50000, 150000)])

# Generate Real Airlines
real_airlines = [
    ("DL", "Delta Air Lines"), ("AA", "American Airlines"), 
    ("UA", "United Airlines"), ("WN", "Southwest Airlines"), 
    ("B6", "JetBlue Airways"), ("AS", "Alaska Airlines"), ("NK", "Spirit Airlines"), ("F9", "Frontier Airlines"),
    ("G4", "Allegiant Airlines"), ("SY", "Sun Country Airlines")
]
airline_codes = [a[0] for a in real_airlines]

with open('airline.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    for code, name in real_airlines:
        writer.writerow([code, name])

# Generate Flights 
flights = []
existing_flight_nums = set()

with open('flight.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    for _ in range(500):
        airline = random.choice(airline_codes)
        
        while True:
            f_num = f"{airline}{random.randint(1000, 9999)}"
            if f_num not in existing_flight_nums:
                existing_flight_nums.add(f_num)
                flights.append(f_num)
                break
                
        origin = random.choice(airports)
        dest = random.choice(airports)
        while dest == origin: 
            dest = random.choice(airports)
            
        writer.writerow([f_num, fake.date_time_this_year(), random.choice(['Scheduled', 'Delayed', 'On Time']), random.choice(aircrafts), origin, dest, airline])

# Generate Bookings
with open('booking.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    existing = set()
    for _ in range(5000):
        p = random.choice(passengers)
        fl = random.choice(flights)
        while (p, fl) in existing:
            p, fl = random.choice(passengers), random.choice(flights)
        existing.add((p, fl))
        writer.writerow([p, fl, f"{random.randint(1,30)}{random.choice(['A','B','C','D','E','F'])}"])

# Generate Staffing 
with open('staffing.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    existing_s = set()
    for _ in range(2000):
        e = random.choice(employees)
        fl = random.choice(flights)
        if (e, fl) not in existing_s:
            existing_s.add((e, fl))
            writer.writerow([e, fl])
