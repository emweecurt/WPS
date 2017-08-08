import sqlite3

conn = sqlite3.connect('Pitching_data.db')

c = conn.cursor()

c.execute('''CREATE TABLE starts (GameId integer, PitcherName text, PitcherId integer, Outs integer, H integer, 
            R integer, ER integer, HR integer, BB integer, SO integer, NP integer, S integer, BF integer, GS integer, 
            GS_BJ integer, GS_2 integer)''')

c.execute('''CREATE TABLE games (Id integer, Date text, HomeTeam text, AwayTeam text, Park text)''')
