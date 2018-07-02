from distutils.core import setup
setup(name='Sudoku Game',
      version='1.01',
      py_modules=['sudoku', 'gui'],
      description='Simple Sudoku Game in PyGame',
      author='Wiktor Garbarek',
      author_email='wektorgarbarek@gmail.com',
      url='http://github.com/wekt0r',
      data_files=[('images', ['images/background.png', 'images/bebas.ttf', 'images/board.png']),
                  ('tests', ['tests/tests_sudoku.py'])]
      )
