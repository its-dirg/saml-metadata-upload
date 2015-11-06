from setuptools import setup, find_packages

setup(
    name='saml_metadata_upload',
    version='0.1',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    package_data={
        'upload_service': [
            'schema/*.xsd',
            'templates/*.html'
        ]
    },
    url='https://github.com/its-dirg/saml-metadata-upload',
    license='Apache License 2.0',
    author='Rebecka Gulliksson',
    author_email='rebecka.gulliksson@umu.se',
    description='Simple file upload service for SAML metadata.'
)
