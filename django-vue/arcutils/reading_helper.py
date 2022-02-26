from .reading_processor.syllables import get_total_syllables
from .reading_processor.words_sentences import get_total_sentences, get_total_words
from django.utils.text import Truncator

DIFFICULTY_MULTIPLIER = 1000
MAGIC_READABILITY_CONST = [0.3793, 0.0207, 13.988]
MAX_WORDS = 300


def encode_difficulty(score):
    return int(float(score) * DIFFICULTY_MULTIPLIER)


def decode_difficulty(score):
    return score / DIFFICULTY_MULTIPLIER


def compute_reading_difficulty(reading):
    stripped_reading = clean_text(reading)

    total_words = get_total_words(stripped_reading)
    total_sentences = get_total_sentences(stripped_reading)
    total_syllables = get_total_syllables(stripped_reading)

    #print('Words', total_words)
    #print('Sentences', total_sentences)
    #print('Syllables', total_syllables)
    if total_sentences == 0:
        total_sentences = 1
    word_by_sentence_1 = float(total_words) / total_sentences
    sentence_word_multiply_1 = word_by_sentence_1 * MAGIC_READABILITY_CONST[0]
    syll_multiply = total_syllables * MAGIC_READABILITY_CONST[1]
    total_multiply_1 = sentence_word_multiply_1 + syll_multiply

    word_by_sentence_2 = float(300)/total_sentences
    sentence_word_multiply_2 = word_by_sentence_2 * MAGIC_READABILITY_CONST[0]
    total_multiply_2 = sentence_word_multiply_2 + syll_multiply

    #print('Word/sentence', word_by_sentence)
    #print('Sentence word multiply', sentence_word_multiply)
    #print('Syllables multiply', syll_multiply)
    #print('Total multiply', total_multiply)

    return [total_multiply_1 - MAGIC_READABILITY_CONST[2],
            total_multiply_2 - MAGIC_READABILITY_CONST[2],
            total_words, total_syllables, total_sentences]


def clean_text(str):
    stripped_str = str.replace("\n", " ")
    stripped_str = str.rstrip().lstrip()
    while "  " in stripped_str:
        stripped_str = stripped_str.replace("  ", " ")

    return Truncator(stripped_str).words(MAX_WORDS, '')
