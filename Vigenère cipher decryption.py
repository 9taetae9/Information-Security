import math
from collections import defaultdict

ciphertext = "dhtcgmicskfstadpnixklsduryojqjlmdiflrbppfcdbcztdbczptpipnvlmydhdddihsmtltigabtplkicbwoojgmmdpgiuehhqoexhqaacsguggxeotxcdyocimmmthnlazxlnwdgbzoulgzddbjltxizlltigabtacaiiqcseixrieatrptqtuoihecywdgbzoulgzddbjltxizlacsuoeciflbgdilnwtyyttsnloeacsikxlniciflwdgjkavgcltwtplwxajiepcyusltpseixrieudpahdjeotwtwtanqcwagicktwtplihhrplapaoacrcahpiroenlgslhtcahtgcdiaazlacplzwtgjltxizlltigabtacaiiqcseixrieatrptqtwlawiflrtlgslqtyuachulratrptqtjltxizlltigabtacaiiqcseixrielwgzptguvrshmmwxhbvmatrptqtjltxizlltigabtacaiiqcfepwjltxizlwwxqweglmydhdddihsmtltigabtplkwwtlahtcgnhixqjldjbftwtplihhrplapjpgwiroaihfpnthmumthfpntjlaiaimtoggmdltigabtxuhktjnaoiwczojcbvfbjqpcbdroegbyyyrdklsidklsetyricvuvrshmmwxhbvmatrptqtjltxizlltigabtacaiiqcfepwjltxizltwtplwxajiepcyusltpseixrieatrptqtjltxizlltigabtnchhatrptqtroegtuplaqchnpcqdegacaiiqcseixrieatrptqtjltxizlytpfseixrielwgzptguvrshmmwxhbvmatrptqt"


def find_repeated_sequences(text, seq_length=3):
    seq_positions = {}
    for i in range(len(text) - seq_length):
        seq = text[i:i+seq_length]
        if seq in seq_positions:
            seq_positions[seq].append(i)
        else:
            seq_positions[seq] = [i]
    return {seq: positions for seq, positions in seq_positions.items() if len(positions) > 1}

def get_factors(n):
    factors = set()
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            factors.add(i)
            factors.add(n // i)
    return factors

def guess_key_length(ciphertext):
    repeated_seq = find_repeated_sequences(ciphertext)
    distances = []
    for seq, positions in repeated_seq.items():
        for i in range(1, len(positions)):
            distances.append(positions[i] - positions[i-1])

    factor_counts = defaultdict(int)
    for distance in distances:
        for factor in get_factors(distance):
            factor_counts[factor] += 1

    # Return the factor that appears most often, excluding 1
    likely_key_length = max(factor_counts, key=factor_counts.get)
    
    return likely_key_length

key_length_guess = guess_key_length(ciphertext)
print(f"Guessed Key Length: {key_length_guess}")

def count_letters(group):
    count = {}
    for char in 'abcdefghijklmnopqrstuvwxyz':
        count[char] = group.count(char)
    return count

def separate_into_groups(ciphertext, key_length):
    groups = [""] * key_length

    for i, char in enumerate(ciphertext):
        groups[i % key_length] += char

    return groups

groups = separate_into_groups(ciphertext, key_length_guess)

for i, group in enumerate(groups, 1):
    letter_counts = count_letters(group)
    print(f"Group {i} letter counts:")
    for char, count in letter_counts.items():
        print(f"{char} : {count}")
    print() 

def vigenere_decrypt(ciphertext, key):
    decrypted = ""
    key_length = len(key)
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    for i in range(len(ciphertext)):
        char = ciphertext[i]
        if char.isalpha():  # decrypt only alphabets
            shift = alphabet.index(key[i % key_length].lower())
            decrypted += alphabet[(alphabet.index(char.lower()) - shift) % 26]
        else:
            decrypted += char

    return decrypted



def get_shift_for_most_frequent_to_e(group):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    
    # Get the most frequent letter in the group
    letter_counts = count_letters(group)
    most_frequent_letter = max(letter_counts, key=letter_counts.get)
    
    # Calculate the shift needed to make the most frequent letter into 'e'
    shift = (ord(most_frequent_letter) - ord('e')) % 26
    return shift

key = ""

alphabet = "abcdefghijklmnopqrstuvwxyz"
for group in groups:
    shift = get_shift_for_most_frequent_to_e(group)
    key += alphabet[shift]

print("Predicted Key:", key)

plaintext = vigenere_decrypt(ciphertext, key)
print("Plaintext:", plaintext)

print()

plaintext_answer = vigenere_decrypt(ciphertext, "happy")
print("Plaintext:", plaintext_answer)
