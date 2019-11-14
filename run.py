from flask import Flask, render_template, redirect, request, url_for, send_from_directory
import os
import PyPDF2
from fpdf import FPDF
import csv
import requests
import zipfile
import random

app = Flask(__name__)

@app.route("/")
def index():
    
    return render_template("index.html") 

app.config["IMAGE_UPLOADS"] = "C:/Users/ARPIT/projects/pdf_invites/all_pdf"

@app.route("/upload", methods=["GET","POST"])
def upload():
    if request.method == "POST":
        if request.files:
            myFile = request.files["myFile"]
            myFile.save(os.path.join(app.config["IMAGE_UPLOADS"], myFile.filename ))
            print("upload success")
            return redirect(url_for('name'))
            # return redirect(request.url)
    return render_template("file.html")
@app.route("/name", methods=["GET","POST"])
def name():
    if request.method == "POST" and request.files:
        x = int(request.form["x"])
        y = int(request.form["y"])
    
        csvfile = request.files["csvfile"]
        csvfile.save(os.path.join(app.config["IMAGE_UPLOADS"], csvfile.filename ))
        print("upload success")
        
        with open('all_pdf/name.csv', mode='r') as name:
            csv_reader = csv.DictReader(name)
            for row in csv_reader:
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.cell(x, y, txt=row["name"], ln=1, align="C")
                pdf.output("result/"+row["name"]+".pdf")
                input_file = "all_pdf/nidhi_weds_rohan.pdf"
                output_file = "final/"+row["name"]+"_final.pdf"
                watermark_file = "result/"+row["name"]+".pdf"

                with open(input_file, "rb") as filehandle_input:
                    # read content of the original file
                    pdf = PyPDF2.PdfFileReader(filehandle_input)

                    with open(watermark_file, "rb") as filehandle_watermark:
                        # read content of the watermark
                        watermark = PyPDF2.PdfFileReader(filehandle_watermark)
            
                        # get first page of the original PDF
                        first_page = pdf.getPage(0)
            
                        # get first page of the watermark PDF
                        first_page_watermark = watermark.getPage(0)
            
                        # merge the two pages
                        first_page.mergePage(first_page_watermark)
            
                        # create a pdf writer object for the output file
                        pdf_writer = PyPDF2.PdfFileWriter()
            
                        # add page
                        pdf_writer.addPage(first_page)
            
                        with open(output_file, "wb") as filehandle_output:
                            # write the watermarked file to the new file
                            pdf_writer.write(filehandle_output)
        def zipdir(path, ziph):
        # ziph is zipfile handle
            for root, dirs, files in os.walk(path):
                for file in files:
                    ziph.write(os.path.join(root, file))
        zipf = zipfile.ZipFile('pdf_invites.zip', 'w', zipfile.ZIP_DEFLATED)
        zipdir('final/', zipf)
        zipf.close()
        return render_template("download.html")
    return render_template("xy.html")

app.config["show_file"] = "C:/Users/ARPIT/projects/pdf_invites/all_pdf"
app.config["zip_file"] = "C:/Users/ARPIT/projects/pdf_invites"

@app.route('/download/<zip_name>')
def download(zip_name):
    
    try:
        return send_from_directory(
            app.config["zip_file"], filename=zip_name, as_attachment=True
        )
    except FileNotFoundError:
        abort(404)
@app.route('/show/<file_name>')
def show(file_name):
    try:
        return send_from_directory(
            app.config["show_file"], filename=file_name, as_attachment=False
        )
    except FileNotFoundError:
        abort(404)

@app.route('/aaa')
def aaa():
    return render_template('download.html')

if __name__ == "__main__": 
    app.run(debug=True)