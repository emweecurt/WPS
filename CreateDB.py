import sqlite3

conn = sqlite3.connect('Pitching_data.db')

c = conn.cursor()

c.execute("PRAGMA foreign_keys = on")

c.execute('''CREATE TABLE IF NOT EXISTS games (
    Id INTEGER PRIMARY KEY, 
    Date TEXT, 
    HomeTeam TEXT, 
    AwayTeam TEXT, 
    Park TEXT,
    HomeTeamWon INTEGER)''')

c.execute('''CREATE TABLE IF NOT EXISTS starts (
    Id INTEGER PRIMARY KEY, 
    GameId INTEGER, 
    PitcherName TEXT, 
    PitcherId INTEGER,
    IsHomeTeam INTEGER, 
    Outs INTEGER, 
    H INTEGER, 
    R INTEGER, 
    ER INTEGER, 
    HR INTEGER, 
    BB INTEGER, 
    SO INTEGER, 
    NP INTEGER, 
    S INTEGER, 
    BF INTEGER, 
    GS INTEGER, 
    GS_BJ INTEGER, 
    GS_2 INTEGER, 
    FOREIGN KEY(GameId) REFERENCES games(Id))''')

# c.execute('''INSERT INTO games (Id, Date, HomeTeam, AwayTeam, Park, HomeTeamWon)
#     VALUES (1, '2017_05_01', 'STL Cardinals', 'ATL Barves', 'Microsoft Field', 1)''')

# c.execute('''INSERT INTO starts (Id, GameId, PitcherName, PitcherId, IsHomeTeam, Outs, H, R, ER, HR, BB, SO, NP, S, BF, GS, GS_BJ, GS_2)
#     VALUES (1, 1, 'Michael Wacha', 12674, 1, 15, 3, 2, 1, 0, 3, 4, 85, 58, 23, 12, 12, 18)''')

conn.commit()

conn.close()