from flask import render_template, url_for, request, redirect
from app import app, db, models
from datetime import datetime
from .text_handler.file_reader import Analyzer, FileContent, sentence_part
import os
from werkzeug.utils import secure_filename

uploads_dir = os.path.join(app.root_path, 'uploads')
bg_colors = ('bg-primary', 'bg-success', 'bg-warning', 'bg-info', 'bg-dark', 'bg-danger')


@app.route('/', methods=['POST', 'GET'])
@app.route('/home', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        file = request.files["file"]
        if file:
            filename = file.filename
            filepath = os.path.join(uploads_dir, secure_filename(file.filename))

            exists = models.DFile.query.filter_by(filename=filename).first()
            if exists:
                exists.date = datetime.now()
                db.session.commit()
                return redirect('/text-analysis')
            else:
                file.save(filepath)
                dfile = models.DFile(filename=filename, filepath=filepath, date=datetime.now())
                try:
                    db.session.add(dfile)
                    db.session.commit()
                    return redirect('/text-analysis')
                except:
                    return "При добавлении произошла ошибка"
    else:
        return render_template("/index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/show-statistics')
def show_statistics():
    exists = models.DFile.query.first()
    if exists:
        print("ex show")
        files = models.DFile.query.order_by(models.DFile.date.desc()).all()
        print(files)
    else:
        print("net show")
        files = 0
    return render_template("show-statistics.html", files=files)


@app.route('/show-statistics/<int:id>')
def show_statistics_detail(id):
    stat = models.Statistics.query.filter_by(parent_id=id).first()
    dfile = models.DFile.query.get(id)

    # parts = {sentence_part[0]: stat.subject, sentence_part[1]: stat.predicate, sentence_part[2]: stat.addition,
    #          sentence_part[3]: stat.attribute, sentence_part[4]: stat.adverbial_modifier,
    #          sentence_part[5]: stat.unknown}
    values = (stat.subject, stat.predicate, stat.addition, stat.attribute, stat.adverbial_modifier, stat.unknown)
    return render_template("statistics-detail.html", words_count=stat.words_count, sentence_part=sentence_part,
                           dfile=dfile, bg_colors=bg_colors, values=values, lenght=6)


# # Create a directory in a known location to save files to.
# uploads_dir = os.path.join(app.instance_path, 'uploads')
# # os.makedirs(uploads_dir, exists_ok=True)
# MAX_FILE_SIZE = 1024 * 1024 + 1


@app.route("/text-analysis")
def text_analysis():
    dfile = models.DFile.query.order_by(models.DFile.date.desc()).first()
    print("***************************")
    if dfile:
        print(dfile.filename,"  fNAME")
        ftext = FileContent(dfile.filename, dfile.filepath, dfile.date)
        stat = Analyzer(ftext.getFileText())
        exists = models.Statistics.query.filter_by(parent_id=dfile.id).first()
        print(exists, "  exists ")
        if exists:
            print("ex")
        else:
            temp_dict = stat.getDict()
            rec = models.Statistics(parent_id=dfile.id, words_count=stat.words_count,
                                    subject=temp_dict.get(sentence_part[0]), predicate=temp_dict.get(sentence_part[1]),
                                    addition=temp_dict.get(sentence_part[2]), attribute=temp_dict.get(sentence_part[3]),
                                    adverbial_modifier=temp_dict.get(sentence_part[4]),
                                    unknown=temp_dict.get(sentence_part[5]))
            try:
                db.session.add(rec)
                db.session.commit()
            except:
                return "При добавлении произошла ошибка"
    else:
        stat = Analyzer(" ")

    return render_template("text-analysis.html", stat=stat)

