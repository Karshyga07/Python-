import csv
with open('people.csv', 'w', newline = '', encoding = 'utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['name', 'surname', 'phone'])
    writer.writerow(['Aruzhan', 'Aitkali', '87012345678'])
    writer.writerow(['Dias', 'Aitkali', '87012345678'])
    writer.writerow(['Assem', 'Aitkali', '87012345678'])
   
   
