from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='py_expression_eval',
    version='0.3.14',
    description='Python Mathematical Expression Evaluator',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/AxiaCore/py-expression-eval/',
    author='cansadadeserfeliz',
    author_email='vero4ka.ru@gmail.com',
    license='MIT',
    packages=['py_expression_eval'],
    zip_safe=False,
    test_suite='py_expression_eval.tests',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
