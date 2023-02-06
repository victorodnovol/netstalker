from distutils.core import setup

setup(name='Netstalker',
      version='1.0',
      description='Multithreaded image parser for imgur.com',
      author='Viktor',
      author_email='viktor.odnovol@gmail.com',
      packages=['lib'],
      package_dir={
          'lib': 'lib',
      },
      package_data={'lib': ['*.txt']},
      install_requires=['click', 'requests', 'colorama'],
      entry_points={
          'console_scripts': [
              'stalker = lib.parser:run_app',
          ],
      })
