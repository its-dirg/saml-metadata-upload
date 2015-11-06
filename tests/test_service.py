import os
from io import BytesIO

import pytest

import upload_service.wsgi


class TestFileUploadService():
    @pytest.fixture(autouse=True)
    def create_flask_test_client(self, tmpdir):
        self.app = upload_service.wsgi.app
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['TESTING'] = True
        self.app.config['UPLOAD_DIRECTORY'] = tmpdir.strpath

    def test_renders_upload_page(self):
        html_page = self.response_content(self.app.test_client().get('/upload'))
        assert 'enctype="multipart/form-data"' in html_page
        assert 'type=\"file\"' in html_page
        assert 'Upload' in html_page

    def test_stores_correct_file_upload(self):
        uploaded_filename = 'idp.xml'
        xml_path = os.path.join(os.path.dirname(__file__), 'idp.xml')
        with open(xml_path, 'rb') as f:
            self.post_to_upload_endpoint(f, uploaded_filename)

        upload_path = os.path.join(self.app.config['UPLOAD_DIRECTORY'], uploaded_filename)
        with open(xml_path, 'r') as expected, open(upload_path, 'r') as actual:
            assert actual.read() == expected.read()

    def test_shows_success_message_for_correct_file_upload(self):
        filename = 'idp.xml'
        xml_path = os.path.join(os.path.dirname(__file__), filename)
        with open(xml_path, 'rb') as f:
            resp = self.post_to_upload_endpoint(f, filename)

        assert 'success' in self.response_content(resp)

    def test_rejects_incorrect_xml(self):
        non_saml_xml = """<?xml version='1.0' encoding='UTF-8'?>
        <note>
        <to>Tove</to>
        <from>Jani</from>
        <heading>Reminder</heading>
        <body>Don't forget me this weekend!</body>
        </note>"""

        resp = self.post_to_upload_endpoint(BytesIO(non_saml_xml.encode('utf-8')), 'test.xml')

        assert resp.status_code == 200
        assert 'Invalid' in self.response_content(resp)

    @pytest.mark.parametrize("file_ext", [
        'txt',
        'rst',
        'pdf',
    ])
    def test_rejects_wrong_file_extension_with_error_message(self, file_ext):
        resp = self.post_to_upload_endpoint(BytesIO(), 'data.{}'.format(file_ext))
        assert 'Only SAML Metadata (.xml) allowed.' in self.response_content(resp)

    def test_rejects_wrong_file_type_with_error_message(self):
        resp = self.post_to_upload_endpoint(BytesIO('just some plain text'.encode('utf-8')),
                                            'data.xml')
        assert 'Invalid SAML metadata.' in self.response_content(resp)

    def test_rejects_empty_POST(self):
        resp = self.app.test_client().post('/upload')
        assert 'Error in the &#39;Upload metadata&#39; field - This field is required.' in self.response_content(
            resp)

    def test_sanitizes_filename_before_storing_upload(self):
        uploaded_filename = 'idp.xml'

        xml_path = os.path.join(os.path.dirname(__file__), 'idp.xml')
        with open(xml_path, 'rb') as f:
            self.post_to_upload_endpoint(f, '../../{}'.format(uploaded_filename))

        upload_path = os.path.join(self.app.config['UPLOAD_DIRECTORY'], uploaded_filename)
        with open(xml_path, 'r') as expected, open(upload_path, 'r') as actual:
            assert actual.read() == expected.read()

    def test_creates_upload_directory_if_necessary(self):
        assert os.path.isdir(self.app.config['UPLOAD_DIRECTORY'])

    def response_content(self, response):
        return response.data.decode('utf-8')

    def post_to_upload_endpoint(self, filedata, filename):
        return self.app.test_client().post('/upload', data={'uploaded_file': (filedata, filename)})
