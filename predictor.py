from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pprint import pprint
import datetime
from pytz import timezone
import sys

def get_day_df(day):
  """Return a cleaned dataframe for a given day."""    
  if day not in ["MON", "TUES", "WED", "THURS", "FRI"]:
      return None
  df = pd.read_csv(f"./data_by_day/{day}.csv")
  df.rename(columns={"Unnamed: 0": "Timestamp", "Unnamed: 29": "AVG(TECH)", 
                    "Unnamed: 30": "dAVG(TECH)", "Unnamed: 31": "AVG(PARK)", 
                    "Unnamed: 32": "dAVG(PARK)"}, inplace=True)

  df.drop(index=0, inplace=True) # drops redundant header rows

  # Only keep named columns
  df = df[['Timestamp', 'AVG(TECH)', 'dAVG(TECH)', 'AVG(PARK)', 'dAVG(PARK)']]
  df.set_index(df['Timestamp'], inplace=True)
  df.drop(['Timestamp'], axis=1, inplace=True)
  return df

def predict(day, time):
  """Predicts the parking availabtility in `duration` minutes from now"""
  df = get_day_df(day)
  tech = df.loc[time]["AVG(TECH)"]
  park = df.loc[time]["AVG(PARK)"]
  return {
      "TECH": df.loc[time]["AVG(TECH)"],
      "dTECH": df.loc[time]["dAVG(TECH)"],
      "PARK": df.loc[time]["AVG(PARK)"],
      "dPARK": df.loc[time]["dAVG(PARK)"],
  }

def get_status(garage, day, time):
  """Retrieves parking garage status."""    
  data = predict(day, time)
  pred = int(data[garage])
  delta = int(data["d"+garage])

  rv = f"Status of: {garage} @ {day} {time}\n\n"
  if pred < 100:
    rv += "RED - Above 90% capacity.\n"
  elif 100 <= pred < 200:
    rv += "YELLOW - At about 80% capacity.\n"
  else:
    rv += "GREEN - Plenty of parking.\n"

  if delta > 0:
    rv += "Good news, spots are freeing up.\n"
  else:
    rv += "Better hurry, spots are filling up.\n"

  rv += f"{pred} spots should be available.\n"
  
  return rv


if __name__ == "__main__":
  deck = sys.argv[1]  # TECH or
  day = sys.argv[2]   # all caps shortened
  time = sys.argv[3]  # as hh:mm

  print(get_status(deck, day, time))