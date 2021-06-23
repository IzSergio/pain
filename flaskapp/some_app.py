print("Hello world")
from flask import Flask
app = Flask(__name__)
#декоратор для вывода страницы по умолчанию
@app.route("/")
def hello():
 return '<html><head></head> <body> Hello World! <br> We have <br> <a href="/iz">My individual task</a> </body></html>'
if __name__ == "__main__":
 app.run(host='127.0.0.1',port=5000)
from flask import render_template


# модули работы с формами и полями в формах
from flask_wtf import FlaskForm,RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField, DecimalField
# модули валидации полей формы
from wtforms.validators import DataRequired, InputRequired, NumberRange
from flask_wtf.file import FileField, FileAllowed, FileRequired
# используем csrf токен, можете генерировать его сами
SECRET_KEY = 'secret'
app.config['SECRET_KEY'] = SECRET_KEY
# используем капчу и полученные секретные ключи с сайта google 
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LePmPcaAAAAAKXAXLkMwCeyDvMBnrSgbNKJySUa'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LePmPcaAAAAAPXIblJMnnmnzRcYtu6fLluxlYHg'
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}
# обязательно добавить для работы со стандартными шаблонами
from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)
# создаем форму для загрузки файла

class ContrastForm(FlaskForm):
 # поле для введения строки, валидируется наличием данных
 # валидатор проверяет введение данных после нажатия кнопки submit
 # и указывает пользователю ввести данные если они не введены
 # или неверны
 number = DecimalField('Contrast value', validators=[InputRequired(),NumberRange(min=0,max=100,message='Please give a value between 0 and 100')])
 # поле загрузки файла
 # здесь валидатор укажет ввести правильные файлы
 upload = FileField('Load image', validators=[ FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
 # поле формы с капчей
 recaptcha = RecaptchaField()
 #кнопка submit, для пользователя отображена как send
 submit = SubmitField('send')

 
import base64
from PIL import Image
from io import BytesIO
# модуль проверки и преобразование имени файла
# для устранения в имени символов типа / и т.д.
from werkzeug.utils import secure_filename
import os
from iz import makegraphs
# подключаем наш модуль и переименовываем
# для исключения конфликта имен
# метод обработки запроса GET и POST от клиента
@app.route("/iz",methods=['GET', 'POST'])
def iz():
 # создаем объект формы
 form = ContrastForm()
 # обнуляем переменные передаваемые в форму
 filenames = []
 # проверяем нажатие сабмит и валидацию введенных данных
 if form.validate_on_submit():
  print('dir before: {}'.format(os.listdir('./static/img/')))
  for f in os.listdir('./static/img/'): #
   os.remove('./static/img/'+f) # 
  # файлы с изображениями читаются из каталога src
  filename = os.path.join('./static/img/', secure_filename(form.upload.data.filename)) #не нужно
  # сохраняем загруженный файл
  form.upload.data.save(filename)
  print('Saved as {}'.format(filename))
  print('dir: {}'.format(os.listdir('./static/img/')))
  fimage = Image.open(filename)
  print('Value: {}'.format(form.number.data))
  # передать загруженный файл
  filenames = makegraphs(fimage,form.number.data)
  print('dir after: {}'.format(os.listdir('./static/img/')))
 # передаем форму в шаблон
 # если был нажат сабмит, либо передадим falsy значения
 return render_template('iz.html',form=form,image_res=filenames)

from flask import request
from flask import Response
import json
# метод для обработки запроса от пользователя
@app.route("/apiiz",methods=['GET', 'POST'])
def apinet():
 result = {}
 # проверяем что в запросе json данные
 if request.mimetype == 'application/json': 
  # получаем json данные
  data = request.get_json()
  # берем содержимое по ключу, где хранится файл
  # закодированный строкой base64
  # декодируем строку в массив байт, используя кодировку utf-8
  # первые 128 байт ascii и utf-8 совпадают, потому можно
  filebytes = data['imagebin'].encode('utf-8')
  # декодируем массив байт base64 в исходный файл изображение
  cfile = base64.b64decode(filebytes)
  # чтобы считать изображение как файл из памяти используем BytesIO
  img = Image.open(BytesIO(cfile))
  #img.filename = 'orig.jpg'
  nums = base64.b64decode(data['contrast'])
  result = makegraphs(img,nums)
  # пример сохранения переданного файла
  # handle = open('./static/f.png','wb')
  # handle.write(cfile)
  # handle.close()
 # преобразуем словарь в json строку
 ret = json.dumps(result)
 # готовим ответ пользователю
 resp = Response(response=ret,
                 status=200,
                 mimetype="application/json")
 # возвращаем ответ
 return resp 

@app.route("/dir",methods=['GET', 'POST'])
def speak():
 res = []
 if request.mimetype == 'path':
  try:
   res=os.listdir(request.get_data)
  except:
   res=['No dir']
 return tuple(res)
