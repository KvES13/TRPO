from flask import render_template, url_for, request, redirect
from app import app, db
from app.models import Statistics, DFile
from .text_handler.file_reader import FileContent
import os
from werkzeug.utils import secure_filename

uploads_dir = os.path.join(app.root_path, 'uploads')


@app.route('/', methods=['POST', 'GET'])
@app.route('/home', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        file = request.files["file"]
        if file:
            print("POST")
            print(file.filename)
            filename = file.filename
            filepath = os.path.join(uploads_dir, secure_filename(file.filename))
            file.save(filepath)
            dfile = DFile(filename=filename, filepath=filepath)
            try:
                db.session.add(dfile)
                db.session.commit()
                return redirect('/text-analysis')
            except:
                return "При добавлении произошла ошибка"
    else:
        print("GET")
        return render_template("/index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/show-statistics')
def show_statistics():
    stat = Statistics.query.order_by(Statistics.date.desc()).all()
    return render_template("show-statistics.html", stat=stat)


@app.route('/show-statistics/<int:id>')
def show_statistics_detail(id):
    stat = Statistics.query.get(id)
    return render_template("statistics-detail.html", stat=stat)


# # Create a directory in a known location to save files to.
# uploads_dir = os.path.join(app.instance_path, 'uploads')
# # os.makedirs(uploads_dir, exists_ok=True)
# MAX_FILE_SIZE = 1024 * 1024 + 1


@app.route("/text-analysis")
def text_analysis():
    dfile = DFile.query.order_by(DFile.date.desc()).first()
    ftext = FileContent(dfile.filename, dfile.filepath, dfile.date)
    print(ftext.getDate())
    print("  " + ftext.getFPath())
    return render_template("text-analysis.html", ftext=ftext)

