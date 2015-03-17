from distutils.core import setup
import re, os

to_path = "/opt"
from_path = 'mehrcal'

def get_files():
    datafiles = []
    for root, dirs, files in os.walk(from_path):
        for f in files:
            filename, ext = os.path.splitext(f)
            if ext!=".pyc" and ext!=".ui~" : #--- Exclude this extensions
                datafiles.append((os.path.join(to_path, root),[os.path.join(root, f)]))

    return datafiles

data_files = get_files()
data_files.append( ('/usr/share/icons/hicolor/scalable/apps', ['mehrcal/data/mehrcal.svg']) )
data_files.append( ('/usr/share/applications', ['mehrcal/data/mehrcal.desktop']) )
data_files.append( ('/usr/bin', ['mehrcal/mehrcal']) )


setup(
    name='mehrcal',
    author = 'Mahdi Ghane.g',
    url = 'https://github.com/meyt/mehrcal',
    version='0.2dev',
    require=["python-gi"],
    zip_safe= False,
    include_package_data= True,
    license="GPLv3",
    long_description=""" a simplpe Persian/Jalali calendar """,
    #scripts = ["mehrcal/mehrcal"],
    classifiers = [
        # http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI-Approved :: GNU General Public License (GPL)',
        'Intended Audience :: End Users/Desktop',
        'Development Status :: 2 - Pre-Alpha',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python',
        'Natural Language :: Persian',
        'Environment :: X11 Applications :: GTK',
        'Topic :: Desktop Environment :: Gnome'
        ],
    data_files= data_files
)