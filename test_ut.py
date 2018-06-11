import unittest
import emath
import os

class TestSequenceFunctions(unittest.TestCase):
    def setUp(self):
        print('测试开始执行')

    def test_loadfont(self):
        print('test load_font')

        if os.name == 'posix':
            fontpath = '/Library/Fonts/Songti.ttc'
        else:
            fontpath = 'C:\Windows\Fonts\simsun.ttc'
        
        self.assertTrue(str(emath.load_font()).find(fontpath)>=0)

        #self.assertEqual(self.seq,range(10))
        #self.assertRaises(TypeError,random.shuffle,(1,2,3))
    def test_gen_formular(self):
        print('test gen_formular')

        print( type(emath.gen_formular()))

    def tearDown(self):
        print('测试执行结束')

if __name__ == '__main__':
    unittest.main()