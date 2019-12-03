from flask import Flask, render_template, redirect, request, url_for, send_from_directory
import os
import shutil
import PyPDF2
from fpdf import FPDF
import csv
import requests
import zipfile
import random
import json
import time
from progressbar import ProgressBar
pbar = ProgressBar()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html") 

app.config["IMAGE_UPLOADS"] = "C:/Users/ARPIT/projects/pdf_invites"

@app.route("/upload", methods=["GET","POST"])
def upload():
    if request.method == "POST":
        if request.files:
            myFile = request.files["myFile"]
            myFile.save(os.path.join(app.config["IMAGE_UPLOADS"] + "/Orignal_pdf", myFile.filename ))
            print("upload success")
            pdf_name = myFile.filename
            return redirect(url_for('view', pdf_name=pdf_name))
    return render_template("file.html")

@app.route("/view/<string:pdf_name>", methods=["GET","POST"])
def view(pdf_name):

    if request.method == "POST":
        req = request.values
        x = int(req["x"])
        y = int(req["y"])

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(x) #left align settting
        pdf.cell(x, y, txt="sample text", ln=1, align="C")
        pdf.output("Watermark_pdf/water.pdf")

        input_file = "Orignal_pdf/" + pdf_name
        watermark_file = "Watermark_pdf/water.pdf"

        output_file = "static/pdf/sample.pdf"
    
        with open(input_file, "rb") as filehandle_input:
            pdf = PyPDF2.PdfFileReader(filehandle_input)
            with open(watermark_file, "rb") as filehandle_watermark:
                watermark = PyPDF2.PdfFileReader(filehandle_watermark)
                total_input = pdf.getNumPages()
                first_page_watermark = watermark.getPage(0)
                for i in range(0,total_input):
                    pdf.getPage(i).mergePage(first_page_watermark)
                
                pdf_writer = PyPDF2.PdfFileWriter()
                
                for i in range(0,total_input):
                    pdf_writer.addPage(pdf.getPage(i))

                with open(output_file, "wb") as filehandle_output:
                    pdf_writer.write(filehandle_output)
        return render_template("pdf.html",pdf_name=pdf_name,x=x,y=y)
    return render_template("pdf.html")

@app.route("/name/<string:pdf_name>", methods=["GET","POST"])
def name(pdf_name):
    
    sample_list = []
    if request.method == "POST" and request.files:
        req = request.values
        x = int(req["x"])
        y = int(req["y"])
        zipname = req["zipname"]
        csvfile = request.files["csvfile"]
        csv_name = csvfile.filename
        csvfile.save(os.path.join(app.config["IMAGE_UPLOADS"] + "/CSV_Files", csv_name ))
        print("upload success")
        
        with open('CSV_Files/'+csv_name, mode='r') as name:
            csv_reader = csv.DictReader(name)
            csv_reader = list(csv_reader)
            print(len(csv_reader))
            print(type(csv_reader))
            count = 0
            for row in pbar(csv_reader):
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.cell(x) #left align settting
                pdf.cell(x, y, txt=" ", ln=1, align="C")
                pdf.output("Watermark_pdf/"+row["name"]+".pdf")

                input_file = "Orignal_pdf/" + pdf_name
                watermark_file = "Watermark_pdf/"+row["name"]+".pdf"
                
                mk_path = app.config["IMAGE_UPLOADS"] + "/Result_of_pdf"

                if row["name"] == 'LOT 1':
                    os.mkdir(mk_path)
                    os.mkdir(mk_path + "/lot1")
                    out = "Result_of_pdf/lot1/"
                elif row["name"] == 'LOT 2':
                    os.mkdir(mk_path + "/lot2")
                    out = "Result_of_pdf/lot2/"
                elif row["name"] == 'LOT 3':
                    os.mkdir(mk_path + "/lot3")
                    out = "Result_of_pdf/lot3/"
                elif row["name"] == 'LOT 4':
                    os.mkdir(mk_path + "/lot4")
                    out = "Result_of_pdf/lot4/"
                elif row["name"] == 'LOT 5':
                    os.mkdir(mk_path + "/lot5")
                    out = "Result_of_pdf/lot5/"
                elif row["name"] == 'LOT 6':
                    os.mkdir(mk_path + "/lot6")
                    out = "Result_of_pdf/lot6/"
                elif row["name"] == 'LOT 7':
                    os.mkdir(mk_path + "/lot7")
                    out = "Result_of_pdf/lot7/"

                name = row["name"] #.replace(" ","_")
                if len(sample_list) == 0:
                    sample_list.append(name+".pdf")

                output = out+name+".pdf"
                output_file = output


                with open(input_file, "rb") as filehandle_input:
                    # read content of the original file
                    pdf = PyPDF2.PdfFileReader(filehandle_input)
                    
                    with open(watermark_file, "rb") as filehandle_watermark:
                        # read content of the watermark
                        watermark = PyPDF2.PdfFileReader(filehandle_watermark)
                        # total_water = watermark.getNumPages()
                        total_input = pdf.getNumPages()
                        
                        # get first page of the original PDF
                        first_page_watermark = watermark.getPage(0)

                        for i in range(0,total_input):
                            pdf.getPage(i).mergePage(first_page_watermark)
                            
                        pdf_writer = PyPDF2.PdfFileWriter()

                        for i in range(0,total_input):
                            pdf_writer.addPage(pdf.getPage(i))

                        with open(output_file, "wb") as filehandle_output:
                            # write the watermarked file to the new file
                            pdf_writer.write(filehandle_output)
                
                count = int(count + 1)
        def zipdir(path, ziph):
        # ziph is zipfile handle
            for root, dirs, files in os.walk(path):
                for file in files:
                    ziph.write(os.path.join(root, file))
        zipf = zipfile.ZipFile(zipname+'.zip', 'w', zipfile.ZIP_DEFLATED)
        zipdir('Result_of_pdf/', zipf)
        zipf.close()
        sample = sample_list[0]
        print(sample)
        return render_template("download.html")
    return render_template("xy.html")

app.config["show_file"] = "C:/Users/ARPIT/projects/pdf_invites/Result_of_pdf/lot1"
app.config["zip_file"] = "C:/Users/ARPIT/projects/pdf_invites"

@app.route('/name/download/<zip_name>')
def download(zip_name):
    
    try:
        return send_from_directory(
            app.config["zip_file"], filename=zip_name, as_attachment=True
        )
    except FileNotFoundError:
        abort(404)
@app.route('/name/show/<file_name>')
def show(file_name):
    try:
        return send_from_directory(
            app.config["show_file"], filename=file_name, as_attachment=False
        )
    except FileNotFoundError:
        abort(404)

@app.route('/name/delete')
def delete():
    delete_path = app.config["IMAGE_UPLOADS"] + "/Result_of_pdf"
    shutil.rmtree(delete_path)
    return render_template('download.html')

if __name__ == "__main__": 
    app.run(use_reloader = True,debug=True)