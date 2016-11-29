#!/usr/bin/env python3

import utils
import cipher
import unittest

KEY_LENGTH_UPPER_BOUND = 20  # Unlikely that higher? ^^^  Could have problems with repeated...


class Vigenere(cipher.AbstractCipher):

	def encrypt(plaintext, key):
		ciphertext = ''

		lowera = ord('a')
		keylen = len(key)
		keyIndex = 0
		for c in plaintext:
			if utils.isAlpha(c):
				shift = ord(key[keyIndex]) - lowera
				ciphertext += chr(((ord(c) - lowera + shift) % utils.ALPHABET_SIZE) + lowera) 

				keyIndex = (keyIndex + 1) % keylen  # Updating the key
			else:
				ciphertext += c  # key not updated

		return ciphertext

	def decrypt(ciphertext, key):
		plaintext = ''

		lowera = ord('a')
		keylen = len(key)
		keyIndex = 0
		for c in ciphertext:
			if utils.isAlpha(c):
				shift = ord(key[keyIndex]) - lowera
				plaintext += chr(((ord(c) - lowera - shift + utils.ALPHABET_SIZE) % utils.ALPHABET_SIZE) + lowera) 

				keyIndex = (keyIndex + 1) % keylen  # Updating the key
			else:
				plaintext += c  # key not updated

		return plaintext

	def crack(ciphertext):
		keyLen = Vigenere.findKeyLength(ciphertext, KEY_LENGTH_UPPER_BOUND)

		key = ''
		lowera = ord('a')
		for i in range(keyLen):  # gets each Caesar text embedded in the ciphertext
			subtext = ''

			j = i
			while j < len(ciphertext):
				c = ciphertext[j]
				if utils.isAlpha(c):
					subtext += c

				j += keyLen

			lowestShift = 0
			lowestChi2 = 100000

			for j in range(min(utils.ALPHABET_SIZE, len(ciphertext))):
				maybePlaintext = Vigenere.rot(subtext, j)
				chi2 = utils.calcChiSquared(maybePlaintext)
				if chi2 < lowestChi2:
					lowestShift = j
					lowestChi2 = chi2

			keyShift = 0
			if lowestShift != 0:
				keyShift = 26-lowestShift  # We found the amount to shift for decryption, now we want the encryption key

			key += chr(keyShift+lowera)

		key = Vigenere.refineKey(key)

		plaintext = Vigenere.decrypt(ciphertext, key)
		chi2 = utils.calcChiSquared(plaintext)

		return (key, chi2)

	# It's possible that we found the key to be lemonlemon, but really it should just be lemon.  This function refines it
	def refineKey(maybeRepeatKey):
		length = len(maybeRepeatKey)

		for i in range(1, length):
			if length % i == 0:
				if maybeRepeatKey[0:i]*(length//i) == maybeRepeatKey:
					return maybeRepeatKey[0:i]  # We don't need to look further, this is the best one

		return maybeRepeatKey  # No refining possible

	def findKeyLength(ciphertext, keyLengthUpperBound):
		highestIOC = -1.0  # Highest index of coincidence found so far
		shiftForHighest = 1

		for i in range(1,keyLengthUpperBound):
			shiftedString = Vigenere.shiftString(ciphertext, i)

			indexOfCoincidence = Vigenere.calcIndexOfCoincidence(ciphertext, shiftedString)

			if indexOfCoincidence > highestIOC:
				highestIOC = indexOfCoincidence
				shiftForHighest = i

		return shiftForHighest   # This shift gave the highest COI, which implies that it's the keylength

	# Calculates how many times the lined up characters of the two texts match, then uses the index of coincidence formula
	def calcIndexOfCoincidence(text1, text2):
		numOccurs = {}  # Dictionary mapping alphabet chars to number of times it matches in the two texts
		for i in range(len(text1)):
			c = text1[i]
			if c == text2[i]:
				numOccurs[c] = numOccurs.setdefault(c, 0) + 1

		summation = 0.0
		for x in numOccurs.values():
			summation += x*(x-1)

		text1Len = len(text1)
		indexOfCoincidence = utils.ALPHABET_SIZE*summation/(text1Len*(text1Len-1))  # Note this requires that the ciphertext must have multiple characters...

		return indexOfCoincidence


	# This is not rot.  It sends the ith character to the (i+shift)th spot, module len(str)
	def shiftString(inStr, shift):
		shift = shift % len(inStr)  # in case shift is greater (shouldn't be)
		return inStr[-shift:]+inStr[:-shift] 

	def rot(plaintext, shift):
		ciphertext = ''

		lowera = ord('a')
		for c in plaintext:
			if utils.isAlpha(c):
				ciphertext += chr(((ord(c)-lowera+shift) % utils.ALPHABET_SIZE)+lowera)
			else:
				ciphertext += c

		return ciphertext

	def getNameOfCipher(key=None):
		if len(key) == 1:
			return 'Caesar (Vigenere)'  # Should technically also handle rot13
		else:
			return 'Vigenere'

	def usage():
		print('Key must be a lower-case string')


class VigenereTest(unittest.TestCase):

	def test_encrypt(self):
		plaintext = 'abcde'
		self.assertEqual(Vigenere.encrypt(plaintext, 'b'), 'bcdef')

		plaintext = 'abcde'
		self.assertEqual(Vigenere.encrypt(plaintext, 'a'), 'abcde')

		plaintext = 'wxyza'
		self.assertEqual(Vigenere.encrypt(plaintext, 'b'), 'xyzab')

		plaintext = 'a c'
		self.assertEqual(Vigenere.encrypt(plaintext, 'b'), 'b d')

		plaintext = 'to be or not to be that is the question'
		self.assertEqual(Vigenere.encrypt(plaintext, 'relations'), 'ks me hz bbl ks me mpog aj xse jcsflzsy')

	def test_decrypt(self):
		ciphertext = 'bcdef'
		self.assertEqual(Vigenere.decrypt(ciphertext, 'b'), 'abcde')

		ciphertext = 'abcde'
		self.assertEqual(Vigenere.decrypt(ciphertext, 'a'), 'abcde')

		ciphertext = 'xyzab'
		self.assertEqual(Vigenere.decrypt(ciphertext, 'b'), 'wxyza')

		ciphertext = 'b d'
		self.assertEqual(Vigenere.decrypt(ciphertext, 'b'), 'a c')

		ciphertext = 'ks me hz bbl ks me mpog aj xse jcsflzsy'
		self.assertEqual(Vigenere.decrypt(ciphertext, 'relations'), 'to be or not to be that is the question')

	def test_identity(self):
		text = 'hello there!'
		key = 'key'

		self.assertEqual(Vigenere.decrypt(Vigenere.encrypt(text, key), key), text)

		self.assertEqual(Vigenere.encrypt(Vigenere.decrypt(text, key), key), text)

	def test_calcIndexOfCoincidence(self):
		text1 = 'abcdefgab'
		text2 = 'abcjgfaab'

		self.assertAlmostEqual(Vigenere.calcIndexOfCoincidence(text1, text2), 1.444444444)

	def test_shiftString(self):
		text1 = 'abcdefgh'
		text2 = 'ghabcdef'

		self.assertEqual(Vigenere.shiftString(text1, 2), text2)
		self.assertEqual(Vigenere.shiftString(text1, 0), text1)

	def test_rot(self):
		self.assertEqual(Vigenere.rot('xyz',1), 'yza')
		self.assertEqual(Vigenere.rot('x z',1), 'y a')

	def test_findKeyLength(self):
		ciphertext = 'ulpkxwrjugccqdlbvkvinlctzevoknlycwqlytcrqbmyjaszdwwlmikzeglimkllcfimvezygmiapfwvjjbsalukezeayjxetwwxryzmckuidiaxglvbivpjucgcqeamrwsceuienxzfunzikiyvuevpgkahxkvwegwfgwbssnfqiznggvolmtfzcpivnwiwvhdpjmrmmmdshurlqnzuizvmwsnvyxwgslzjyalkjvxxatfceaszxsnzjrapuoidxgdmwyvwlllutjrntvyeomiwanpyeblahkzkztlsrpxppfnzxebtghrihvzflvkyltsnzjruzvyiigzjhnfbviazszixmckytowbswxzngqadcezwwqeukciullctngwxhokzvanayexiiyvyczgbcawrgivrahvzvqyygfyizyulpkxwrjugccqdzyrqmtjtujzhwyeukciullctvpbswiitevouidkybpjmtdivnwjivgbtuytmcxegaivtptuucbsztlbdnezpvyjdkvpvuijyvouidkybllcfietssluiiadsmjpqxeaienqivahxnykssfxjvqezgjcezolismiivahgmekeawvwciyquuqizdslpdxqdlbvjvmeawrgpgagmjdftplismiivkotceajknvhfceanznmvqwujdftpliujwwmquetovzohgmekeawrgqmlfmtmcxegffbczpdukzhbpubejpwrqbrnvitkyuvrcxtyijjtpyucdwafwmkcimwwwkmsvtuzijrbtwlwjyvosnzjrelkceqstgwxzieklkyzixppmhzoildlukzwesawylymdlcfiilhzykcizcwkldvqyymlntmnlyuxvqxahrgwbzhlfqmlplbvdvlpulpkxqzfevtwbzdunzrnzjwvhiveamligwyknzoybtghrgxppwzwvvofwxkcebezcjdwigaicvxqzfiwolmcaayosnygnszmvrxiixilegcexvqxahroiwywmvgjidycmzrqylbvamnezudzrlx'
		self.assertEqual(Vigenere.findKeyLength(ciphertext, KEY_LENGTH_UPPER_BOUND), 14)  # Actually, the key length is 7, but refineKey catches this

	def test_refineKey(self):
		self.assertEqual(Vigenere.refineKey('lemonlemonlemon'), 'lemon')
		self.assertEqual(Vigenere.refineKey('lemon'), 'lemon')
		self.assertEqual(Vigenere.refineKey('lemonlemonorange'), 'lemonlemonorange')		
		self.assertEqual(Vigenere.refineKey('aaaaaaaaaaa'), 'a')

	def test_crack(self):
		ciphertext = 'ulpkxwrjugccqdlbvkvinlctzevoknlycwqlytcrqbmyjaszdwwlmikzeglimkllcfimvezygmiapfwvjjbsalukezeayjxetwwxryzmckuidiaxglvbivpjucgcqeamrwsceuienxzfunzikiyvuevpgkahxkvwegwfgwbssnfqiznggvolmtfzcpivnwiwvhdpjmrmmmdshurlqnzuizvmwsnvyxwgslzjyalkjvxxatfceaszxsnzjrapuoidxgdmwyvwlllutjrntvyeomiwanpyeblahkzkztlsrpxppfnzxebtghrihvzflvkyltsnzjruzvyiigzjhnfbviazszixmckytowbswxzngqadcezwwqeukciullctngwxhokzvanayexiiyvyczgbcawrgivrahvzvqyygfyizyulpkxwrjugccqdzyrqmtjtujzhwyeukciullctvpbswiitevouidkybpjmtdivnwjivgbtuytmcxegaivtptuucbsztlbdnezpvyjdkvpvuijyvouidkybllcfietssluiiadsmjpqxeaienqivahxnykssfxjvqezgjcezolismiivahgmekeawvwciyquuqizdslpdxqdlbvjvmeawrgpgagmjdftplismiivkotceajknvhfceanznmvqwujdftpliujwwmquetovzohgmekeawrgqmlfmtmcxegffbczpdukzhbpubejpwrqbrnvitkyuvrcxtyijjtpyucdwafwmkcimwwwkmsvtuzijrbtwlwjyvosnzjrelkceqstgwxzieklkyzixppmhzoildlukzwesawylymdlcfiilhzykcizcwkldvqyymlntmnlyuxvqxahrgwbzhlfqmlplbvdvlpulpkxqzfevtwbzdunzrnzjwvhiveamligwyknzoybtghrgxppwzwvvofwxkcebezcjdwigaicvxqzfiwolmcaayosnygnszmvrxiixilegcexvqxahroiwywmvgjidycmzrqylbvamnezudzrlx'
		plaintext = 'cryptographyisthepracticeandstudyoftechniquesforsecurecommunicationinthepresenceofthirdpartiescalledadversariesmoregenerallyitisaboutconstructingandanalyzingprotocolsthatovercometheinfluenceofadversariesandwhicharerelatedtovariousaspectsininformationsecuritysuchasdataconfidentialitydataintegrityauthenticationandnonrepudiationmoderncryptographyintersectsthedisciplinesofmathematicscomputerscienceandelectricalengineeringmoderncryptographyisheavilybasedonmathematicaltheoryandcomputersciencepracticecryptographicalgorithmsaredesignedaroundcomputationalhardnessassumptionsmakingsuchalgorithmshardtobreakinpracticebyanyadversaryitistheoreticallypossibletobreaksuchasystembutitisinfeasibletodosobyanyknownpracticalmeanscryptologyrelatedtechnologyhasraisedanumberoflegalissuestheelectronicfrontierfoundationwasinvolvedinacaseintheunitedstateswhichquestionedwhetherrequiringsuspectedcriminalstoprovidetheirdecryptionkeystolawenforcementisunconstitutionaltheeffarguedthatthisisaviolationoftherightofnotbeingforcedtoincriminateoneselfasgiveninthefifthamendm'

		(key, _) = Vigenere.crack(ciphertext)
		maybePlaintext = Vigenere.decrypt(ciphertext, key)
		self.assertEqual(plaintext, maybePlaintext)
