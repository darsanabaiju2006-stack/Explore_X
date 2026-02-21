import sqlite3
import hashlib

DB = 'explorex.db'

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_database():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    # ─── TABLES ───────────────────────────────────────────────
    c.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS destinations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            place_name TEXT NOT NULL,
            description TEXT,
            image TEXT,
            category TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS packages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            destination_id INTEGER NOT NULL,
            package_name TEXT NOT NULL,
            price REAL NOT NULL,
            duration_days INTEGER NOT NULL,
            details TEXT,
            includes TEXT,
            FOREIGN KEY (destination_id) REFERENCES destinations(id)
        );

        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            package_id INTEGER NOT NULL,
            booking_date TEXT NOT NULL,
            number_of_people INTEGER DEFAULT 1,
            total_amount REAL NOT NULL,
            status TEXT DEFAULT 'Confirmed',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (package_id) REFERENCES packages(id)
        );
    """)

    # ─── SEED USERS ───────────────────────────────────────────
    c.execute("SELECT COUNT(*) FROM users")
    if c.fetchone()[0] == 0:
        c.executemany("INSERT INTO users (name,email,password,role) VALUES (?,?,?,?)", [
            ('Admin',      'admin@explorex.com', hash_password('admin123'), 'admin'),
            ('Arun Kumar', 'arun@gmail.com',     hash_password('user123'),  'user'),
        ])

    # ─── SEED DESTINATIONS ────────────────────────────────────
    c.execute("SELECT COUNT(*) FROM destinations")
    if c.fetchone()[0] == 0:
        destinations = [
            ('Munnar',            'Emerald tea plantations, mist-covered peaks and cool mountain air — Kerala most beloved hill retreat.',              'https://images.unsplash.com/photo-1585938389612-a552a28d6914?w=600&q=80', 'Hill Station'),
            ('Alleppey',          'Float through serene backwaters in a traditional houseboat surrounded by coconut groves and village life.',          'https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?w=600&q=80', 'Backwaters'),
            ('Wayanad',           'Dense forests, ancient caves, roaring waterfalls and wildlife sanctuaries — Kerala green treasure chest.',           'https://images.unsplash.com/photo-1607427293702-036933bbf746?w=600&q=80', 'Wildlife'),
            ('Thekkady',          'Home to Periyar Tiger Reserve, spice gardens and boat safaris on the Periyar Lake — a true wilderness experience.', 'https://images.unsplash.com/photo-1596895111956-bf1cf0599ce5?w=600&q=80', 'Wildlife'),
            ('Kovalam',           'Crescent beaches, Ayurvedic wellness retreats and lighthouse views — Kerala premier beach destination.',              'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=600&q=80', 'Beach'),
            ('Fort Kochi',        'Portuguese, Dutch and British heritage — Chinese fishing nets, spice markets and vibrant street art.',               'https://images.unsplash.com/photo-1567157577867-05ccb1388e66?w=600&q=80', 'Heritage'),
            ('Goa',               'Sun-soaked beaches, vibrant nightlife, Portuguese heritage and fresh seafood along the Arabian Sea coast.',          'https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=600&q=80', 'Beach'),
            ('Ooty',              'The Queen of Hill Stations — rolling grasslands, blue gum forests, tea gardens and cool misty mornings.',           'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600&q=80', 'Hill Station'),
        ]
        c.executemany("INSERT INTO destinations (place_name,description,image,category) VALUES (?,?,?,?)", destinations)

    # ─── SEED PACKAGES ────────────────────────────────────────
    c.execute("SELECT COUNT(*) FROM packages")
    if c.fetchone()[0] == 0:
        packages = [
            (1, 'Munnar Weekend',       4999,  3, 'Tea estates, Eravikulam Park and Echo Point.',                'Hotel, Breakfast, Tea Estate Tour, Transfer'),
            (1, 'Munnar Explorer',      7999,  5, 'Complete Munnar with Mattupetty Dam and trekking.',           'Resort, All Meals, 4 Tours, Trekking, Transfer'),
            (1, 'Munnar Luxury',        14999, 7, 'Private villa with jeep safari and plantation experience.',   'Luxury Resort, All Meals, Private Guide, Jeep Safari, Transfer'),
            (2, 'Backwater Bliss',      5499,  2, 'Overnight houseboat cruise on Alleppey backwaters.',          'Houseboat, All Meals, Sunset Cruise'),
            (2, 'Alleppey Classic',     9999,  4, 'Houseboat plus kayaking and village walks.',                  'Houseboat + Hotel, All Meals, Kayaking, Village Walk, Transfer'),
            (3, 'Wayanad Quick',        4499,  3, 'Edakkal Caves, Pookode Lake and Soochipara Waterfalls.',      'Homestay, Breakfast, Cave Visit, Lake Tour, Transfer'),
            (3, 'Wayanad Wild',         8499,  5, 'Jungle resort with safari and bamboo rafting.',               'Jungle Resort, All Meals, Safari, Waterfall Trek, Rafting, Transfer'),
            (4, 'Spice Trail',          5299,  3, 'Spice garden tour and Periyar boat safari.',                  'Hotel, Breakfast, Spice Garden, Boat Safari, Transfer'),
            (4, 'Periyar Explorer',     9499,  5, 'Full wildlife experience with night patrol.',                 'Jungle Lodge, All Meals, Boat Safari, Elephant Walk, Night Patrol, Transfer'),
            (5, 'Kovalam Escape',       5999,  3, 'Beach and Ayurvedic massage with lighthouse visit.',          'Beach Hotel, Breakfast, Ayurvedic Massage, Lighthouse, Transfer'),
            (5, 'Kovalam Wellness',     12999, 6, 'Complete Ayurveda and yoga retreat by the beach.',            'Beach Resort, All Meals, Daily Ayurveda, Yoga, Kathakali, Transfer'),
            (6, 'Kochi Heritage Walk',  3499,  2, 'Walking tour of Fort Kochi with Kathakali show.',             'Heritage Hotel, Breakfast, Walking Tour, Kathakali Show, Transfer'),
            (6, 'Fort Kochi Classic',   7499,  4, 'Jewish Synagogue, Mattancherry and sunset cruise.',           'Boutique Hotel, Breakfast, Heritage Sites, Sunset Cruise, Transfer'),
            (7, 'Goa Express',          6999,  4, 'North and South Goa beaches with water sports.',              'Hotel, Breakfast, Beach Tours, Water Sports, Transfer'),
            (7, 'Goa Premium',          12999, 7, 'Full Goa with heritage tours and luxury stay.',               'Luxury Hotel, All Meals, Heritage Tour, Water Sports, Cruise, Transfer'),
            (8, 'Ooty Getaway',         5299,  3, 'Toy train, Botanical Gardens and Doddabetta Peak.',           'Hotel, Breakfast, Toy Train, Garden Visit, Transfer'),
            (8, 'Ooty Complete',        8999,  5, 'Full Nilgiris with tea factory and trekking.',                'Resort, All Meals, Toy Train, Tea Factory, Trekking, Transfer'),
        ]
        c.executemany("INSERT INTO packages (destination_id,package_name,price,duration_days,details,includes) VALUES (?,?,?,?,?,?)", packages)

    conn.commit()
    conn.close()
    print("✅ Database created successfully!")
    print("─────────────────────────────────")
    print("👤 User  : arun@gmail.com  / user123")
    print("⚙️  Admin : admin@explorex.com / admin123")
    print("─────────────────────────────────")

if __name__ == '__main__':
    create_database()
