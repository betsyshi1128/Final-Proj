import unittest
import requests
import sqlite3
import json
import os

def get_swapi_info(url, params=None):
    try:
        info = requests.get(url, params)
        d = info.json()
        print(d)
        return d
    except:
        print('Exception!')
        return None
    
def load_json(filename):
    try:
        with open(filename,'r') as f:
            # contents = f.read()
            data = json.load(f)
        f.close()
        return data
    except:
        return {}

def write_json(filename, dict):
    with open(filename, 'w') as f:
        json.dump(dict,f)
    return None

def set_up_database(db_name):
    """
    Sets up a SQLite database connection and cursor.

    Parameters
    -----------------------
    db_name: str
        The name of the SQLite database.

    Returns
    -----------------------
    Tuple (Cursor, Connection):
        A tuple containing the database cursor and connection objects.
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + db_name)
    cur = conn.cursor()
    return cur, conn


def set_up_types_table(data, cur, conn):
    """
    Returns
    -----------------------
    None
    """
    type_list = []
    for pokemon in data:
        pokemon_type = pokemon["type"][0]
        if pokemon_type not in type_list:
            type_list.append(pokemon_type)
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Types (id INTEGER PRIMARY KEY, type TEXT UNIQUE)"
    )
    for i in range(len(type_list)):
        cur.execute(
            "INSERT OR IGNORE INTO Types (id,type) VALUES (?,?)", (i, type_list[i])
        )
    conn.commit()


def set_up_price_table(data, cur, conn):
    cur.execute(
        'CREATE TABLE IF NOT EXISTS Price (name TEXT PRIMARY KEY, price INTEGER, value INTEGER, us_unit TEXT, net_price INTEGER)'
    )
    # print(data)
    for ingredient in data:
        # print(ingredient)
        name = ingredient['name']
        price = ingredient['price']
        value = ingredient['amount']['us']['value']
        us_unit = ingredient['amount']['us']['unit']
        net_price = ingredient['price']

        cur.execute(
            "INSERT INTO Pokemon (name, price, value, us_unit, net_price) VALUES (?, ?, ?, ?, ?)",
            (name, price, value, us_unit, net_price)
        )
    conn.commit()


# class TestAllMethods(unittest.TestCase):
#     def setUp(self):
#         path = os.path.dirname(os.path.abspath(__file__))
#         self.conn = sqlite3.connect(path+'/'+'pokemon.db')
#         self.cur = self.conn.cursor()
#         self.data = read_data_from_file('pokemon.json')

#     def test_pokemon_table(self):
#         self.cur.execute('SELECT * from Pokemon')
#         pokemon_list = self.cur.fetchall()
#         self.assertEqual(len(pokemon_list), 500)
#         self.assertEqual(len(pokemon_list[0]),8)
#         self.assertIs(type(pokemon_list[0][0]), str)
#         self.assertIs(type(pokemon_list[0][1]), int)
#         self.assertIs(type(pokemon_list[0][2]), int)
#         self.assertIs(type(pokemon_list[0][3]), int)
#         self.assertIs(type(pokemon_list[0][4]), int)
#         self.assertIs(type(pokemon_list[0][5]), int)

    
def main():



if __name__ == "__main__":
    main()

