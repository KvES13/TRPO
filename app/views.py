from flask import render_template, request, redirect
from app import app, db, models, db_queries, file_handler, sentence_info as si
from datetime import datetime
import os
from werkzeug.utils import secure_filename


uploads_dir = os.path.join(app.root_path, 'uploads')
bg_colors = ('bg-info','bg-primary', 'bg-success', 'bg-warning', 'bg-info', 'bg-dark', 'bg-danger')


@app.route('/', methods=['POST', 'GET'])
@app.route('/home', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        file = request.files["file"]
        if file:
            file_format = file_handler.allowed_file(file.filename)
            if file_format == 'undef':
                return render_template("/index.html", error="Формат данного файла не поддерживается")
            else:
                filename = file.filename
                filepath = os.path.join(uploads_dir, secure_filename(file.filename))
                exists = models.Files.query.filter_by(filename=filename).first()
                if exists:
                    exists.date = datetime.now()
                    db.session.commit()
                    return redirect('/text-analysis')
                else:
                    file.save(filepath)
                    dfile = models.Files(filename=filename, filepath=filepath, date=datetime.now())
                    # try:
                    db.session.add(dfile)
                    db.session.commit()
                    analyzer = file_handler.Analyzer(dfile.id)
                    print(file_format,"  ",filepath)
                    print(file_handler.read_from_file(file_format, filepath))
                    analyzer.ultra_mega_algo(file_handler.read_from_file(filepath, file_format))
                    return redirect('/text-analysis')
                    # except:
                    # return render_template("/index.html", error="При добавлени записи произошла ошибка")

    else:
        return render_template("/index.html", error=0)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/show-statistics')
def show_statistics():
    exists = models.Files.query.first()
    files = 0
    if exists:
        files = models.Files.query.order_by(models.Files.date.desc()).all()

    return render_template("show-statistics.html", files=files)


@app.route('/show-statistics/<int:id>')
def show_statistics_detail(id):
    stat = db_queries.get_file_stat(id)
    dfile = db_queries.get_file_info(id)

    # parts = {sentence_part[0]: stat.subject, sentence_part[1]: stat.predicate, sentence_part[2]: stat.addition,
    #          sentence_part[3]: stat.attribute, sentence_part[4]: stat.adverbial_modifier,
    #          sentence_part[5]: stat.unknown}
    values = (stat.words_count, stat.subject, stat.predicate, stat.addition, stat.attribute, stat.adverbial_modifier, stat.unknown)
    return render_template("statistics-detail.html", sentence_part=si.parts,
                           dfile=dfile, bg_colors=bg_colors, values=values)


@app.route("/text-analysis", methods=['POST', 'GET'])
def text_analysis():
    dfile = models.Files.query.order_by(models.Files.date.desc()).first()
    text = ""
    cb_values = (0, "")
    if dfile:
        if request.method == 'POST':
            word = request.form.get('word')
            role = request.form.get('role')
            role_index = si.parts.index(role)
            text = db_queries.get_sentences(dfile.id,role_index, word)
            cb_values = (role_index, word)
        else:
            text = db_queries.get_sentences(dfile.id, si.SParts.all, "")
        record = db_queries.get_file_stat(dfile.id)
        values = (record.words_count,record.subject, record.predicate, record.addition, record.attribute,
                  record.adverbial_modifier, record.unknown)

        return render_template("text-analysis.html", values=values, text=text,
                               sentence_part=si.parts,cb_values=cb_values)
    else:

        values = (0, 0, 0, 0, 0, 0, 0)

        return render_template("text-analysis.html", values=values, text=text,
                               sentence_part=si.parts, cb_values=cb_values)

