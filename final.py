import unittest
import sqlite3
import json
import os

def read_data_from_file(filename):
    """
    Reads data from a file with the given filename.

    Parameters
    -----------------------
    filename: str
        The name of the file to read.

    Returns
    -----------------------
    dict:
        Parsed JSON data from the file.
    """
    full_path = os.path.join(os.path.dirname(__file__), filename)
    f = open(full_path)
    file_data = f.read()
    f.close()
    json_data = json.loads(file_data)
    return json_data


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
    Sets up the Types table in the database using the provided Pokemon data.

    Parameters
    -----------------------
    data: list
        List of Pokemon data in JSON format.

    cur: Cursor
        The database cursor object.

    conn: Connection
        The database connection object.

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


def set_up_pokemon_table(data, cur, conn):
    cur.execute(
        'CREATE TABLE IF NOT EXISTS Pokemon (name TEXT PRIMARY KEY, type_id INTEGER, HP INTEGER, attack INTEGER, defense INTEGER, speed INTEGER, spl_attack INTEGER, spl_defense INTEGER)'
    )
    # print(data)
    type_mapping = {row[1]: row[0] for row in cur.execute("SELECT id, type FROM Types")}
    # print(type_mapping)
    for pokemon in data:
        # print(pokemon)
        name = pokemon['name']
        type_id = type_mapping[pokemon['type'][0]]
        HP = pokemon['stats']['hp']
        attack = pokemon['stats']['attack']
        defense = pokemon['stats']['defense']
        speed = pokemon['stats']['speed']
        spl_attack = pokemon['stats']['special-attack']
        spl_defense = pokemon['stats']['special-defense']
        cur.execute(
            "INSERT INTO Pokemon (name, type_id, HP, attack, defense, speed, spl_attack, spl_defense) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (name, type_id, HP, attack, defense, speed, spl_attack, spl_defense),
        )
    conn.commit()
    """
    Sets up the Pokemon table in the database using the provided Pokemon data.

    [TASK 1]: 20 points

    1. Iterate through the JSON data to get a list of pokemon
    2. Load all of the pokemon into a database table called Pokemon, with the following columns in each row:
        - name (datatype: text and Primary key)
        - type_id (datatype: integer)
        - HP (datatype: integer)
        - attack (datatype: integer)
        - defense (datatype: integer)
        - speed (datatype: integer)
    Hint: To find the type_id for each pokemon, you will have to look up the first type of each pokemon
    in the types table we create for you. See setUpTypesTable for details.

    Parameters
    -----------------------
    data: list
        List of Pokemon data in JSON format

    cur: Cursor
        The database cursor object

    conn: Connection
        The database connection object

    Returns
    -----------------------
    None
    """


def get_pokemon_by_HP(hp, cur):
    cur.execute("SELECT name, type_id, HP FROM Pokemon WHERE HP = ?", (hp,))
    result = cur.fetchall()
    return result
    """
    This function returns a list of tuples containing pokemon that have a particular HP
    
    [TASK 2]: 10 points
    Select the pokemon from the pokemon table that have 
    Each tuple contains the pokemon name, type_id, and the HP.

    Parameters
    -----------------------
    hp: int
    A pokemon's HP (Hit Points)

    cur: Cursor
    The database cursor object

    Returns
    -----------------------
    tuple: (name, type_id, hp)
    """


def get_pokemon_above_HP_equal_speed_and_attack(hp, cur):
    cur.execute("SELECT name, speed, defense FROM Pokemon WHERE HP > ? AND attack = speed", (hp,))
    result = cur.fetchall()
    return result
    """
    [TASK 3]: 10 points
    The function takes 2 arguments as input: the HP and the database cursor.
    It selects all pokemon greater than the HP passed to the function, 
    having an equal attack and speed stat.
    The function returns a list of tuples.
     Each tuple in the list contains the pokemon name, speed, and defense.

    Parameters
    -----------------------
    hp: int
        A pokemon's HP value

    cur: Cursor
        The database cursor object

    Returns
    -----------------------
    list of tuples: [(name, speed, defense), ...]
    """


