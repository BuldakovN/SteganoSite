
# A very simple Flask Hello World app for you to get started with...

from flask import Flask

app = Flask(__name__)

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
    data = {"post":False, "data":"пивас"}
    if request.method == "POST":
        data["post"] = True
        image = request.files["image_for_encrypt"]
        image.save("app/static/download_file" + image.filename)
        data['data'] = request.form
        data['filename']="download_file" + image.filename
        controller = Controller()
        controller.to_encrypt("/static")
    return render_template("encrypt.html", links=links, data=data)




if __name__ == "__main__":
    app.run()
