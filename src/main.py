import sys
import os
import sqlite3
import pandas as pd
from pybaseball import standings
from pybaseball import team_batting
import tkinter as tk
from tkinter import ttk

# goes through the year that you want
# eventually will be able to compare years
# like take for example 2025 and 2024 and see how they compare

#connection to SQL db
connection = sqlite3.connect("data/mlb.db")

def rate_team(win_percentage):

    if win_percentage > 0.599:
        return "Excellent"

    elif win_percentage > 0.550:
        return "Good"

    elif win_percentage > 0.500:
        return "Average"

    else:
        return "Below Average"

#print each to check the output

print(rate_team(0.610))
print(rate_team(0.575))
print(rate_team(0.520))
print(rate_team(0.400))

# get the connection that I will play with 
cursor = connection.cursor()
cursor.execute("""
    SELECT Tm,W, L, Win_Percentage
    FROM team_records
""")


teams = cursor.fetchall()
# print used just to check 
#print(teams)

for team,wins,losses, win_percentage in teams:
    rating = rate_team(win_percentage)
    # print(teams)
    print(f"{team} - {wins} wins - {rating}")

# set up the javafx but python
root = tk.Tk()
root.title("MLB analysis")
root.geometry("500x400")

# labels
year_label = tk.Label(root, text="Select Year:")
year_label.pack()

# range
years = list(range(2025, 1999, -1))

# just commendted out for now
#print(years)

year_dropdown = ttk.Combobox(
    root, 
    values=years,
    state="readonly"
    )
year_dropdown.pack()

year_dropdown.set(2025)


def analyze_year():
    selected_year = year_dropdown.get()
    print(f"Selected year: {selected_year}")

analyze_button = tk.Button(
    root,
    text="Analyze",
    command=analyze_year
)

analyze_button.pack()

root.mainloop()

def season_exists(year):
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT 1
        FROM team_records
        WHERE Season = ?
        LIMIT 1
        """,
        (year,)

    )

    result = cursor.fetchone()
    return result is not None
    print(season_exists(connection,2025))
    print(season_exists(connection,2024))

def analyze_year():

    selected_year = int(year_dropdown.get())
    if season_exists(connection, selected_year):
        print(f"Season {selected_year} is already in the database")
    else:
        print(f"Season {selected_year} is not in the database")


