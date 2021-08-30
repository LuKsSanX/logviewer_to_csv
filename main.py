import re
import csv
import os
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

in_file_path: str = filedialog.askopenfilename(title='Open',
                                               initialdir=os.environ['HOME'],
                                               filetypes=[('LogViewer logs', '.log')])

out_file_path = f"{in_file_path.split('.')[0]}.csv"

if out_file_path in os.listdir():
    os.remove(out_file_path)

with open(file=in_file_path, mode='r') as in_file:
    print(f'opening {in_file_path}')
    with open(file=out_file_path, mode='w', newline='') as out_file:
        writer = csv.writer(out_file,
                            delimiter=';')

        writer.writerow(['date', 'time', 'scope', 'error'])
        row = ''

        for line in in_file.readlines():
            line = line.replace('\n', '')

            date = re.search(r'\[\d{4}-\d{2}-\d{2}\s', line)
            time = re.search(r'\d{2}:\d{2}:\d{2}]\s', line)
            scope = re.search(r'\w*\.\w*:\s', line)

            if not (date or scope or time):
                row[-1] += line
                continue

            if row:
                writer.writerow(row)

            row = ['' for i in range(4)]

            row[3] = line

            date = date.group()
            row[0] = date[1:-1]

            time = time.group()
            row[1] = time[:-2]

            scope = scope.group()
            row[2] = scope[:-2]

            row[3] = str(row[3]).replace(date + time + scope, '')

print(f'saved on {out_file_path}')
