from flask import Flask, render_template, request, send_file
import tempfile
from utils import transferStyleInAToB
from io import BytesIO
import numpy as np

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def uploadForm():
    temp_dir = tempfile.TemporaryDirectory()
    
    if request.method == 'POST':
        print(request.files.keys)
        from_image = request.files['originalImageInput']
        to_image = request.files['targetImageInput']

        if from_image.filename != '' and to_image.filename != '':

            from_file_stream = BytesIO(from_image.read())
            from_file_stream.seek(0)
            from_file_bytes = np.asarray(bytearray(from_file_stream.read()), dtype=np.uint8)

            to_file_stream = BytesIO(to_image.read())
            to_file_stream.seek(0)
            to_file_bytes = np.asarray(bytearray(to_file_stream.read()), dtype=np.uint8)

            file_path = transferStyleInAToB(from_file_bytes, to_file_bytes, temp_dir.name)
            return send_file(file_path, as_attachment=True, mimetype='image/jpg', download_name=f"download.jpg");

    return render_template('index.html')

if __name__ == '__main__':
    app.run()