import os, sys
import sqlite3 as sql
import pyperclip as clip
from time import sleep

#clip.copy(link_list)
#print ("Copied {} links".format(len(URIs)))

def create_db():
    db = sql.connect('curiositylist.db')
    c = db.cursor()
    c.execute('''CREATE TABLE categories
                 (name TEXT NOT NULL PRIMARY KEY, parent INTEGER NOT NULL, id INTEGER NOT NULL UNIQUE)''')
    c.execute('''CREATE TABLE history
                 (uri TEXT NOT NULL PRIMARY KEY, name TEXT NOT NULL, subcat INTEGER,
                  FOREIGN KEY (subcat) REFERENCES categories(id));''')
    c.execute('''CREATE TABLE backlog (name TEXT NOT NULL, subcat INTEGER,
                  FOREIGN KEY (subcat) REFERENCES categories(id));''')

    categories = [
        ('Science',        0,   1),
        ('History',        0,   5),
        ('Technology',     0,   6),
        ('Nature',         0,   7),
        ('Society',        0,   8),
        ('Lifestyle',      0,   9),
        ('Kids',           0, 113),

        ('Physics',    1,   37),  # Science
        ('Space',      1,   38),
        ('Mind',       1,   40),
        ('Biology',    1,   41),
        ('Genetics',   1,   42),
        ('Medicine',   1,   44),
        ('Evolution',  1,   94),
        ('Geology',    1,   95),
        ('Psychology', 1,  112),

        ('Prehistory',     5,  96),  # History
        ('Ancient',        5,  97),
        ('Medieval',       5,  98),
        ('Modern',         5,  99),
        ('Aviation',       5, 100),
        ('Biographies',    5, 101),
        ('Megastructures', 5, 102),
        ('Military',       5, 103),

        ('Energy',                  6, 45),  # Technology
        ('Engineering',             6, 47),
        ('Transportation',          6, 48),
        ('Communications',          6, 49),
        ('Nanotechnology',          6, 50),
        ('Artificial Intelligence', 6, 69),
        ('Privacy & Security',      6, 71),
        ('Social Web',              6, 72),

        ('Earth',                 7,  39),  # Nature
        ('Animals',               7, 105),
        ('Birds',                 7, 106),
        ('Insects',               7, 107),
        ('Natural Habitats',      7, 108),
        ('Prehistoric Creatures', 7, 109),
        ('Oceans',                7, 110),
        ('Plants',                7, 111),

        ('Entrepreneurship',    8, 54),  # Society
        ('Social Issues',       8, 55),
        ('Politics',            8, 56),
        ('Crime & Forensics',   8, 57),
        ('Economics',           8, 58),
        ('Business & Commerce', 8, 59),
        ('Democracy',           8, 60),
        ('Current Events',      8, 61),

        ('Food',              9,  62),  # Lifestyle
        ('Collecting',        9,  63),
        ('Performing Arts',   9,  64),
        ('Creativity',        9,  67),
        ('Home Projects',     9,  68),
        ('Philosophy',        9,  73),
        ('Health & Wellness', 9,  74),
        ('Travel',            9, 104),

        ('STEAM',              113, 114),  # Kids
        ('HistoryKids',        113, 115),
        ('Space Exploration',  113, 116),
        ('NatureKids',         113, 117),
        ('Dinosaurs',          113, 118),
        ('Current EventsKids', 113, 119)
    ]
    c.executemany('''INSERT OR IGNORE INTO categories VALUES (?, ?, ?)''', categories)
    db.commit()

    db.close()


def get_uri_list():
    # @todo: better handling of failures! Maybe return empty list an handle in main loop...
    error = os.system('adb shell "su -c \'cp /data/data/com.curiosity.curiositystream/databases/exoplayer_internal.db /sdcard/Download/curiosity/ -f\'"')
    if error:
        print("Could not get root access! Exiting...")
        sys.exit(1)
    
    error = os.system('adb pull /sdcard/Download/curiosity/exoplayer_internal.db')
    if error:
        print("Could not pull database! Exiting...")
        sys.exit(1)
    
    exoplayer = sql.connect('exoplayer_internal.db')
    exo_c = exoplayer.cursor()
    
    exo_c.execute('''SELECT uri FROM ExoPlayerDownloads''')
    URIs = exo_c.fetchall()
    
    link_list = ''
    for link in URIs:
        link_list += link[0] + '\n'
    exoplayer.close()
    
    return(link_list)


