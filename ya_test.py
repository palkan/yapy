import unittest
import tempfile
import os
import ya

class TestYaParser(unittest.TestCase):
	def test_parse_line(self):
		ya.COLLECT_EMPTY = False
		self.assertFalse(ya.parse_line('sesid1	M	user_id'))
		self.assertEqual(('sesid1','Q'), ya.parse_line('sesid1	2914120412	Q	1	1	[url1,url2] '))
		self.assertEqual(('sesid1','C'), ya.parse_line('sesid1	12345678	C	1	1'))
		self.assertFalse(ya.parse_line('sesid1 M user_id'))
		self.assertFalse(ya.parse_line('sesid1	C	12313	1	1'))
		ya.COLLECT_EMPTY = True
		self.assertEqual(('sesid1',False), ya.parse_line('sesid1	M	user_id'))
		

	def test_process_file(self):
		input = open('session_log.txt','r')
		tmp = tempfile.mkstemp()[1]
		output = open(tmp, 'w')
		ya.COLLECT_EMPTY = False
		ya.process_file(input,output)
		input.close()
		output.close()
		gold_file = open('qclick_log_gold.txt','r')
		expected = gold_file.read().rstrip('\n\t')
		gold_file.close()
		res_file = open(tmp)
		result = res_file.read().rstrip('\n\t')
		res_file.close()
		self.assertEqual(expected,result)
		
	def test_process_file_with_empty(self):
		input = open('session_log.txt','r')
		tmp = tempfile.mkstemp()[1]
		output = open(tmp, 'w')
		ya.COLLECT_EMPTY = True
		ya.process_file(input,output)
		input.close()
		output.close()
		gold_file = open('qclick_log_empty_gold.txt','r')
		expected = gold_file.read().rstrip('\n\t')
		gold_file.close()
		res_file = open(tmp)
		result = res_file.read().rstrip('\n\t')
		res_file.close()
		self.assertEqual(expected,result)	
		
		
	
if __name__ == '__main__':
    unittest.main()