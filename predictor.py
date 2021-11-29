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

def predict(duration):
  """Predicts the parking availabtility in `duration` minutes from now"""
  # tz = timezone('US/Eastern')
  # et_now = datetime.datetime.now(tz)
  et_now = datetime.datetime(2021, 11, 28, 12, 00)

  then = et_now + datetime.timedelta(minutes=duration)
  day_str = then.strftime("%a").upper()
  day_str = "MON"
  then_str = then.strftime("%H:%M")
  # then_str = "13:00"

  df = get_day_df(day_str)
  tech = df.loc[then_str]["AVG(TECH)"]
  park = df.loc[then_str]["AVG(PARK)"]
  spots = int(tech) + int(park)

  return {
      "TECH": df.loc[then_str]["AVG(TECH)"],
      "dTECH": df.loc[then_str]["dAVG(TECH)"],
      "PARK": df.loc[then_str]["AVG(PARK)"],
      "dPARK": df.loc[then_str]["dAVG(PARK)"],
  }
  return spots

def get_status(garage, duration):
  """Retrieves parking garage status."""    
  data = predict(duration)
  pred = int(data[garage])
  delta = int(data["d"+garage])

  rv = f"Status of: {garage}\n\n"
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

  rv += f"{pred} spots currently available.\n"
  
  return rv


if __name__ == "__main__":
  duration = int(sys.argv[1])
  deck = sys.argv[2]
  print(get_status(deck, duration))