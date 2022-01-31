#
# header comment? Overview, name, etc.
# Ada Pici, Project 1, CS 341 UIC


import sqlite3
import matplotlib.pyplot as figure


###########################################################  
#
# print_stats
#
# Given a connection to the CTA database, executes various
# SQL queries to retrieve and output basic stats.
#
def print_stats(dbConn):
    dbCursor = dbConn.cursor()
    
    print("General stats:")
    
    dbCursor.execute("Select count(*) From Stations;")
    row = dbCursor.fetchone();
    print("  # of stations:", f"{row[0]:,}")
    dbCursor.execute("Select count(*) From Stops;")
    row2 = dbCursor.fetchone();
    print("  # of stops:", f"{row2[0]:,}")
    dbCursor.execute("Select count(*) From Ridership")
    row3 = dbCursor.fetchone();
    print("  # of ride entries:", f"{row3[0]:,}")
    
    dbCursor.execute("Select date(Ride_Date) From Ridership")
    row5 = dbCursor.fetchall();
    # for row in row5[:1]:
    #   print(row[0])
    # for row in row5[-1:]:
    #   print(row[0])
    for row in row5[-1:]:
      print("  date range:", row5[0][0],"-", row[-1])
    dbCursor.execute("Select sum(Num_Riders) From Ridership;")
    row4 = dbCursor.fetchone();
    print("  Total ridership:", f"{row4[0]:,}")
    dbCursor.execute("Select printf('%,d',sum(Num_Riders)), ROUND(Sum(Num_Riders)) / (Select Sum(Num_Riders) FROM Ridership) *100 From Ridership WHERE Type_of_Day = 'W'")
    row6 = dbCursor.fetchall();
    for row in row6:
      print("  Weekday ridership:" , row[0], f"({row[1]:.2f}%)")
    dbCursor.execute("Select printf('%,d',sum(Num_Riders)), ROUND(Sum(Num_Riders)) / (Select Sum(Num_Riders) FROM Ridership) *100 From Ridership WHERE Type_of_Day = 'A'")
    row6 = dbCursor.fetchall();
    for row in row6:
      print("  Saturday ridership:" , row[0], f"({row[1]:.2f}%)")
    dbCursor.execute("Select printf('%,d',sum(Num_Riders)), ROUND(Sum(Num_Riders)) / (Select Sum(Num_Riders) FROM Ridership) *100 From Ridership WHERE Type_of_Day = 'U'")
    row6 = dbCursor.fetchall();
    for row in row6:
      print("  Sunday/holiday ridership:" , row[0], f"({row[1]:.2f}%)\n")

#
# command1
#
#user inputs a station name and program searches for stations that are "like" the user's input   
def command1(dbConn):
  print()
  dbCursor = dbConn.cursor()

  sql = "Select Station_ID, Station_Name from Stations WHERE Station_Name LIKE ? ORDER BY Station_Name asc"
  stationName = input("Enter partial station name (wildcards _ and %): ")
  
  dbCursor.execute(sql, [stationName])
  rows = dbCursor.fetchall()

  if not rows:
      print("**No stations found...")
      print()
  for row in rows:
    print(row[0], ":", row[1])
  print()
#
# command2
#
#output the ridership at each station in asc order by station name, output the percentage this value represents across the total L
def command2(dbConn):
  dbCursor = dbConn.cursor()
  print("** ridership all stations **")
  
  sql = "Select Station_Name, printf('%,d', SUM(Num_Riders)),ROUND(Sum(Num_Riders)) /(SELECT SUM(Num_Riders) FROM Stations JOIN Ridership ON (Stations.Station_ID = Ridership.Station_ID))*100 FROM Stations JOIN Ridership ON (Stations.Station_ID = Ridership.Station_ID) GROUP BY Station_Name "

  dbCursor.execute(sql)
  rows = dbCursor.fetchall()
  
  #formatting output, outputting results
  for row in rows:
    stationname = row[0]
    ridership = row[1]
    percentage = row[2]
    print(stationname, ":", ridership, f"({percentage:.2f}%)")
  print()
#
# command3
#
# output the top-10 busiest stations in terms of ridership, in descending order by ridership:
def command3(dbConn):
  dbCursor = dbConn.cursor()
  print("** top-10 stations **")

  sql = "SELECT Station_Name, printf('%,d', SUM(Num_Riders)), ROUND(Sum(Num_Riders)) /(SELECT SUM(Num_Riders) FROM Stations JOIN Ridership ON (Stations.Station_ID = Ridership.Station_ID))*100 FROM Stations JOIN Ridership ON (Stations.Station_ID = Ridership.Station_ID) GROUP BY Station_Name ORDER BY Sum(Num_Riders) DESC LIMIT 10"

  dbCursor.execute(sql)
  rows = dbCursor.fetchall()

  for row in rows:
    stationname = row[0]
    ridership = row[1]
    percentage = row[2]
    print(stationname, ":", ridership, f"({percentage:.2f}%)")
  print()
