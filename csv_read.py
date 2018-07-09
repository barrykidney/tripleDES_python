import csv


def read_csv(filename):

    file = open(filename, "r")
    reader = csv.reader(file)
    x=[]
    for r in reader:
        for s in r:
            x.append(s)
    return x


print(read_csv("files/pc_1.csv"))