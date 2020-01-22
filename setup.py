from setuptools import setup, find_packages

setup(name='Another .txt Editor',
      version= '1.0',
      description='Another tkinter txt editor',
      author='Rodrigo Pietnechuk',
      author_email='ptnchk.rodrigo@gmail.com',
      project_urls={
          'Source code':'https://github.com/ghnoob/Another-txt-Editor'
      },
      packages=find_packages(),
      scripts=['main.py'],
      install_requires=['tkfontchoser']
     )