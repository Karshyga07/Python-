import csv
with open('people.csv', 'w', newline = '', encoding = 'utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['name', 'surname', 'phone'])
    writer.writerow(['Bayan', 'Rahmetbay', '8701782978'])
    writer.writerow(['Samat', 'Serik', '870127898978'])
    writer.writerow(['Dana', 'Palenshiev', '87052755678'])
   
   
