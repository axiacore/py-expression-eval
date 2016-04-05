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


class ParserTestCase(unittest.TestCase):

    def test_parser(self):
        parser = Parser()
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

if __name__ == '__main__':
    unittest.main()
