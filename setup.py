from setuptools import setup

with open("README.md", "r") as file:
    long_description = file.read()

setup(name='goinpy',
      version='0.2',
      description='Use Golang functions inside Python code',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='http://github.com/hermanTenuki/goinpy/',
      author='Herman Schechkin (hermanTenuki)',
      author_email='itseasy322@gmail.com',
      license='MIT',
      packages=['goinpy'],
      classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
            'Operating System :: OS Independent',
      ],
      include_package_data=False,
      python_requires='>=3.6')
