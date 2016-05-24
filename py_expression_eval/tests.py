#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: AxiaCore S.A.S. http://axiacore.com
#
# Based on js-expression-eval, by Matthew Crumley (email@matthewcrumley.com, http://silentmatt.com/)
# https://github.com/silentmatt/js-expression-eval
#
# Ported to Python and modified by Vera Mazhuga (ctrl-alt-delete@live.com, http://vero4ka.info/)
#
# You are free to use and modify this code in anyway you find useful. Please leave this comment in the code
# to acknowledge its original source. If you feel like it, I enjoy hearing about projects that use my code,
# but don't feel like you have to let me know or ask permission.

import unittest

from py_expression_eval import Parser

def testFunction(a,b):
    return 2*a+3*b
class ParserTestCase(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()

    def test_parser(self):
        parser = Parser()
        #parser and variables
        self.assertEqual(parser.parse('lulu(x,y)').variables(), ['lulu','x','y'])

        #evaluate
        self.assertEqual(parser.parse('2 * 3').evaluate({}), 6)
        self.assertEqual(parser.parse('2 ^ x').evaluate({'x': 3}), 8)
        self.assertEqual(parser.parse('2 * x + 1').evaluate({'x': 3}), 7)
        self.assertEqual(parser.parse('2 + 3 * x').evaluate({'x': 4}), 14)
        self.assertEqual(parser.parse('(2 + 3) * x').evaluate({'x': 4}), 20)
        self.assertEqual(parser.parse('2-3^x').evaluate({'x': 4}), -79)
        self.assertEqual(parser.parse('-2-3^x').evaluate({'x': 4}), -83)
        self.assertEqual(parser.parse('-3^x').evaluate({'x': 4}), -81)
        self.assertEqual(parser.parse('(-3)^x').evaluate({'x': 4}), 81)
        self.assertEqual(parser.parse('2*x + y').evaluate({'x': 4, 'y': 1}), 9)
        self.assertEqual(parser.parse("x||y").evaluate({'x': 'hello ', 'y': 'world'}), 'hello world')
        self.assertEqual(parser.parse("'x'||'y'").evaluate({}), 'xy')
        #functions
        self.assertEqual(parser.parse('pyt(2 , 0)').evaluate({}),2)
        self.assertEqual(parser.parse("concat('Hello',' ','world')").evaluate({}),'Hello world')

        #external function
        self.assertEqual(parser.parse('testFunction(x , y)').evaluate({"x":2,"y":3,"testFunction":testFunction}),13)


        # test substitute
        expr = parser.parse('2 * x + 1')
        expr2 = expr.substitute('x', '4 * x')  # ((2*(4*x))+1)
        self.assertEqual(expr2.evaluate({'x': 3}), 25)

        # test simplify
        expr = parser.parse('x * (y * atan(1))').simplify({'y': 4})
        self.assertIn('x*3.141592', expr.toString())
        self.assertEqual(expr.evaluate({'x': 2}), 6.283185307179586)

        # test variables
        expr = parser.parse('x * (y * atan(1))')
        self.assertEqual(expr.variables(), ['x', 'y'])
        self.assertEqual(expr.simplify({'y': 4}).variables(), ['x'])

    def test_consts(self):
        # self.assertEqual(self.parser.parse("PI ").variables(), [""])
        self.assertEqual(self.parser.parse("PI").variables(), [])
        self.assertEqual(self.parser.parse("PI ").variables(), [])
        self.assertEqual(self.parser.parse("E ").variables(), [])
        self.assertEqual(self.parser.parse(" E").variables(), [])
        self.assertEqual(self.parser.parse("E").variables(), [])
        self.assertEqual(self.parser.parse("E+1").variables(), [])
        self.assertEqual(self.parser.parse("E / 1").variables(), [])
        self.assertEqual(self.parser.parse("sin(PI)+E").variables(), [])

    def test_parsing_e_and_pi(self):
        self.assertEqual(self.parser.parse('Pie').variables(), ["Pie"])
        self.assertEqual(self.parser.parse('PIe').variables(), ["PIe"])
        self.assertEqual(self.parser.parse('Eval').variables(), ["Eval"])
        self.assertEqual(self.parser.parse('Eval1').variables(), ["Eval1"])
        self.assertEqual(self.parser.parse('EPI').variables(), ["EPI"])
        self.assertEqual(self.parser.parse('PIE').variables(), ["PIE"])
        self.assertEqual(self.parser.parse('Engage').variables(), ["Engage"])
        self.assertEqual(self.parser.parse('Engage * PIE').variables(), ["Engage", "PIE"])
        self.assertEqual(self.parser.parse('Engage_').variables(), ["Engage_"])

if __name__ == '__main__':
    unittest.main()