if __name__ == "__main__":
    running = True
    while running:
        os.system('cls')
        print("MENU:\n")
        print("1. Add URI entries.")
        print("2. Add titles to backlog.")
        print("3. Initialize database.")
        print("4. Clean duplicates.")
        print("x. Quit.")
        print("\nMake your choice: ", end='')
        choice = input()
        
        if len(choice) > 1:
            print("\nPlease enter a single character! Press enter to restart... ", end='')
            input()
        else:
            if   choice == 'x':
                running = False
            elif choice == '1':
                db = sql.connect('curiositylist.db')
                c = db.cursor()

                running_uri_loop = True
                repeating = False
                title_to_add = None
                uri_sum = 0
                while running_uri_loop:
                    if not repeating:
                        c.execute('''SELECT MIN(rowid), name, subcat FROM backlog;''')
                        title_to_add = c.fetchone()
                    repeating = False
                    if title_to_add == None or None in title_to_add:
                        print("\nThe backlog is empty. Press enter to restart.", end='')
                        input()
                        running_uri_loop = False
                    else:
                        print("\nAdding '{}' to database. Press enter to fetch URIs from phone... ".format(title_to_add[1]), end='')
                        if input() == 'x':
                            print("Cancelling...", end='')
                            sleep(0.3)
                            running_uri_loop = False
                        else:
                            uri_list = get_uri_list().split('\n')
                            insert_values = []
                            for uri in uri_list:
                                if uri.strip() != '':
                                    insert_values.append((uri, title_to_add[1], title_to_add[2]))
                            c.executemany('''INSERT OR IGNORE INTO history VALUES (?, ?, ?)''', insert_values)
                            uri_count = len(insert_values)
                            if uri_count < uri_sum:
                                uri_sum = 0
                            print('Fetched {} URIs. Correct? '.format(uri_count - uri_sum), end='')
                            choice = input()
                            if choice == '' or choice[0].lower() == 'y':
                                c.execute('''DELETE FROM backlog WHERE name=?''', (title_to_add[1],))
                                uri_sum = len(insert_values)
                            else:
                                repeating = True
                            db.commit()
                db.close()
            elif choice == '2':
                db = sql.connect('curiositylist.db')
                c = db.cursor()
                print("\nInput category ID: ", end='')
                cat_id = input()  # @todo: check this

                print("Press enter to paste title list from clipboard. ", end='')
                input()
                title_list = clip.paste()
                print("\n\n{}".format(title_list))
                print("\nIs this the correct list? ", end='')
                choice = input()
                if choice == '' or choice[0].lower() == 'y':
                    for title in title_list.split('\n'):
                        c.execute('''INSERT INTO backlog VALUES (?, ?);''', (title, cat_id))
                    db.commit()
                else:
                    print("Cancelling...", end='')
                    sleep(0.3)
                db.close()
            elif choice == '3':
                try:
                    create_db()
                except:
                    print("\nCould not initialize database. Press enter to restart... ", end='')
                    input()
                    continue
                print("\nSuccessfully initialized database. Press enter to continue... ", end='')
                input()
            elif choice == '4':
                db = sql.connect('curiositylist.db')
                c = db.cursor()
                c.execute('''SELECT name,subcat FROM backlog ORDER BY rowid''')
                titles = c.fetchall()
                already_deleted = []
                to_delete = []
                for title in titles:
                    if not (title[0] in already_deleted):
                        to_delete.append((title[0], title[1]))
                        already_deleted.append(title[0])
                c.executemany('''DELETE FROM backlog WHERE name=? AND subcat<>?''', to_delete)
                db.commit()
                print("Deleted {} entries. ".format(len(to_delete)), end='')
                sleep(0.3)