#
# command4
#
# output the least-10 busiest stations in terms of ridership, in ascending order by ridership:
def command4(dbConn):
  dbCursor = dbConn.cursor()
  print("** least-10 stations **")

  sql = "SELECT Station_Name, printf('%,d', SUM(Num_Riders)), ROUND(Sum(Num_Riders)) /(SELECT SUM(Num_Riders) FROM Stations JOIN Ridership ON (Stations.Station_ID = Ridership.Station_ID))*100 FROM Stations JOIN Ridership ON (Stations.Station_ID = Ridership.Station_ID) GROUP BY Station_Name ORDER BY Sum(Num_Riders) ASC LIMIT 10"

  dbCursor.execute(sql)
  rows = dbCursor.fetchall()

  for row in rows:
    stationname = row[0]
    ridership = row[1]
    percentage = row[2]
    print(stationname, ":", ridership, f"({percentage:.2f}%)")
  print()
#
# command5
#
# input a line of color from the user and output all stop names that are part of that line, in ascending order. If te line does not exist, say so
def command5(dbConn):
  dbCursor = dbConn.cursor()
  print()
  #user input
  userColor = input("Enter a line color (e.g. Red or Yellow): ")

  sql = "Select Stop_Name, Direction, ADA FROM Stops JOIN StopDetails ON (Stops.Stop_ID = StopDetails.Stop_ID) JOIN Lines ON (StopDetails.Line_ID = Lines.Line_ID) WHERE UPPER(Color) = UPPER(?) ORDER BY Stop_Name asc"

  dbCursor.execute(sql,[userColor])
  rows = dbCursor.fetchall()

  if not rows:
    print("**No such line...")
    print()
    return
  for row in rows:
    stopName = row[0]
    direction = row[1]
    accessible = row[2]
    #if statement to print ADA outputs
    if not accessible:
      print(stopName, ": direction =", direction, "(accessible? no)")
    print(stopName, ": direction =", direction, "(accessible? yes)")
  print()

#
# command6
#
# outputs total ridership by month, in ascending order by month. After the output, the user is given the option to plot the data:
def command6(dbConn):
  dbCursor = dbConn.cursor()

  print("** ridership by month **")

  sql = "Select strftime('%m',Ride_Date), SUM(Num_Riders) FROM Ridership GROUP BY strftime('%m',Ride_Date) ORDER BY strftime('%m',Ride_Date) ASC"

  dbCursor.execute(sql)
  rows = dbCursor.fetchall()

  for row in rows:
    print(row[0], ":", f"{row[1]:,}")
 #plot the data
  print()  
  plot = input("Plot? (y/n) ")
  print()
  if plot == "y":
    x = []
    y = []
    for row in rows:
      x.append(row[0])
      y.append(row[1]/100000000)
  
    figure.xlabel("month")
    figure.ylabel("number of riders(x * 10^8)")
    figure.title("monthly ridership")

    figure.plot(x,y)
    figure.show()
  
#
# command7
#
#outputs total ridership by year, in ascending order by year. After the output,the user is given the option to plot the data:
def command7(dbConn):
  dbCursor = dbConn.cursor()
  print("** ridership by year **")
  sql = "Select strftime('%Y',Ride_Date), SUM(Num_Riders) FROM Ridership GROUP BY strftime('%Y',Ride_Date) ORDER BY strftime('%Y',Ride_Date) ASC"

  dbCursor.execute(sql)
  rows = dbCursor.fetchall()

  for row in rows:
    print(row[0], ":", f"{row[1]:,}")
  #plotting the data
  print()
  plot = input("Plot? (y/n) \n")

  if plot == "y":
    x = []
    y = []
    for row in rows:
      x.append(row[0]) #year
      y.append(row[1]/100000000) #number of riders

    figure.xlabel("year")
    figure.ylabel("number of riders (x * 10^8)")
    figure.title("yearly ridership")

    figure.plot(x,y)
    figure.show()

