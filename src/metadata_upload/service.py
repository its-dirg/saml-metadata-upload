import os
import random
import string

from flask_transfer.transfer import Transfer
from flask_transfer.validators import AllowedExts
from flask_wtf.file import FileField
from flask_wtf.file import FileRequired, FileAllowed
from flask_wtf.form import Form
from werkzeug.utils import secure_filename
from wtforms.fields.simple import SubmitField

from metadata_upload.validation import SAMLMetadataValidator

ALLOWED_EXTENSIONS = ['xml']


class SAMLMetadataUploadForm(Form):
    uploaded_file = FileField(label='Upload metadata',
                              validators=[
                                  FileRequired(),
                                  FileAllowed(ALLOWED_EXTENSIONS,
                                              'Only SAML Metadata (.xml) allowed.')
                              ])
    submit = SubmitField(label='Upload')


def random_string(n=16):
    return ''.join(
        random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(n))


def save_with_sanitized_filename(filehandle, upload_directory):
    fullpath = os.path.join(upload_directory, secure_filename(filehandle.filename))
    filehandle.save(fullpath)


SAMLMetadataDocuments = AllowedExts(*ALLOWED_EXTENSIONS)
SAMLMetadataUpload = Transfer(validators=[SAMLMetadataDocuments],
                              destination=save_with_sanitized_filename)
SAMLMetadataUpload.validator(SAMLMetadataValidator())
