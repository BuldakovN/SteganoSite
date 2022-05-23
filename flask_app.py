from flask import Flask

app = Flask(__name__)
app.secret_key = 'super secret key'

from flask import render_template, flash, redirect, request
import Controller
from Controller import Controller

links = {
        "encrypt":"/encrypt",
        "decrypt":"/decrypt",
        "deepapiencrypt":"/deepapidecrypt"
}

@app.route('/')
@app.route('/index')
def index():
    return render_template("base.html" ,links=links)


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




if __name__ == "__main__":
    app.run(debug=True)
