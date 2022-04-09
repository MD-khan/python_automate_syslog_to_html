#!/usr/bin/env python3

"""This is the main file. And this is my work"""

import re
import csv
import operator

file = open("syslog.log")
lines = file.readlines()
file.close

per_user = {}
error_detais = {}

for line in lines:
    result = re.search(
        r"ticky: (ERROR|INFO) ([\w ]*) [\[\]#\d\s]*\((\w*)", line)
    if result is not None:
        # Count the Error frequency
        if result.group(1) == "ERROR":  # result[1] - ERROR, INFO
            # result[2] is message
            if result.group(2) not in error_detais.keys():
                error_detais[result.group(2)] = 0
            error_detais[result.group(2)] += 1

        if result.group(3) not in per_user.keys():  # result[3] - user name
            per_user[result.group(3)]["INFO"] = 0
            per_user[result.group(3)]["ERROR"] = 0

        if result.group(1) == "ERROR":
            per_user[result.group(3)]["ERROR"] += 1
        elif result.group(1) == "INFO":
            per_user[result.group(3)]["INFO"] += 1

# print(per_user)
error_detais = sorted(error_detais.items(),
                      key=operator.itemgetter(1), reverse=True)

with open("error_message.csv", "w") as file:
    write = csv.writer(file)
    write.writerow(["Error", "Count"])
    write.writerows(error_detais)
file.close()

per_user = sorted(per_user.items())
with open("user_statistics.csv", 'w') as f:
    writer = csv.writer(f)
    writer.writerow(["Username", "INFO", "ERROR"])
    for line in per_user: 
        writer.writerow([line[0], line[1]["INFO"], line[1]["ERROR"]])
f.close()
