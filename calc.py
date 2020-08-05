from datetime import datetime

data = '990801401668'

bday = f'20{data[0:2]}-{data[2:4]}-{data[4:6]}'
gender = data[6]

bday_date = datetime.strptime(bday, '%Y-%m-%d').date()
curr_date = datetime.now().date()

if curr_date < bday_date:
    bday = f'19{data[0:2]}-{data[2:4]}-{data[4:6]}'

datetime.strptime(bday, '%Y-%m-%d').date()

iin_data = {'gender': gender, 'date_of_birth': bday}

print(iin_data)