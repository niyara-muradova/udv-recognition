import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from recog import photo_recog
from datetime import datetime

import logging

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# allowed file types of photos
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_data_udv(data):
    # need improvement
    IDKAZ = 5
    num_len = 10
    iin_len = 12

    all_data = {}

    name_surname = data.splitlines()[2]

    split = name_surname.split('<<')

    surname = split[0]
    name = split[1][0:split[1].find('<')]
    doc_num = data[IDKAZ:IDKAZ + num_len]
    iin = data[IDKAZ + num_len:iin_len + IDKAZ + num_len]

    datas = calculate_iin(iin)


    print(surname)
    print(name)
    print(iin)
    print(doc_num)
    print(datas)

def calculate_iin(data):
    if len(data) == 12:
        c_dig = control_digit(data)
        if c_dig == int(data[-1]):
            iin_data = iin_info(data)
        else:
            iin_data = {'gender': None, 'date_of_birth': None, 'additional': '[Ошибка контрольного разряда]'}
    else:
        iin_data = {'gender': None, 'date_of_birth': None, 'additional': '[Несоответствие формата ИИН]'}

    return iin_data


def control_digit(data):
    data_list = list(data)

    weight = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    c_digit = 0

    for i in range(11):
        mult = weight[i] * int(data_list[i])
        c_digit += mult

    c_digit = c_digit % 11

    return c_digit


def iin_info(data):
    additional = ''

    bday = f'20{data[0:2]}-{data[2:4]}-{data[4:6]}'
    gender = data[6]

    bday_date = datetime.strptime(bday, '%Y-%m-%d').date()
    curr_date = datetime.now().date()

    if curr_date < bday_date:
        bday = f'19{data[0:2]}-{data[2:4]}-{data[4:6]}'

    datetime.strptime(bday, '%Y-%m-%d').date()

    iin_data = {'gender': gender, 'date_of_birth': bday, 'additional': additional}

    return iin_data


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            file.save(os.path.join(f'{app.config["UPLOAD_FOLDER"]}/', filename))

            doc = photo_recog(filename)
            get_data_udv(doc)

            return redirect(url_for('upload_file', filename=filename))
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
