from flask import Flask

app = Flask(__name__)
app.secret_key = 'super secret key'

from flask import render_template, flash, redirect, request
import Controller
from Controller import Controller

links = {
        "encrypt":"/encrypt",
        "decrypt":"/decrypt",
        "deepapiencrypt":"/deepapiencrypt"
}



def index():
    return render_template("index.html" ,links=links)


@app.route('/', methods=['GET', 'POST'])
@app.route('/encrypt', methods=['GET', 'POST'])
def encrypt():
    data = {"post":False, "data":""}
    if request.method == "POST":
        file = request.files['image_for_encrypt']
        if file.filename == '':
            flash('Нет выбранного файла')
            data['data'] = "НЕТ ФАЙЛА"
            return render_template("encrypt.html", links=links, data=data)

        text = request.form.get('text')
        if text == "":
            data['data'] = "НЕТ СТРОКИ ДЛЯ ШИФРОВАНИЯ"
            return render_template("encrypt.html", links=links, data=data)
        
        file.save("static/" + file.filename)
        data['filename']=file.filename
        controller = Controller()
        image = controller.to_encrypt(text, f"static/{data['filename']}")
        image.save(f"static/{data['filename']}")
        data['post'] = True
    return render_template("encrypt.html", links=links, data=data)



@app.route('/decrypt', methods=['GET', 'POST'])
def decrypt():
    data = {"post":False, "error":"", "text":""}
    if request.method == "POST":
        file = request.files['image_for_encrypt']
        if file.filename == '':
            flash('Нет файла')
            data['data'] = "НЕТ ФАЙЛА"
            return render_template("encrypt.html", links=links, data=data)

        file.save("static/" + file.filename)
        data['filename'] = file.filename
        controller = Controller()
        text = controller.to_decrypt(f"static/{data['filename']}")
        data['text'] = text
        data['post'] = True
        if text is None:
            data['error'] = "Не удалось расшифровать изображение"
            data['post'] = False
    return render_template("decrypt.html", links=links, data=data)



@app.route('/deepapiencrypt', methods=['GET', 'POST'])
def deepapiencrypt():
    data = {"post":False, "error":"", "text":""}
    if request.method == "POST":
        data['post'] = True
        text = request.form.get('text')
        theme = request.form.get('theme')
        if theme == "" or text == "":
            data['error'] = "Заполните оба поля"
            data['post'] = False
            return render_template("deepapiencrypt.html", links=links, data=data)
        
        controller = Controller()
        image = controller.to_encrypt_with_generated_image(text, theme)
        data['filename'] = image.filename.split("/")[-1]
    return render_template("deepapiencrypt.html", links=links, data=data)


if __name__ == "__main__":
    app.run(debug=True)