#
# command8
#
#input a year and the name of two stations (full or partial names), and then outputs the daily ridership at each station for that year. output the first 5 days and the last 5 days of data for each station
def command8(dbConn):
  dbCursor = dbConn.cursor()
  print()
  year = input("Year to compare against? \n")
  station1 = input("Enter station 1 (wildcards _ and %): ")
  
  sql0 = "Select Station_ID, Station_Name FROM Stations WHERE Station_Name LIKE ?"
  
  dbCursor.execute(sql0,[station1])
  rows = dbCursor.fetchall()
  if not rows:
    print("**No station found...")
    print()
    return
  if len(rows) > 1:
    print("**Multiple stations found...")
    print()
    return
  print()
  station2 = input("Enter station 2 (wildcards _ and %): ")
  sql = "Select DISTINCT date(Ride_Date), Num_Riders from Ridership JOIN Stations ON (Ridership.Station_ID = Stations.Station_ID) WHERE Station_Name LIKE ? AND strftime('%Y', Ride_Date) = ?ORDER BY Ride_Date ASC "

  dbCursor.execute(sql,[station1, year])
  rows2 = dbCursor.fetchall()

  ##Station 2 execution
  dbCursor.execute(sql0,[station2])
  rows3 = dbCursor.fetchall()
  # if not rows:
  #   print("** No station found...")
  #   return
  if not rows3:
    print("**No station found...")
    print()
    return
  if len(rows3) > 1:
    print("**Multiple stations found...")
    print()
    return
  for row in rows:
    print("Station 1:", row[0], row[1])
  
  # for loop to print the first 5 days of data
  for row in rows2[:5]:
    print(row[0], row[1])
  # for loop to print the last 5 days of data
  for row in rows2[-5:]:
    print(row[0], row[1])

  for row in rows3:
    print("Station 2:", row[0], row[1])

  dbCursor.execute(sql,[station2, year])
  
  rows4 = dbCursor.fetchall()
  # for loop to print the first 5 days of data
  for row in rows4[:5]:
    print(row[0], row[1])
  # for loop to print the last 5 days of data
  for row in rows4[-5:]:
    print(row[0], row[1])
  print()
  #plotting the data
  plot = input("Plot? (y/n) \n")
  if plot == "y":
    x = []
    y = []
    z = []
    j = []
    day = 1

    for row in rows2:
      x.append(day)
      y.append(row[1])
      day = day + 1
    
    day = 1
    for row in rows4:
      z.append(day)
      j.append(row[1])
      day = day + 1

    figure.xlabel("day")
    figure.ylabel("number of riders")
    figure.title("riders each day of 2020")

    figure.plot(x,y)
    figure.plot(z,j)
    figure.show()
  
    
#
# command8
#
#input a line color from the user and output all station names that are part of that line, in ascending order.
def command9(dbConn):
  dbCursor = dbConn.cursor()
  print()
  color = input("Enter a line color (e.g. Red or Yellow): ")

  sql = "Select DISTINCT Station_Name, Latitude, Longitude FROM Stops JOIN Stations ON (Stops.Station_ID = Stations.Station_ID) JOIN StopDetails ON (Stops.Stop_ID = StopDetails.Stop_ID) JOIN Lines ON (Lines.Line_ID = StopDetails.Line_ID) WHERE UPPER(Color) =  UPPER(?) ORDER BY Station_Name asc;"
  
  dbCursor.execute(sql,[color])
  rows = dbCursor.fetchall()

  if not rows:
    print("**No such line...")
    print()
    return
  for row in rows:
    stationName = row[0]
    latitude = row[1]
    longitude = row[2]
    print(f"{stationName} : ({latitude}, {longitude})")
  #plotting the data
  print()
  plot = input("Plot? (y/n) \n")
  if plot == "y":
    #
    # populate x and y lists with (x, y) coordinates --- note that longitude
    # are the X values and latitude are the Y values #
    x = []
    y = []
    for row in rows:
      x.append(row[2])
      y.append(row[1])
    image = figure.imread("chicago.png")

    xydims = [-87.9277, -87.5569, 41.7012, 42.0868] 
    figure.imshow(image, extent=xydims)
    # area covered by the map: figure.imshow(image, extent=xydims)
    figure.title(color + " line")
    #
    # color is the value input by user, we can use that to plot the
    # figure *except* we need to map Purple-Express to Purple: #
    if (color.lower() == "purple-express"):
      color="Purple" # color="#800080"

    figure.plot(x, y, "o", c=color)
    #
    # annotate each (x, y) coordinate with its station name: #
    for row in rows:
      figure.annotate(row[0], (row[2], row[1])) 

    figure.xlim([-87.9277, -87.5569])
    figure.ylim([41.7012, 42.0868]) 
    figure.show()
        
###########################################################  
#
# main
#
print('** Welcome to CTA L analysis app **\n')


dbConn = sqlite3.connect('CTA2_L_daily_ridership.db')

print_stats(dbConn)
command = input("Please enter a command (1-9, x to exit): ")

while command != 'x':
  if command == '1':
      command1(dbConn)
  elif command == '2':
    command2(dbConn)
  elif command == '3':
    command3(dbConn)
  elif command == '4':
    command4(dbConn)
  elif command == '5':
    command5(dbConn)
  elif command == '6':
    command6(dbConn)
  elif command == '7':
    command7(dbConn)
  elif command == '8':
    command8(dbConn)
  elif command == '9':
    command9(dbConn)
  else:
    print("**Error, unknown command, try again...")
    print()
  
  command = input("Please enter a command (1-9, x to exit): ")
#print_stats(dbConn)

#
# done
#
