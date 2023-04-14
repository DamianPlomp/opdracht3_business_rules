import psycopg2
import random

#Relationele database connection
con = psycopg2.connect(
    host='localhost',
    database='opdracht3_sp',
    user='postgres',
    password='1824')

con.autocommit = True
cur = con.cursor()

#Tijdelijke input
test_product = 'SELECT TOP 1 category_1 FROM product'
gender_test_product = 'SELECT TOP 1 gender FROM product'
test_profiles = 'SELECT TOP 2 profile_id FROM profile'

cur.execute(test_product)

def collab_filter():
    """
    Reccomend een product d.m.v. het kijken naar wat andere profielen leuk vonden.
    :return final_rec: list
    """
    # Get viewed_before from the first profile in the database
    viewed_before = [cur.execute('SELECT viewed_before FROM profile WHERE profile_id = (%s)'), test_profiles[0]]
    final_rec = []
    products = []
    categories = []
    # add viewed_before items into different products list
    for i in range(len(viewed_before)):
        products.append(viewed_before[i])
    # get category from each product in products list
    for product in products:
        category = cur.execute('SELECT category_1 FROM product WHERE product_id = (%s)', product)
        categories.append(category)
    # get all product that have the same category as the products in products
    for category in categories:
        final_rec.append(cur.execute('SELECT * FROM product WHERE category_1 = (%s)'), category)

    # shuffle the list, so that the user most likely gets a different product recommended each time
    random.shuffle(final_rec)

    # fill final_rec with products sorted by gender
    if len(final_rec) < 8:
        genders = []
        fill_products = []
        for product in products:
            gender = cur.execute('SELECT gender FROM product WHERE product_id = (%s)'), product
            genders.append(gender)
        for gender in genders:
            product = cur.execute('SELECT product_id FROM product WHERE gender = (%s)'), gender
            if product in fill_products:
                pass
            else:
                fill_products.append(products)
        for item in fill_products:
            if len(final_rec) < 8:
                final_rec.append(item)
            else:
                break
    # if list is long enough, create new list with 8 products to recommend
    elif len(final_rec) > 8:
        final_rec.shuffle()
        recommendation = []
        for i in range(8):
            recommendation.append(final_rec[i])
        return recommendation

    return final_rec



def content_filter():
    """
    Recommend een product aan m.b.v. product informatie
    :return final_rec: list
    """
    final_rec = []
    # get all products where category is the same
    category_search = [cur.execute('SELECT product_id FROM product WHERE category_1 = (%s)', (test_product,))]
    # if the list is not long enough
    if len(category_search) < 8:
        gender_search = [cur.execute('SELECT * FROM product WHERE gender = (%s)', (gender_test_product,))]
        for i in range(len(category_search) + 1):
            category_search.append(gender_search[i])
        final_rec = category_search.copy()
    # if the list is long enough, create a list of product ids of length 8
    elif len(category_search) > 8:
        for i in range(8):
            random.shuffle(category_search)
            final_rec.append(category_search[i])
    return final_rec

def fast_mover_filter():
    """
    Recommend producten m.b.v. fast_mover
    :return: final_rec: list
    """
    # Get all products which move fast
    fast_move_search = [cur.execute('SELECT * FROM product WHERE fast_mover = TRUE')]
    fast_move_search.shuffle()
    final_rec = []
    for i in range(8):
        final_rec.append(fast_move_search[i])
    return final_rec