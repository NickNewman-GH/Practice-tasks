import warnings
import numpy as np
import ionex

print("Enter the last 2 digits of the year and number of day (For example 15 77 means 77-th day (18-th of march) of 2015 year)")
data=input()
data=data.split()
year, day = int(data[0]), int(data[1])
print("Enter the top left and bottom right corner of the area (x1 y1 x2 y2) without any symbols. Each coordinate in number form")
data=input()
data=data.split()
x1, y1, x2, y2=int(data[0]), int(data[1]), int(data[2]), int(data[3])
if x1 > 73:
    x1 = 73
elif x1 < 0:
    x1 = 0
if x2 > 73:
    x2 = 73
elif x2 < 0:
    x2 = 0
if y1 > 71:
    y1 = 71
elif y1 < 0:
    y1 = 0
if y2 > 71:
    y2 = 71
elif y2 < 0:
    y2 = 0

print("Your coordinates: [",(x1*5)-180,"; ",87.5-(y1*2.5),"], [", (x2*5)-180,"; ",87.5-(y2*2.5),"]")
print("Enter the difference сoefficient (it means how many times storm's TEC must be more then normal TEC)")
ratio=int(input())
start_pos=73*y1+x1
length=abs(x2-x1)
height=abs(y1-y2)

mass=[0]*height
mediana=[0]*height
for i in range(height):
    mass[i]=[0]*length
    mediana[i]=[0]*length

days=1
for i in range(days):
        today=int(day-i-1)
        try:
            with open("ckmg0"+str(today)+"0."+str(year)+"i") as file:
                inx = ionex.reader(file)
                for ionex_map in inx:
                    for i in range(height):
                       for j in range(length):
                           mediana[i][j]=mediana[i][j]+int(ionex_map.tec[start_pos+j+i*73]*10)
        except:
            print("day doesn't exist")

for i in range(height):
    for j in range(length):
        mediana[i][j]=int(mediana[i][j]/(days*25))
        print(mediana[i][j], end=" ")
    print()

output=open("output.txt","w")
output.write("Date \n")
output.write("TEC of area  |  difference between area's TEC and area's mediana  |  coordinates of area \n \n")

with open("ckmg0"+str(day)+"0."+str(year)+"i") as file:
            inx = ionex.reader(file)
            for ionex_map in inx:
                check=False
                output.write(str(ionex_map.epoch)+"\n")
                for i in range(height):
                    for j in range(length):
                        mass[i][j]=int(ionex_map.tec[start_pos+j+i*73]*10)
                        if mass[i][j]>mediana[i][j]*ratio:
                            output.write(str(mass[i][j])+"  "+str(abs(mass[i][j]-mediana[i][j]))+"\t ["+str(((x1+i)*5)-180)+"; "+str(87.5-((y1+j)*2.5))+"] \n")
                            check=True
                if check==True:
                    output.write("\n")
output.close()
