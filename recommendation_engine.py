import psycopg2
import random

class RecommendationEngine:
    def __init__(self, host, database, user, password):
        self.connection = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()

    def close_connection(self):
        self.cursor.close()
        self.connection.close()

    def execute_query(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def collab_filter(self, profile_id):
        query = 'SELECT viewed_before FROM profile WHERE profile_id = %s'
        viewed_before = self.execute_query(query, (profile_id,))[0][0]
        final_rec = []
        products = []
        categories = []

        for product_id in viewed_before:
            query = 'SELECT product_id, category_1, gender FROM product WHERE product_id = %s'
            product = self.execute_query(query, (product_id,))
            products.append(product)
            categories.append(product[0][1])

        for category in categories:
            query = 'SELECT * FROM product WHERE category_1 = %s'
            final_rec.extend(self.execute_query(query, (category,)))

        random.shuffle(final_rec)
        return final_rec[:8]

    def content_filter(self, category_1, gender):
        query = 'SELECT product_id FROM product WHERE category_1 = %s'
        category_search = self.execute_query(query, (category_1,))

        if len(category_search) < 8:
            query = 'SELECT * FROM product WHERE gender = %s'
            gender_search = self.execute_query(query, (gender,))
            category_search += gender_search

        random.shuffle(category_search)
        return category_search[:8]

    def fast_mover_filter(self):
        query = 'SELECT * FROM product WHERE fast_mover = TRUE'
        fast_move_search = self.execute_query(query)
        random.shuffle(fast_move_search)
        return fast_move_search[:8]
