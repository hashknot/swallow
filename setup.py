from setuptools import setup, find_packages

setup(name='swallow',
      version='0.1',
      description='A utility which overlays wallaper and quote of the day',
      author='Jitesh Kamble',
      author_email='io@jite.sh',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'bs4',
          'requests',
          'Pillow',
      ],
      entry_points={
          'console_scripts': [
              'swallow=swallow.main:main'
          ]
      },
      )
