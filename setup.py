from setuptools import setup, find_packages

setup(
    name='saml_metadata_upload',
    version='0.1',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    package_data={
        'metadata_upload': [
            'schema/*.xsd',
            'templates/*.html'
        ]
    },
    url='https://github.com/its-dirg/saml-metadata-upload',
    license='Apache License 2.0',
    author='Rebecka Gulliksson',
    author_email='rebecka.gulliksson@umu.se',
    description='Simple file upload service for SAML metadata.',
    install_requires=[
        'Flask==0.10.1',
        'flask-transfer==0.0.1',
        'Flask-WTF==0.12',
        'Flask-Bootstrap==3.3.5.7',
        'lxml==3.4.4'
    ]
)
