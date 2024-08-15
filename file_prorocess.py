import pandas as pd
import requests
import time
import logging
from datetime import datetime, timedelta
import re
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet, brown
from collections import Counter

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

lemmatizer = WordNetLemmatizer()

CSV_FILE_PATH = 'path/to/vocabularytest.csv'
PROCESSED_CSV_FILE_PATH = 'path/to/processed_vocabulary.csv'

DICTIONARY_API_KEY = 'YOUR_DICTIONARY_API_KEY'
THESAURUS_API_KEY = 'YOUR_THESAURUS_API_KEY'

word_freq = Counter(brown.words())
total_words = sum(word_freq.values())

def clean_text(text):
    return re.sub(r'\{[^}]*\}', '', text).strip()

def get_word_frequency(word):
    lemma = lemmatizer.lemmatize(word.lower())
    freq = word_freq[lemma] / total_words
    
    if freq > 0.001: return "Very High"
    elif freq > 0.0001: return "High"
    elif freq > 0.00001: return "Medium"
    elif freq > 0.000001: return "Low"
    else: return "Very Low"

def get_merriam_webster_data(word):
    lemma = lemmatizer.lemmatize(word.lower())
    dictionary_url = f'https://www.dictionaryapi.com/api/v3/references/collegiate/json/{lemma}?key={DICTIONARY_API_KEY}'
    thesaurus_url = f'https://www.dictionaryapi.com/api/v3/references/thesaurus/json/{lemma}?key={THESAURUS_API_KEY}'
    
    definition = part_of_speech = synonyms = antonyms = ''
    
    try:
        dict_response = requests.get(dictionary_url)
        dict_response.raise_for_status()
        dict_data = dict_response.json()
        
        if dict_data and isinstance(dict_data[0], dict):
            definition = clean_text(dict_data[0].get('shortdef', [''])[0])
            part_of_speech = dict_data[0].get('fl', '')
        
        thes_response = requests.get(thesaurus_url)
        thes_response.raise_for_status()
        thes_data = thes_response.json()
        
        if thes_data and isinstance(thes_data[0], dict):
            synonyms = ', '.join(thes_data[0].get('meta', {}).get('syns', [[]])[0])
            antonyms = ', '.join(thes_data[0].get('meta', {}).get('ants', [[]])[0])
    
    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed for word '{word}': {str(e)}")
    except (IndexError, KeyError) as e:
        logging.error(f"Data parsing error for word '{word}': {str(e)}")
    except Exception as e:
        logging.error(f"Unexpected error processing word '{word}': {str(e)}")
    
    return definition, part_of_speech, synonyms, antonyms

def process_vocabulary():
    df = pd.read_csv(CSV_FILE_PATH)
    df = df.drop_duplicates(subset=[df.columns[0]], keep='first')

    new_columns = [
        'Merriam-Webster Definition', 'YouGlish Link',
        'Part of Speech', 'Synonyms', 'Antonyms', 'Frequency of Use',
        'Personal Example', 'Review Date'
    ]

    for col in new_columns:
        if col not in df.columns:
            df[col] = ''

    for index, row in df.iterrows():
        word = row.iloc[0]
        logging.info(f"Processing word: {word}")
        
        definition, part_of_speech, synonyms, antonyms = get_merriam_webster_data(word)
        
        df.at[index, 'Merriam-Webster Definition'] = definition
        df.at[index, 'Part of Speech'] = part_of_speech
        df.at[index, 'Synonyms'] = synonyms
        df.at[index, 'Antonyms'] = antonyms
        df.at[index, 'YouGlish Link'] = f'https://youglish.com/pronounce/{word}/english?'
        df.at[index, 'Frequency of Use'] = get_word_frequency(word)
        df.at[index, 'Review Date'] = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
        
        time.sleep(1)

    df.to_csv(PROCESSED_CSV_FILE_PATH, index=False)
    logging.info(f"Processed CSV file saved successfully at {PROCESSED_CSV_FILE_PATH}!")

if __name__ == "__main__":
    process_vocabulary()
