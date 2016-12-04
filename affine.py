#!/usr/bin/env python3

import utils
import cipher
import unittest
import fractions

class Affine(cipher.AbstractBruteForceCipher):

	def encrypt(self, plaintext, key):
		(a,b) = key
		ciphertext = ''

		lowera = ord('a')
		for c in plaintext:
			if utils.isAlpha(c):
				x = ord(c)-lowera
				y = (a*x+b) % utils.ALPHABET_SIZE
				ciphertext += chr(lowera+y)
			else:
				ciphertext += c

		return ciphertext

	def decrypt(self, ciphertext, key):
		(a,b) = key
		plaintext = ''

		lowera = ord('a')
		for c in ciphertext:
			if utils.isAlpha(c):
				x = ord(c)-lowera
				y = (utils.multInverse(a, utils.ALPHABET_SIZE)*(x-b)) % utils.ALPHABET_SIZE
				plaintext += chr(lowera+y)
			else:
				plaintext += c

		return plaintext	

	def genKeys(self):  # Can't really unit test this effectively...
		for a in range(1, utils.ALPHABET_SIZE):
			if fractions.gcd(a, utils.ALPHABET_SIZE) == 1:
				for b in range(1, utils.ALPHABET_SIZE):
					yield (a,b)	

	def crack(self, ciphertext):
		return super().bruteForce(ciphertext)

	def getNameOfCipher(self, key=None):
		if key == None:
			return 'Affine'

		(a,b) = key
		if a == 25 and b == 25:
			return 'Atbash (Affine)'
		elif a == 1:
			if b == 13:
				return 'Rot13 (Caesar (Affine))'
			else:
				return 'Caesar (Affine)'
		else:
			return 'Affine'

	def usage(self):
		print('Key is in the form (a,b), where 1<=a<utils.ALPHABET_SIZE,')
		print('0<=b<utils.ALPHABET_SIZE, and gcd(a, utils.ALPHABET_SIZE=1')


class AffineTest(unittest.TestCase):

	def setUp(self):
		self.affineInstance = Affine()

	def test_encrypt(self):
		self.assertEqual(self.affineInstance.encrypt('abc', (1,1)), 'bcd')
		self.assertEqual(self.affineInstance.encrypt('xyz', (1,1)), 'yza')
		self.assertEqual(self.affineInstance.encrypt('aBc', (1,1)), 'bBd')
		self.assertEqual(self.affineInstance.encrypt('affine cipher', (5,8)), 'ihhwvc swfrcp')

	def test_decrypt(self):
		self.assertEqual(self.affineInstance.decrypt('bcd', (1,1)), 'abc')
		self.assertEqual(self.affineInstance.decrypt('bBd', (1,1)), 'aBc')
		self.assertEqual(self.affineInstance.decrypt('ihhwvc swfrcp', (5,8)), 'affine cipher')

	def test_identity(self):
		self.assertEqual(self.affineInstance.encrypt(self.affineInstance.decrypt('random text hi there! zzz', (7,13)), (7,13)), 'random text hi there! zzz')
		self.assertEqual(self.affineInstance.encrypt(self.affineInstance.decrypt('random text hi there! zzz', (7,13)), (7,13)), 'random text hi there! zzz')

	def test_crack(self):
		# Regular Affine
		ciphertext = 'lrekmepqocpcboygywppehfiwpfzyqgdzergypwfywecyojeqcmyegfgypwfcymjyfgfmfgwpqgdzergpgffzeyciedbcgpfehfbefferqcpjeepqrodfexfwcpowpewlyetercbxgllerepfqgdzerfehfbefferyxedepxgpswpgfydwygfgwpgpfzeieyycse'
		plaintext = 'frequencyanalysisonnextmonthscipherisnotsoeasybecauseitisnotasubstitutioncipherinitthesameplaintextlettercanbeencryptedtoanyoneofseveraldifferentciphertextlettersdependingonitspositioninthemessage'
		(key, _) = self.affineInstance.crack(ciphertext)
		maybePlaintext = self.affineInstance.decrypt(ciphertext, key)
		self.assertEqual(key, (7,2))
		self.assertEqual(plaintext, maybePlaintext)

		# Caesar text
		ciphertext = 'qeb nrfzh yoltk clu grjmp lsbo qeb ixwv ald'
		plaintext = 'the quick brown fox jumps over the lazy dog'
		(key, _) = self.affineInstance.crack(ciphertext)
		maybePlaintext = self.affineInstance.decrypt(ciphertext, key)
		self.assertEqual(key, (1,23))		
		self.assertEqual(plaintext, maybePlaintext)

		# Atbash text
		ciphertext = 'gsv jfrxp yildm ulc qfnkh levi gsv ozab wlt'
		plaintext = 'the quick brown fox jumps over the lazy dog'
		(key, _) = self.affineInstance.crack(ciphertext)
		maybePlaintext = self.affineInstance.decrypt(ciphertext, key)
		self.assertEqual(key, (utils.ALPHABET_SIZE-1,utils.ALPHABET_SIZE-1))				
		self.assertEqual(plaintext, maybePlaintext)
