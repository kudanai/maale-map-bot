import pandas as pd
from fuzzywuzzy import fuzz, process
import sqlite3

from models.address_source import AddressSource


class SQLiteDatasource(AddressSource):
    """
    SQLite backed address data source.
    And a pandas dataframe for fuzzywuzzy suggestions

    Uses fts5 for search: 
    note: update the fts table if data is changed
        CREATE VIRTUAL TABLE IF NOT EXISTS addresses_index USING fts5(name, district, lat, lng, road, postalcode, tokenize=porter);
        DELETE FROM addresses_index;
        INSERT INTO addresses_index SELECT name, district, lat, lng, road, postalcode FROM addresses;
    """

    def __init__(self, db_source):
        self.__dbconn = sqlite3.connect(db_source)
        self.__df = pd.read_sql_query("SELECT name from addresses", self.__dbconn)

    def __query_df(self, q):
        return [x[0] for x in process.extractBests(q, self.__df['name'], scorer=fuzz.WRatio, score_cutoff=70, limit=5)]
        # return (self.__df[self.__df.apply(lambda row: fuzz.WRatio(row['name'],q), axis=1) > 70]['name']).tolist()

    def __row_to_dict(self, row):
        return {
            "id": self._get_address_hash(row[0]),
            "latitude": row[2],
            "longitude": row[3],
            "title": str(row[0]).title(),
            "address": f"{row[4]}, {row[5]}".title()
        }

    def get_suggestions(self, query):
        return self.__query_df(query)

    def get_addresses_results(self, query):
        items = []

        if query:
            c = self.__dbconn.cursor()
            try:
                res = c.execute("SELECT * FROM addresses_index WHERE addresses_index MATCH ? ORDER BY rank LIMIT 10;",
                                (f"name:{query}*",))
                for row in res:
                    items.append(self.__row_to_dict(row))
            except Exception as e:
                pass

            c.close()
        return items
