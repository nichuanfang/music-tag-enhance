from db import postgres
from db import sqlite

def main():
    p_result = postgres.fetch_data('select * from public.music_scrobble_records limit 10')
    print(p_result)
    s_result = sqlite.fetch_data('SELECT * FROM music_listen LIMIT 10')
    print(s_result)

if __name__ == "__main__":
    main()