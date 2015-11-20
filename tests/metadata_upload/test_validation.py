import os
from io import BytesIO

import pytest
from flask_transfer.exc import UploadError

from metadata_upload.validation import SAMLMetadataValidator


class TestSAMLMetadataValidator():
    @pytest.fixture(autouse=True)
    def create_validator(self):
        self.validator = SAMLMetadataValidator()

    def test_accepts_valid_SAML_metadata(self):
        xml_path = os.path.join(os.path.dirname(__file__), 'idp.xml')
        with open(xml_path, 'rb') as xmldata:
            assert self.validator(xmldata)

    def test_rejects_invalid_xml(self):
        non_saml_xml = """<?xml version='1.0' encoding='UTF-8'?>
        <note>
        <to>Tove</to>
        <from>Jani</from>
        <heading>Reminder</heading>
        <body>Don't forget me this weekend!</body>
        </note>"""

        xmldata = BytesIO(non_saml_xml.encode('utf-8'))
        with pytest.raises(UploadError):
            self.validator(xmldata)
