import sqlite3
import csv
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'adult.db')
DATA_FILES = [
    os.path.join(os.path.dirname(__file__), '..', 'adult.data'),
    os.path.join(os.path.dirname(__file__), '..', 'adult.test')
]

COLUMNS = [
    'age', 'workclass', 'fnlwgt', 'education', 'education-num', 'marital-status',
    'occupation', 'relationship', 'race', 'sex', 'capital-gain', 'capital-loss',
    'hours-per-week', 'native-country', 'class'
]

CATEGORICAL = [
    'workclass', 'education', 'marital-status', 'occupation',
    'relationship', 'race', 'sex', 'native-country', 'class'
]

TABLES = [
    'workclass', 'education', 'marital_status', 'occupation',
    'relationship', 'race', 'sex', 'native_country', 'class'
]

# Mapping from column name to table name (for foreign keys)
COL_TO_TABLE = {
    'workclass': 'workclass',
    'education': 'education',
    'marital-status': 'marital_status',
    'occupation': 'occupation',
    'relationship': 'relationship',
    'race': 'race',
    'sex': 'sex',
    'native-country': 'native_country',
    'class': 'class'
}

SCHEMA = '''
CREATE TABLE IF NOT EXISTS workclass (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);
CREATE TABLE IF NOT EXISTS education (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);
CREATE TABLE IF NOT EXISTS marital_status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);
CREATE TABLE IF NOT EXISTS occupation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);
CREATE TABLE IF NOT EXISTS relationship (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);
CREATE TABLE IF NOT EXISTS race (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);
CREATE TABLE IF NOT EXISTS sex (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);
CREATE TABLE IF NOT EXISTS native_country (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);
CREATE TABLE IF NOT EXISTS class (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);
CREATE TABLE IF NOT EXISTS person (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    age INTEGER,
    workclass_id INTEGER,
    fnlwgt INTEGER,
    education_id INTEGER,
    education_num INTEGER,
    marital_status_id INTEGER,
    occupation_id INTEGER,
    relationship_id INTEGER,
    race_id INTEGER,
    sex_id INTEGER,
    capital_gain INTEGER,
    capital_loss INTEGER,
    hours_per_week INTEGER,
    native_country_id INTEGER,
    class_id INTEGER,
    FOREIGN KEY (workclass_id) REFERENCES workclass(id),
    FOREIGN KEY (education_id) REFERENCES education(id),
    FOREIGN KEY (marital_status_id) REFERENCES marital_status(id),
    FOREIGN KEY (occupation_id) REFERENCES occupation(id),
    FOREIGN KEY (relationship_id) REFERENCES relationship(id),
    FOREIGN KEY (race_id) REFERENCES race(id),
    FOREIGN KEY (sex_id) REFERENCES sex(id),
    FOREIGN KEY (native_country_id) REFERENCES native_country(id),
    FOREIGN KEY (class_id) REFERENCES class(id)
);
'''

def reset_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    print('Database reset.')

def initialize_database():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for stmt in SCHEMA.split(';'):
        if stmt.strip():
            c.execute(stmt)
    conn.commit()
    conn.close()
    print('Database initialized.')

def get_or_create_id(conn, table, value):
    c = conn.cursor()
    c.execute(f'SELECT id FROM {table} WHERE name = ?', (value,))
    row = c.fetchone()
    if row:
        return row[0]
    c.execute(f'INSERT INTO {table} (name) VALUES (?)', (value,))
    conn.commit()
    return c.lastrowid

def fill_database():
    conn = sqlite3.connect(DB_PATH)
    for table in TABLES:
        conn.execute(f'DELETE FROM {table}')
    conn.execute('DELETE FROM person')
    conn.commit()
    for filename in DATA_FILES:
        with open(filename, encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=',', skipinitialspace=True)
            for row in reader:
                if len(row) != len(COLUMNS):
                    continue
                data = {}
                for i, col in enumerate(COLUMNS):
                    val = row[i].strip()
                    if col in CATEGORICAL:
                        table = COL_TO_TABLE[col]
                        val_id = get_or_create_id(conn, table, val)
                        data[col] = val_id
                    else:
                        data[col] = val if val != '?' else None
                conn.execute('''
                    INSERT INTO person (
                        age, workclass_id, fnlwgt, education_id, education_num, marital_status_id,
                        occupation_id, relationship_id, race_id, sex_id, capital_gain, capital_loss,
                        hours_per_week, native_country_id, class_id
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    int(data['age']) if data['age'] else None,
                    data['workclass'],
                    int(data['fnlwgt']) if data['fnlwgt'] else None,
                    data['education'],
                    int(data['education-num']) if data['education-num'] else None,
                    data['marital-status'],
                    data['occupation'],
                    data['relationship'],
                    data['race'],
                    data['sex'],
                    int(data['capital-gain']) if data['capital-gain'] else None,
                    int(data['capital-loss']) if data['capital-loss'] else None,
                    int(data['hours-per-week']) if data['hours-per-week'] else None,
                    data['native-country'],
                    data['class']
                ))
    conn.commit()
    conn.close()
    print('Database filled with data.')

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Initialise, remplir ou reset la base Adult SQLite.')
    parser.add_argument('action', choices=['init', 'fill', 'reset'], help='Action à effectuer')
    args = parser.parse_args()
    if args.action == 'reset':
        reset_database()
    elif args.action == 'init':
        initialize_database()
    elif args.action == 'fill':
        fill_database()
