from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='py_expression_eval',
    version='0.3.9',
    description='Python Mathematical Expression Evaluator',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/AxiaCore/py-expression-eval/',
    author='vero4ka',
    author_email='vero4ka.ru@gmail.com',
    license='MIT',
    packages=['py_expression_eval'],
    zip_safe=False,
    test_suite='py_expression_eval.tests',
)
