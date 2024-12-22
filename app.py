import pymongo
from flask import Flask, render_template, request, redirect
from random import *

app = Flask('jumbledwords')

client = pymongo.MongoClient("localhost:27017")
db = client['jumbledwords']

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        print(request.form)
        doc={}
        doc['word']=request.form['word'].strip()
        print(doc)
        db.words.insert_one(doc)
        return redirect('/')


@app.route('/play', methods = ['GET','POST'])
def play():
    find = db.words.find({})
    words = [x for x in find]
    
    correctwords = words[:]
    
    if request.method == 'GET':
        for w in words:
            a = list(w['word'])
            shuffle(a)
            b = ''.join(a)
            w['word'] = b
        
     
        print('hi',words)
        return render_template('play_game.html', words = words)
    if request.method == 'POST':
        score = 0
        wordlist = dict(request.form.items())
        guess = [wordlist[x] for x in wordlist]
        
        l = len(guess)

        for i in range(l):
            if guess[i] == correctwords[i]['word']:
                score += 1

        return render_template('result.html', score = score, correct = correctwords, guess = guess)

    

app.run(debug=True)
