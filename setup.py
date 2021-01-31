from setuptools import setup, find_packages

setup(
    name='jigsaw_generator',
    version='0.0',
    author='Bruno Bollos Correa (Bollos00)',
    author_email='bollos@outlook.com.br',
    license='GPLv3',
    description='',
    keywords='',
    url='https://github.com/Bollos00/JigsawGenerator',
    packages=find_packages(),
    install_requires=['numpy', 'PySide2'],
    long_description=open('README.md').read(),
    package_dir={'jigsaw_generator': 'jigsaw_generator'},
    package_data={'jigsaw_generator': ['image_template.jpg']}
)
