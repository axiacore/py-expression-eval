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
    def setUp(self):
        self.parser = Parser()

    def test_parser(self):
        parser = Parser()
        #parser and variables
        self.assertEqual(parser.parse('pow(x,y)').variables(), ['x','y'])
        self.assertEqual(parser.parse('pow(x,y)').symbols(), ['pow','x','y'])

        #checking if '"a b"' could be a variable (using it in sql)
        self.assertEqual(parser.parse('"a b"*2').evaluate({'"a b"':2}),4)

        #evaluate
        self.assertEqual(parser.parse('1').evaluate({}), 1)
        self.assertEqual(parser.parse('a').evaluate({'a': 2}), 2)
        self.assertEqual(parser.parse('2 * 3').evaluate({}), 6)
        self.assertEqual(parser.parse(u'2 \u2219 3').evaluate({}), 6)
        self.assertEqual(parser.parse(u'2 \u2022 3').evaluate({}), 6)
        self.assertEqual(parser.parse('2 ^ x').evaluate({'x': 3}), 8)
        self.assertEqual(parser.parse('x < 3').evaluate({'x': 3}), False)
        self.assertEqual(parser.parse('x < 3').evaluate({'x': 2}), True)
        self.assertEqual(parser.parse('x <= 3').evaluate({'x': 3}), True)
        self.assertEqual(parser.parse('x <= 3').evaluate({'x': 4}), False)
        self.assertEqual(parser.parse('x > 3').evaluate({'x': 4}), True)
        self.assertEqual(parser.parse('x >= 3').evaluate({'x': 3}), True)
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
        self.assertEqual(parser.parse("'x'=='x'").evaluate({}), True)
        self.assertEqual(parser.parse("(a+b)==c").evaluate({'a': 1, 'b': 2, 'c': 3}), True)
        self.assertEqual(parser.parse("(a+b)!=c").evaluate({'a': 1, 'b': 2, 'c': 3}), False)
        self.assertEqual(parser.parse("(a^2-b^2)==((a+b)*(a-b))").evaluate({'a': 4859, 'b': 13150}), True)
        self.assertEqual(parser.parse("(a^2-b^2+1)==((a+b)*(a-b))").evaluate({'a': 4859, 'b': 13150}), False)
        self.assertEqual(parser.parse("x/((x+y))").simplify({}).evaluate({'x':1, 'y':1}), 0.5)

        #functions
        self.assertEqual(parser.parse('pyt(2 , 0)').evaluate({}),2)
        self.assertEqual(parser.parse("concat('Hello',' ','world')").evaluate({}),'Hello world')
        self.assertEqual(parser.parse('if(a>b,5,6)').evaluate({'a':8,'b':3}),5)
        self.assertEqual(parser.parse('if(a,b,c)').evaluate({'a':None,'b':1,'c':3}),3)



        # test substitute
        expr = parser.parse('2 * x + 1')
        expr2 = expr.substitute('x', '4 * x')  # ((2*(4*x))+1)
        self.assertEqual(expr2.evaluate({'x': 3}), 25)

        # test simplify
        expr = parser.parse('x * (y * atan(1))').simplify({'y': 4})
        self.assertIn('x*3.141592', expr.toString())
        self.assertEqual(expr.evaluate({'x': 2}), 6.283185307179586)

        # test toString with string constant
        expr = parser.parse("'a'=='b'")
        self.assertIn("'a'=='b'",expr.toString())
        self.assertIn("'a'=='b'", "%s" % expr)
        expr = parser.parse("concat('a\n','\n','\rb')=='a\n\n\rb'")
        self.assertEqual(expr.evaluate({}),True)
        expr = parser.parse("a==''")
        self.assertEqual(expr.evaluate({'a':''}),True)

        #test toString with an external function
        expr=parser.parse("myExtFn(a,b,c,1.51,'ok')")
        self.assertEqual(expr.substitute("a",'first').toString(),"myExtFn(first,b,c,1.51,'ok')")



        # test variables
        expr = parser.parse('x * (y * atan(1))')
        self.assertEqual(expr.variables(), ['x', 'y'])
        self.assertEqual(expr.simplify({'y': 4}).variables(), ['x'])

        # list operations
        self.assertEqual(parser.parse('a, 3').evaluate({'a': [1, 2]}), [1, 2, 3])

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
        self.assertEqual(self.parser.parse('Engage1').variables(), ["Engage1"])
        self.assertEqual(self.parser.parse('E1').variables(), ["E1"])
        self.assertEqual(self.parser.parse('PI2').variables(), ["PI2"])
        self.assertEqual(self.parser.parse('(E1 + PI)').variables(), ["E1"])
        self.assertEqual(self.parser.parse('E1_').variables(), ["E1_"])
        self.assertEqual(self.parser.parse('E_').variables(), ["E_"])

    def test_evaluating_consts(self):
        self.assertEqual(self.parser.evaluate("Engage1", variables={"Engage1": 2}), 2)
        self.assertEqual(self.parser.evaluate("Engage1 + 1", variables={"Engage1": 1}), 2)

    def test_custom_functions(self):
        parser = Parser()

        def testFunction0():
            return 13
        def testFunction1(a):
            return 2*a+9
        def testFunction2(a,b):
            return 2*a+3*b

        # zero argument functions don't currently work
        # self.assertEqual(parser
        #     .parse('testFunction()')
        #     .evaluate({"testFunction":testFunction0}),13)
        self.assertEqual(parser
            .parse('testFunction(x)')
            .evaluate({"x":2,"testFunction":testFunction1}),13)
        self.assertEqual(parser
            .parse('testFunction(x , y)')
            .evaluate({"x":2,"y":3,"testFunction":testFunction2}),13)

        # Add some "built-in" functions
        def mean(*xs):
            return sum(xs) / len(xs)
        parser.functions['mean'] = mean

        def counter(initial):
            class nonlocals:
                x = initial
            def count(increment):
                nonlocals.x += increment
                return nonlocals.x
            return count
        parser.functions['count'] = counter(0)

        self.assertEqual(parser.parse("mean(xs)").variables(), ["xs"])
        self.assertEqual(parser.parse("mean(xs)").symbols(), ["mean", "xs"])
        self.assertEqual(parser.evaluate("mean(xs)", variables={"xs": [1, 2, 3]}), 2)
        self.assertEqual(parser.evaluate("count(inc)", variables={"inc": 5}), 5)
        self.assertEqual(parser.evaluate("count(inc)", variables={"inc": 5}), 10)

    def test_decimals(self):
        parser = Parser()

        self.assertEqual(parser.parse(".1").evaluate({}), parser.parse("0.1").evaluate({}))
        self.assertEqual(parser.parse(".1*.2").evaluate({}), parser.parse("0.1*0.2").evaluate({}))
        self.assertEqual(parser.parse(".5^3").evaluate({}), float(0.125))
        self.assertEqual(parser.parse("16^.5").evaluate({}), 4)
        self.assertEqual(parser.parse("8300*.8").evaluate({}), 6640)

        with self.assertRaises(ValueError):
            parser.parse("..5").evaluate({})


if __name__ == '__main__':
    unittest.main()
