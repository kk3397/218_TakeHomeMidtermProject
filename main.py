from flask import Flask, render_template, request

import os
from datetime import datetime

app = Flask(__name__)

#default page
@app.route('/')
def upload():
    return render_template("index.html")

# a function to get various metadata of the passed image
def get_image_metadata(image_path):
    sucess="Upload Successful!"
    # Get the file extension
    _, extension = os.path.splitext(image_path)

    # List of image file extensions
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg']
    if extension.lower() in image_extensions:
        file_name = os.path.basename(image_path)
        file_size = os.stat(image_path)
        upload_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        data = [{'Name':file_name}, {'Size in bytes': file_size.st_size}, {"Time of Upload": upload_time}]
        return str(data)
    else:

        return "Invalid file type. Try again!"

#when the images gets uploaded it will transition to a new page for the metadata
@app.route('/metadata', methods=['GET', 'POST'])
def metadata():
    if request.method == 'POST':
        if 'image_file' in request.files:
            image_file = request.files['image_file']

            if image_file.filename != '' :
                image_path = image_file.filename
                image_file.save(image_path)
                #calls metadata function
                data = get_image_metadata(image_path)
            else:
                return "no files chosen"
    #renders the instructed html page while passing the data for metadata
    return render_template("metadata.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)
