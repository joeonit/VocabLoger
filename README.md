# Vocabulary Learning Tools

This repo contains tools to help build, automate and maintain loging vocabulary list to be used as flashcards.

## Planned Features

- Flashcard system for efficient review
- Spaced repetition algorithm for optimized learning
- Database integration for improved data management and querying

## Components

### 1. Vocabulary Logger (AppleScript)

`vocabulary_logger.scpt` is an AppleScript that logs selected words and the current date into a CSV file.

#### Usage:
1. Copy a word to your clipboard.
2. Run the script.
3. The word and timestamp will be logged to the CSV file.

### 2. Vocabulary Processor (Python)

`file_process.py` is a Python script that processes the logged vocabulary words, fetching definitions, synonyms, antonyms, and other useful information.

#### Features:
- Fetches definitions from Merriam-Webster API
- Adds YouGlish links for pronunciation
- Determines word frequency
- Adds review dates

## Setup

1. Install required Python packages:
```pip install pandas requests nltk```

2. Set up API keys:
- Get API keys from Merriam-Webster for both dictionary and thesaurus, you can get them for free after filing an applciton and signing up [here](https://dictionaryapi.com/)

- Replace the placeholders in `file_process.py` with your actual API keys

3. Update file paths in both scripts to match your local setup

## Usage

1. Use the AppleScript to log words regularly, It works by getting the last word from your clipboard, start by making an automator application then put the script inside the create app and export it finally assign a keyboard shortcut to the app so it los seamlessly 
2. Periodically run the Python script to process and enrich your vocabulary list

