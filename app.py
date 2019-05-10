import os
from flask import Flask, render_template, request


try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract


app = Flask(__name__)


def image_processing(filename):
    """
    Processes the image.
    """
    text = pytesseract.image_to_string(Image.open(filename))
    return text


UPLOAD_FOLDER = '/static/uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def home_page():
    """
    Home page of Application
    """
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', msg='No file selected')
        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', msg='No file selected')
        if file and allowed_file(file.filename):
            file.save(os.path.join(os.getcwd() + UPLOAD_FOLDER, file.filename))

            extracted_text = image_processing(file)

            return render_template('index.html',
                                   msg='Successfully',
                                   extracted_text=extracted_text,
                                   img_src=UPLOAD_FOLDER + file.filename)
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
