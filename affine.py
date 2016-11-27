#!/usr/bin/env python3

import utils
import cipher
import unittest
import fractions

class Affine(cipher.AbstractCipher):

	def encrypt(text, key):
		(a,b) = key
		encrypted = ''

		lowera = ord('a')
		for c in text:
			if utils.isAlpha(c):
				x = ord(c)-lowera
				y = (a*x+b) % utils.ALPHABET_SIZE
				encrypted += chr(lowera+y)
			else:
				encrypted += c

		return encrypted

	def decrypt(text, key):
		(a,b) = key
		decrypted = ''

		lowera = ord('a')
		for c in text:
			if utils.isAlpha(c):
				x = ord(c)-lowera
				y = (utils.multInverse(a, utils.ALPHABET_SIZE)*(x-b)) % utils.ALPHABET_SIZE
				decrypted += chr(lowera+y)
			else:
				decrypted += c

		return decrypted		

	def crack(text):
		key = (1,1)
		lowestChi2 = 100000  # Just a big number 

		for a in range(1, utils.ALPHABET_SIZE):
			if fractions.gcd(a, utils.ALPHABET_SIZE) == 1:
				for b in range(1, utils.ALPHABET_SIZE):
					decrypted = Affine.decrypt(text,(a,b))
					chi2 = utils.calcChiSquared(decrypted)

					if chi2 < lowestChi2:
						key = (a,b)
						lowestChi2 = chi2


		return (key, lowestChi2)

	def usage():
		print('Key is in the form (a,b), where 1<=a<utils.ALPHABET_SIZE,')
		print('0<=b<utils.ALPHABET_SIZE, and gcd(a, utils.ALPHABET_SIZE=1')


class AffineTest(unittest.TestCase):

	def test_encrypt(self):
		self.assertEqual(Affine.encrypt('abc', (1,1)), 'bcd')
		self.assertEqual(Affine.encrypt('xyz', (1,1)), 'yza')
		self.assertEqual(Affine.encrypt('aBc', (1,1)), 'bBd')
		self.assertEqual(Affine.encrypt('affine cipher', (5,8)), 'ihhwvc swfrcp')

	def test_decrypt(self):
		self.assertEqual(Affine.decrypt('bcd', (1,1)), 'abc')
		self.assertEqual(Affine.decrypt('bBd', (1,1)), 'aBc')
		self.assertEqual(Affine.decrypt('ihhwvc swfrcp', (5,8)), 'affine cipher')

	def test_identity(self):
		self.assertEqual(Affine.encrypt(Affine.decrypt('random text hi there! zzz', (7,13)), (7,13)), 'random text hi there! zzz')
		self.assertEqual(Affine.encrypt(Affine.decrypt('random text hi there! zzz', (7,13)), (7,13)), 'random text hi there! zzz')

	def test_crack(self):
		ciphertext = 'lrekmepqocpcboygywppehfiwpfzyqgdzergypwfywecyojeqcmyegfgypwfcymjyfgfmfgwpqgdzergpgffzeyciedbcgpfehfbefferqcpjeepqrodfexfwcpowpewlyetercbxgllerepfqgdzerfehfbefferyxedepxgpswpgfydwygfgwpgpfzeieyycse'
		plaintext = 'frequencyanalysisonnextmonthscipherisnotsoeasybecauseitisnotasubstitutioncipherinitthesameplaintextlettercanbeencryptedtoanyoneofseveraldifferentciphertextlettersdependingonitspositioninthemessage'
		(key, _) = Affine.crack(ciphertext)

		maybePlaintext = Affine.decrypt(ciphertext, key)
		self.assertEqual(plaintext, maybePlaintext)
