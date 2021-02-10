#!/usr/bin/python3

#Author: William Anderson
#Identikey: wian8678
#Assignment: Project 1
#Class: ECEN 4113

import sys
from collections import Counter

#taken from Wikipedia
letter_freqs = {
    'A': 0.08167,
    'B': 0.01492,
    'C': 0.02782,
    'D': 0.04253,
    'E': 0.12702,
    'F': 0.02228,
    'G': 0.02015,
    'H': 0.06094,
    'I': 0.06966,
    'J': 0.00153,
    'K': 0.00772,
    'L': 0.04025,
    'M': 0.02406,
    'N': 0.06749,
    'O': 0.07507,
    'P': 0.01929,
    'Q': 0.00095,
    'R': 0.05987,
    'S': 0.06327,
    'T': 0.09056,
    'U': 0.02758,
    'V': 0.00978,
    'W': 0.02361,
    'X': 0.00150,
    'Y': 0.01974,
    'Z': 0.00074
}

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def pop_var(s):
    """Calculate the population variance of letter frequencies in given string."""
    freqs = Counter(s)
    mean = sum(float(v)/len(s) for v in freqs.values())/len(freqs)  
    return sum((float(freqs[c])/len(s)-mean)**2 for c in freqs)/len(freqs)

# ic(string: ciphertext)
# This function returns the Index of Coincidence for the sequence of ciphertext given
# Returns an integer
def ic(ciphertext):
    # Length of ciphertext to be used in IC equation
	N = float(len(ciphertext))

    # Variable for the frequency of the char in alphabet
	frequency = 0.0

    # Go through alphabet list
	for char in alphabet:
        # Source: https://en.wikipedia.org/wiki/Index_of_coincidence
		frequency += ciphertext.count(char) * (ciphertext.count(char) - 1)
	return frequency / (N * (N - 1))


# findKeyLen(string: ciphertext)
# Finds the length of the key given a cipher text
# This uses the Kasiski method byt is more verbose and abstract
def findKeyLen(ciphertext):
	 #index of coincidence table
	icTable = []

	# For guess length of highest keylen guess. Go through each of the sequences
    # all the way up to 13. After splitting up the cipher text into sequences up
    # to size 13, sort the index of coincidences of those sequences.
	for guess in range(13):
         #IC for a particular sequence
		icSum = 0.0

        #Average of those sequences
		icAverage = 0.0

		# Build sqeuence from ciphertext based upon indicie
		for i in range(guess):
			sequence = ""

            # This is the part that breaks up the ciphertext based upon
            # the sequence number and guess length
			for j in range(0, len(ciphertext[i:]), guess): #For
				sequence += ciphertext[i+j]

            # Build the IC sum to come up with average
			icSum += ic(sequence)

        # If on first indicie, avoid dividing by zero and just add it
        # to the table.
		if not guess == 0:
			icAverage = icSum / guess
		icTable.append(icAverage)

    # Find the best IC from the stable after sorting it. If the first guess
    # this is to deal with if the key is twice or three times itself. In
    # order to prevent IC's of repeated keys we throw out the first best guess
    # for the second one, or just take the first one if it is long enough.
	best = icTable.index(sorted(icTable, reverse = True) [0])
	secondBest = icTable.index(sorted(icTable, reverse = True) [1])
	if best % secondBest == 0:
		return secondBest
	else:
		return best


# frequencyAnalysis(string: seq):
# This uses the Chi squared statistic in order to compare a sequence to
# the dictionary of frequencies of letters in the english language.
# Returns a character.
def frequencyAnalysis(seq):
    # Turn dict into list of frequencies to loop through
    values = letter_freqs.values()
    valuesList = list(values)

    # List of Chi Squareds for each letter corresponding by index
    chiSquareds = [0] * 26

    #Offset based upon if we are dealing with capitals or not
    offset = ord('A')

    # Go through sequence letter by letter and develop chi squared
    # for each letter of the alphabet
    for i in range(26):
        #This is the summation variable of chi squared equation
        chiSquaredSum = 0.0

        # This is meant to deal with the ascii offset when dealing with chi squared equation
        seqOffset = [chr(((ord(seq[j]) - offset - i) % 26)+offset) for j in range(len(seq))]

        # This is the observed value in chi squared equation
        observed = [0] * 26

        # Generate table of observed values from ascii
        for l in seqOffset:
            observed[ord(l) - ord('A')] += 1

        # Divide these to make them into frequencies between 0 and 1
        for j in range(26):
            observed[j] *= (1.0/float(len(seq)))

        # Now they are comparable to our list of letter frequencies
        for j in range(26):
            chiSquaredSum += ((observed[j] - float(valuesList[j]))**2)/float(valuesList[j])
        chiSquareds[i] = chiSquaredSum

    # Find the index of the smalles chi squared and this is how you get
    # the number of your letter.
    shift = chiSquareds.index(min(chiSquareds))

    # Account for ascii shift
    return chr(shift+offset)


# findKey(string: ciphertext, int: keylen):
# Once you know your key length all you have to do is loop through
# all of the sequences up to that length and do a frequency analysis to
# determine all possible characters of this key.
def findKey(ciphertext, keylen):
    # Our eventual key.
    key = ''

    # Loop through each sequence of ciphertext up to key length
    for i in range(keylen):

        # Our eventual sequence.
        seq = ""
        for j in range(0,len(ciphertext[i:]), keylen):
            seq += ciphertext[i+j]

        # Do frequency analysis to get each character of the key
        key += frequencyAnalysis(seq)

    return key

if __name__ == "__main__":
    # Read ciphertext from stdin
    # Ignore line breaks and spaces, convert to all upper case
    cipher = sys.stdin.read().replace("\n", "").replace(" ", "").upper()

    #################################################################
    # Your code to determine the key and decrypt the ciphertext here
    # print("Cipher: " + cipher)
    # keyLength = findKeyLen(cipher)
    # print("Key Length: " + str(keyLength))
    # print("-" * 20)
    print("Key: " + findKey(cipher, keyLength))
