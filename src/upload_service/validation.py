import pkg_resources
from flask_transfer.exc import UploadError
from lxml import etree


class SAMLMetadataValidator():
    def __init__(self):
        # Create the schema object
        with pkg_resources.resource_stream(__name__, 'schema/saml-schema-metadata-2.0.xsd') as f:
            xmlschema_doc = etree.parse(f)
        self.xmlschema = etree.XMLSchema(xmlschema_doc)

    def __call__(self, filehandle, metadata=None):
        # Validate the XML document using the schema
        try:
            # Create a tree for the XML document
            doc = etree.parse(filehandle)
            self.xmlschema.assertValid(doc)
        except (etree.XMLSyntaxError, etree.DocumentInvalid) as e:
            raise UploadError('Invalid SAML metadata.')

        return True
