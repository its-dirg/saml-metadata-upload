import os

from flask.app import Flask
from flask.helpers import flash
from flask.templating import render_template
from flask_bootstrap import Bootstrap
from flask_transfer.exc import UploadError

from metadata_upload.service import random_string, SAMLMetadataUploadForm, \
    SAMLMetadataUpload

app = Flask(__name__)
app.config['UPLOAD_DIRECTORY'] = os.environ.get('MD_UPLOAD_DIR', 'metadata_uploads')
app.secret_key = os.environ.get('MD_UPLOAD_SECRET', random_string())
Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
def upload():
    form = SAMLMetadataUploadForm()

    if form.validate_on_submit():
        filehandle = form.uploaded_file.data
        try:
            SAMLMetadataUpload.save(filehandle, upload_directory=app.config['UPLOAD_DIRECTORY'])
            flash('Uploaded {}'.format(filehandle.filename), 'success')
        except UploadError as e:
            flash('{}: {}'.format(filehandle.filename, str(e)), 'error')
    elif form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash("Error in the '{}' field - {}".format(getattr(form, field).label.text, error),
                      'error')

    return render_template('upload.html', form=form)


# ensure the upload directory exists
if not os.path.isdir(app.config['UPLOAD_DIRECTORY']):
    os.makedirs(app.config['UPLOAD_DIRECTORY'])
