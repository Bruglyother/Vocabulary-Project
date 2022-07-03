#comments
'''
This is a program to be used by teachers for reinforcing vocabulary
'''

import random
import sqlite3

print('--------------------------------')
print('| Welcome to Vocabulary Games! |')
print('--------------------------------')
def create_list():
    # creates new word lists in a word database
    conn = sqlite3.connect('wordsdb.sqlite')
    cur = conn.cursor()

    cur.executescript('''

    CREATE TABLE IF NOT EXISTS words (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        word TEXT UNIQUE
    );

    CREATE TABLE IF NOT EXISTS lists (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        list TEXT UNIQUE
    );

    CREATE TABLE IF NOT EXISTS matchs (
        list_id INTEGER,
        word_id INTEGER,
        PRIMARY KEY (list_id, word_id)
    );

    ''')

    list_name = input('Enter a name for your list:')
    cur.execute('''INSERT OR IGNORE INTO lists (list)
        VALUES ( ? )''', ( list_name, ) )
    cur.execute('SELECT id FROM lists WHERE list = ? ', (list_name, ))
    list_id = cur.fetchone()[0]

    while True:
        word_name = input('Enter a new word or \'q\' to quit:')
        if word_name.lower() == 'q':
            break
        else:
            cur.execute('''INSERT OR IGNORE INTO words (word)
                VALUES ( ? )''', ( word_name, ) )
            cur.execute('SELECT id FROM words WHERE word = ? ', (word_name, ))
            word_id = cur.fetchone()[0]

            cur.execute('''INSERT OR REPLACE INTO matchs
                (list_id, word_id) VALUES ( ?, ? )''',
                ( list_id, word_id) )

            conn.commit()
    cur.close()
    print('Press eneter to continue!')
def random_word(words):
    # pulls a random word from a list
    x = random.randint(0,(len(words)-1))
    return words[x]
def find_wrdlst():
    # Pulls a wordlist from a db file
    conn = sqlite3.connect('wordsdb.sqlite')
    cur = conn.cursor()

    wrdlst = list()
    choices = list('0')
    sqlstr = 'SELECT id, list FROM lists ORDER BY id'
    print('0 All')
    for row in cur.execute(sqlstr):
        choices.append(str(row[0]))
        print(row[0], row[1])
    print('')
    choice = input('Please choose the list you wish to work from today:')
    while choice not in choices:
        choice = input('Invalid choice.  Please choose again:')
    if choice == '0':
        sqlstr = 'SELECT word FROM words ORDER BY id'
        for row in cur.execute(sqlstr):
            wrdlst.append(row[0])
    else:
        temp = list()
        choice = int(choice)
        sqlstr = 'SELECT word_id FROM matchs WHERE list_id = ?'
        for row in cur.execute(sqlstr, (choice,)):
            temp.append(row[0])
        for i in temp:
            for row in cur.execute('SELECT word from words WHERE id = ?',(i,)):
                wrdlst.append(row[0])
    cur.close()
    return wrdlst
def hangman(word):
    #hangman game
    trial = list()
    trial_word = ''
    for letter in word:
        trial.append('*')
        trial_word +='*'
    print('')
    print('Here is your word!')
    print(trial_word)
    attempts = 0
    guesses = ''
    while word != trial_word:
        guess = input('Guess a letter: ')
        if guess.isalpha() != True:
            print ('That is not a letter.')
            continue
        guess = guess.lower()
        if guess in guesses:
            print ('You have already guessed that letter.')
        elif guess not in word:
            guesses += guess
            attempts += 1
            if attempts < 10:
                print('Sorry,', guess,'is not in the word.  You have', (10-attempts), 'fails left.')
            elif attempts == 10:
                print('Sorry,', guess,'is not in the word.  You can not fail again.')
            else:
                print('You have failed to guess', word+'!')
                break
        else:
            guesses += guess
            trial_word = ''
            x=0
            for letter in word:
                if guess == word[x]:
                    trial[x]=guess
                    trial_word = trial_word + guess
                else:
                    trial_word = trial_word + trial[x]
                x+=1
        if word == trial_word:
            print('Congratulations!  You have guessed', word+'!')
        else:
            print(trial_word)
    input('Press enter to continue!')
def wordle(word):
    #wordle game
    trial = list()
    trial_word = ''
    for letter in word:
        trial.append('*')
        trial_word +='*'
    print('')
    print('Here is your word!')
    print(trial_word)
    attempts = 0
    guesses = ''
    while word != trial_word:
        if attempts == 5:
            break
        guess = input('Guess the word: ')
        if len(guess) != len(trial_word):
            print('Too many letters!  Please try again.')
            continue
        x=0
        trial_word = ''
        for letter in word:
            if guess[x] == word[x]:
                trial_word +=  word[x]
            elif guess[x] in word:
                trial_word +=  '?'
            else:
                trial_word += '*'
            x += 1
        attempts +=1
        print(trial_word)
    if trial_word == word:
        print('Congratulations!  You have guessed', word+'!')
    else:
        print('Oh no!  You failed to guess', word+'!')
    input('Press enter to continue!')

#table of contents
while True:
    print('''
    Please choose from the following options:
        H: Hangman game
        W: Wordle game
        C: Create Word List
        V: View a Word List
        Q: Quit
    ''')
    choice = input()
    print('')
    if choice.upper() == 'H':
        hangman(random_word(find_wrdlst()).lower())
    elif choice.upper() == 'W':
        wordle(random_word(find_wrdlst()).lower())
    elif choice.upper() == 'C':
        create_list()
    elif choice.upper() == 'V':
        wrdlst = find_wrdlst()
        for i in wrdlst:
            print(i)
    elif choice.upper() == 'Q':
        print ('Thank you for playing!')
        break
    else:
        print ('Invalid choice.')


# ToDo list:
'''
 Need a way to edit/delete existing word lists or words
 Table of contents - done...but expand as options added.
 Find new games to add
'''
