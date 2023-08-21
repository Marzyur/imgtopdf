from PIL import Image
from flask import request,jsonify,Flask, send_file
import img2pdf
import io


app=Flask(__name__)


@app.route('/convert',methods=['POST'])
def convert():
    if 'image' not in request.files:
        return jsonify({'error':'No image file was uploaded'}),400
    image_file=request.files['image']

    if not is_valid_image(image_file):
        return jsonify({'error':'Invalid image file'}),400
    pdf_files=convert_to_pdf(image_file)

    return send_file(
        io.BytesIO(pdf_files),
        mimetype='application/pdf',
        attachment_filename='converted.pdf',
        as_attachment=True
    )
def is_valid_image(image_file):
    try:
        img=Image.open(image_file)

        supported_formats=['JPEG','PNG','BMP','GIF']
        if img.format not in supported_formats:
            return False
        
        max_width=5000
        max_height=5000

        if img.width>max_width or img.height>max_height:
            return False
        
        return True
    except:
        return False
def convert_to_pdf(image_file):
    image_bytes=image_file.read()

    pdf_byte=img2pdf.convert(image_bytes)

    return pdf_byte

if __name__=="__main__":
    app.run(debug=True)
        