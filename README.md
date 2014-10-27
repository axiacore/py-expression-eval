Python Mathematical Expression Evaluator
========================================

[![PyPi version](https://pypip.in/v/py_expression_eval/badge.png)](https://crate.io/packages/py_expression_eval/)
[![PyPi downloads](https://pypip.in/d/py_expression_eval/badge.png)](https://crate.io/packages/py_expression_eval/)

Based on js-expression-eval, by Matthew Crumley (email@matthewcrumley.com, http://silentmatt.com/)
https://github.com/silentmatt/js-expression-eval

Ported to Python and modified by Vera Mazhuga (ctrl-alt-delete@live.com, http://vero4ka.info/)

You are free to use and modify this code in anyway you find useful. Please leave this comment in the code
to acknowledge its original source. If you feel like it, I enjoy hearing about projects that use my code,
but don't feel like you have to let me know or ask permission.

Installation
------------

    pip install py_expression_eval

Examples
--------

    parser = Parser()
    parser.parse('2 * 3').evaluate({})  # 6
    parser.parse('2 ^ x').evaluate({'x': 3})  # 8
    parser.parse('2 * x + 1').evaluate({'x': 3})  # 7
    parser.parse('2 + 3 * x').evaluate({'x': 4})  # 14
    parser.parse('(2 + 3) * x').evaluate({'x': 4}) # 20
    parser.parse('2-3^x').evaluate({'x': 4})  # -79
    parser.parse('-2-3^x').evaluate({'x': 4})  # -83
    parser.parse('-3^x').evaluate({'x': 4})  # -81
    parser.parse('(-3)^x').evaluate({'x': 4})  # 81
    parser.parse('2*x + y').evaluate({'x': 4, 'y': 1})  # 9
    
    # substitute
    expr = parser.parse('2 * x + 1')
    expr2 = expr.substitute('x', '4 * x')  # ((2*(4*x))+1)
    expr2.evaluate({'x': 3})  # 25
    
    # simplify
    expr = parser.parse('x * (y * atan(1))').simplify({'y': 4})
    expr.toString()  # x*3.141592
    expr.evaluate({'x': 2})  # 6.283185307179586
    
    # get variables
    expr = parser.parse('x * (y * atan(1))')
    expr.variables()  # ['x', 'y']
    expr.simplify({'y': 4}).variables()  # ['x']


Available operations
--------------------

    parser = Parser()
    parser.parse('2 + 3').evaluate({})  # 5.0
    parser.parse('2 - 3').evaluate({})  # -1.0
    parser.parse('2 * 3').evaluate({})  # 6.0
    parser.parse('2 / 3').evaluate({})  # 0.6666666666666666
    parser.parse('2 % 3').evaluate({})  # 2.0
    parser.parse('-2').evaluate({})  #-2.0
