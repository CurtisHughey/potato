#!/usr/bin/env python3

import utils
import cipher
import unittest

class Nothing(cipher.AbstractCipher):

	def encrypt(plaintext, key):
		return plaintext

	def decrypt(ciphertext, key):
		return ciphertext	

	def crack(ciphertext):
		chi2 = utils.calcChiSquared(ciphertext)

		return (None, chi2)

	def getNameOfCipher(key=None):
		return 'Nothing'

	def usage():
		print('Key is ignored.  Sees if plaintext')


class NothingTest(unittest.TestCase):

	def test_encrypt(self):
		self.assertEqual(Nothing.encrypt('abc', (1,1)), 'abc')

	def test_decrypt(self):
		self.assertEqual(Nothing.decrypt('abc', (1,1)), 'abc')