def get_pokemon_above_speed_above_defense_of_type(speed, defense, type, cur):
    cur.execute("SELECT name, type, speed, defense FROM Pokemon JOIN Types ON Pokemon.type_id = Types.id WHERE Types.type = ? AND speed > ? AND defense > ?", 
                (type,speed,defense))
    result = cur.fetchall()
    # print(result)
    return result
    """
    [TASK 4]: 15 points
    This function selects all pokemon of a type:
    - At a speed greater than the speed passed to the function,
    - At a defense greater than the defense passed to the function.

    It returns a list of tuples, each tuple containing the
    pokemon name, type, speed, and defense.

    Hint: You have to use JOIN for this task.

    Parameters
    -----------------------
    speed: int
        A pokemon's speed value

    defense: int
        A pokemon's defense value

    type: str
        A pokemon's type

    cur: Cursor
        The database cursor object

    Returns
    -----------------------
    list of tuples: [(name, type, speed, defense), ...]
    """


def get_special_attack_pokemon_of_type(type, cur):
    cur.execute("SELECT name, type, attack, spl_attack FROM Pokemon JOIN Types ON Pokemon.type_id = Types.id WHERE Types.type = ? AND spl_attack >= attack+20", 
                (type,))
    result = cur.fetchall()
    # print(result)
    return result
    """
    [EXTRA CREDIT]
    This function selects all pokemon of a type that have a special attack value that is 20 or more points than their regular attack value
    i.e. spl_attack >= attack+20

    Parameters
    -----------------------
    type: str
        A pokemon's type
    
    cur: Cursor
        The database cursor object

    Returns
    -----------------------
    list of tuples: [(name, type, attack, spl_attack), ...]
    """

class TestAllMethods(unittest.TestCase):
    def setUp(self):
        path = os.path.dirname(os.path.abspath(__file__))
        self.conn = sqlite3.connect(path+'/'+'pokemon.db')
        self.cur = self.conn.cursor()
        self.data = read_data_from_file('pokemon.json')

    def test_pokemon_table(self):
        self.cur.execute('SELECT * from Pokemon')
        pokemon_list = self.cur.fetchall()
        self.assertEqual(len(pokemon_list), 500)
        self.assertEqual(len(pokemon_list[0]),8)
        self.assertIs(type(pokemon_list[0][0]), str)
        self.assertIs(type(pokemon_list[0][1]), int)
        self.assertIs(type(pokemon_list[0][2]), int)
        self.assertIs(type(pokemon_list[0][3]), int)
        self.assertIs(type(pokemon_list[0][4]), int)
        self.assertIs(type(pokemon_list[0][5]), int)
        self.assertIs(type(pokemon_list[0][6]), int)
        self.assertIs(type(pokemon_list[0][7]), int)


    def test_get_pokemon_by_HP(self):
        x = sorted(get_pokemon_by_HP(45, self.cur))
        self.assertEqual(len(x),25)
        self.assertEqual(len(x[0]), 3)
        self.assertEqual(x[0][0],"anorith")

        y = get_pokemon_by_HP(30, self.cur)
        self.assertEqual(len(y),12)
        self.assertEqual(y[2],('gastly', 12, 30))
        self.assertEqual(y[4][2],30)
        self.assertEqual(y[5][1],2)


    def test_get_pokemon_above_HP_equal_speed_and_attack(self):

        a = get_pokemon_above_HP_equal_speed_and_attack(60, self.cur)
        self.assertEqual(len(a),23)
        self.assertEqual(a[0][1],45)
        self.assertEqual(a[3][2],100)
        self.assertEqual(len(a[1]), 3)

    def test_get_pokemon_above_speed_above_defense_of_type(self):
 
        b = get_pokemon_above_speed_above_defense_of_type(75, 50, "grass", self.cur)
        self.assertEqual(len(b), 11)
        self.assertEqual(b[0][0],'venusaur' )
        self.assertEqual(len(b[1]), 4) 
        self.assertEqual(b[1], ('meganium', 'grass', 80, 100)) 

    
    # UNCOMMENT THIS FUNCTION TO TEST YOUR EXTRA CREDIT SUBMISSION

    def test_get_special_attack_pokemon_of_type(self):
        e = get_special_attack_pokemon_of_type("fire", self.cur)
        self.assertEqual(len(e), 7)

        f = get_special_attack_pokemon_of_type("water",self.cur)
        self.assertEqual(f[0][0], 'slowbro') 

def main():

    json_data = read_data_from_file("pokemon.json")
    cur, conn = set_up_database("pokemon.db")
    set_up_types_table(json_data, cur, conn)
    set_up_pokemon_table(json_data, cur, conn)
    conn.close()

if __name__ == "__main__":
    main()

