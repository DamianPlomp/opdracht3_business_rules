import psycopg2
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

#connectie met postgreSQL
con = psycopg2.connect(
    host='localhost',
    database='opdracht3_sp',
    user='postgres',
    password='1234'
)

con.autocommit = True
cur = con.cursor()

#connectie met mongoDB
client = MongoClient('mongodb://localhost:27017')
db = client.get_database('huwebshop')


#haalt lijst van alle profiles op uit mongoDB
profiles = [profile for profile in client.huwebshop.profiles.find()]

#haalt lijst van alle sessions op uit mongoDB
sessions = [session for session in client.huwebshop.sessions.find()]

#haalt lijst van alle producten op uit mongoDB
products = [product for product in client.huwebshop.products.find_one()]


def profile_to_db():
    print("Initiate the function")
    for profile in profiles:
        if '_id' in profile:
            profile_id = str(profile['_id'])
            viewed_before = None
            if 'recommendations' in profile and 'viewed_before' in profile['recommendations'] and \
                    len(profile['recommendations']['viewed_before']) > 0:
                viewed_before = profile['recommendations']['viewed_before'][0]
            query = 'INSERT INTO profile (profile_id, viewed_before) VALUES (%s, %s)'
            insertion_data = (profile_id, viewed_before)
            try:
                cur.execute(query, insertion_data)
            except psycopg2.errors.UniqueViolation:
                # If inserting this row would result in a duplicate key error, skip it
                print(f"Skipping duplicate row with profile_id={profile_id}")
    print("It's done")


def session_to_db():
    for session in sessions:
        if '_id' in session and 'buid' in session:
            session_id = session['_id']
            buid_ids = session['buid']

            # Iterate over all buid_id values
            for buid_id in buid_ids:
                # If buid_id is a list, iterate over its values
                if isinstance(buid_id, list):
                    for inner_buid_id in buid_id:
                        # Check if the inner_buid_id value exists in the buid table
                        cur.execute("SELECT 1 FROM buid WHERE buid_id = %s", (inner_buid_id,))
                        if cur.fetchone() is not None:
                            # If the inner_buid_id value exists, insert the row into the session table
                            query = 'INSERT INTO session (session_id, buid_id) VALUES (%s,%s)'
                            insertion_data = (session_id, inner_buid_id)
                            try:
                                cur.execute(query, insertion_data)
                            except psycopg2.errors.UniqueViolation:
                                # If inserting this row would result in a duplicate key error, skip it
                                print(f"Skipping duplicate row with session_ id={session_id}")

                else:
                    # Check if the buid_id value exists in the buid table
                    cur.execute("SELECT 1 FROM buid WHERE buid_id = %s", (buid_id,))
                    if cur.fetchone() is not None:
                        # If the buid_id value exists, insert the row into the session table
                        query = 'INSERT INTO session (session_id, buid_id) VALUES (%s,%s)'
                        insertion_data = (session_id, buid_id)
                        try:
                            cur.execute(query, insertion_data)
                        except psycopg2.errors.UniqueViolation:
                            # If inserting this row would result in a duplicate key error, skip it
                            print(f"Skipping duplicate row with session_id={session_id}")
    print("It's done")


def session_product_to_db():
    for session in sessions:
        if 'order' not in session or session['order'] is None or 'products' not in session['order'] or not \
        session['order']['products']:
            continue
        if '_id' in session:
            session_id = session['_id']
            for product in session['order']['products']:
                if 'id' in product:
                    product_id = str(product['id'])
                    # Check if session_id exists in session table
                    cur.execute("SELECT 1 FROM session WHERE session_id = %s", (session_id,))
                    if cur.fetchone() is not None:
                        query = 'INSERT INTO session_product (session_id, product_id) VALUES (%s,%s)'
                        insertion_data = (session_id, product_id)
                        cur.execute(query, insertion_data)
                    else:
                        # session_id does not exist in session table, skip insertion
                        print(f'session_id {session_id} does not exist in session table')
    print("It's done")


def buid_to_db():
    for profile in profiles:
        if 'buids' not in profile or not profile['buids']:
            continue
        if '_id' in profile:
            buid_id = profile['buids'][0]
            profile_id = str(profile['_id'])
            query = 'INSERT INTO buid (buid_id, profile_id) VALUES (%s,%s)'
            insertion_data = (buid_id, profile_id)
            try:
                cur.execute(query, insertion_data)
            except psycopg2.errors.UniqueViolation:
                # If inserting this row would result in a duplicate key error, skip it
                print(f"Skipping duplicate row with buid_id={buid_id}")
    print("It's done")


def product_to_db():
    for product in products:
        if '_id' in product and 'gender' in product and 'fast_mover' in product and 'category' in product:
            product_id = product['_id']
            gender = product['gender']
            fast_mover = product['fast_mover']
            category_1 = product['category']
            query = 'INSERT INTO product (product_id, gender, fast_mover, category_1) VALUES(%s,%s,%s,%s) '
            insertion_data = (product_id, gender, fast_mover, category_1)
            try:
                cur.execute(query, insertion_data)
            except psycopg2.errors.UniqueViolation:
                # If inserting this row would result in a duplicate key error, skip it
                print(f"Skipping duplicate row with product_id={product_id}")
    print("It's done")


profile_to_db()
buid_to_db()
session_to_db()
session_product_to_db()
product_to_db()