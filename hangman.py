from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necessary for session management

word_list = [
    ["guitar", "A musical instrument with strings"],
    ["python", "A popular programming language"],
    ["piano", "A musical instrument with keys"],
    ["elephant", "The largest land animal"],
    ["chocolate", "A sweet treat made from cacao beans"],
    ["computer", "An electronic device for processing data"],
    ["football", "A popular team sport played with a round ball"],
    ["mountain", "A large natural elevation of the Earth's surface"],
    ["ocean", "A vast body of salt water covering most of the Earth"],
    ["sunflower", "A tall plant with a large yellow flower"],
    ["astronaut", "A person trained to travel in space"],
    ["bookstore", "A retail shop that sells books"],
    ["butterfly", "An insect with colorful wings"],
    ["volcano", "An opening in the Earth's crust that erupts lava"],
    ["skyscraper", "A tall, continuously habitable building"],
    ["parachute", "A device used to slow descent from the air"],
    ["chandelier", "A decorative hanging light fixture"],
    ["telescope", "An optical instrument for viewing distant objects"],
    ["zebra", "A wild animal known for its black and white stripes"],
    ["whale", "The largest marine mammal"],
    ["balloon", "A flexible bag filled with air or gas"],
    ["chess", "A strategic board game for two players"],
    ["rainbow", "A spectrum of light appearing in the sky"],
    ["jungle", "A dense forest in a tropical area"],
    ["cactus", "A plant that grows in dry, desert conditions"],
    ["kangaroo", "A large marsupial from Australia"],
    ["giraffe", "The tallest land animal"],
    ["horizon", "The line where the earth's surface and the sky appear to meet"],
    ["dragon", "A mythical creature often depicted as a large lizard"],
    ["mermaid", "A mythical sea creature with a human upper body and fish tail"],
    ["robot", "A machine capable of carrying out complex actions automatically"],
    ["skeleton", "The framework of bones supporting the body"],
    ["dinosaur", "A prehistoric reptile that lived millions of years ago"],
    ["rainforest", "A dense forest rich in biodiversity and high rainfall"],
    ["fireworks", "Explosive devices used for entertainment, especially during celebrations"],
    ["carnival", "A festival featuring parades, games, and entertainment"],
    ["pyramid", "A monumental structure with a square base and triangular sides"],
    ["glacier", "A large mass of ice that moves slowly down a mountain"],
    ["carousel", "A rotating amusement ride with seats often resembling animals"],
    ["safari", "An expedition to observe or hunt animals in their natural habitat"],
    ["kaleidoscope", "An optical instrument with mirrors and colored glass that creates changing patterns"],
    ["tornado", "A rapidly rotating column of air that extends from a thunderstorm"],
    ["labyrinth", "A complicated network of paths or passages"],
    ["symphony", "A long musical composition for an orchestra"],
    ["neighborhood", "A district or community within a town or city"],
    ["carnivore", "An animal that primarily eats meat"],
    ["herbivore", "An animal that primarily eats plants"],
    ["omnivore", "An animal that eats both plants and meat"],
    ["cryptocurrency", "A digital or virtual currency secured by cryptography"],
    ["puzzle", "A game or problem that requires thought and effort to solve"],
    ["hologram", "A three-dimensional image formed by the interference of light beams"],
    ["artichoke", "A vegetable with edible buds and leaves"],
    ["espresso", "A strong coffee brewed by forcing steam through finely ground coffee beans"],
    ["quicksand", "A loose, wet sand that can trap objects"],
    ["pomegranate", "A fruit with a tough skin and many seeds inside"],
]

list_emoji = ["💀", "😢", "😄", "😂"]

# Home route
@app.route('/')
def index():
    return render_template("main.html")

# Game initialization route
@app.route('/game')
def game():
    # Initialize session variables for the game if they don't exist
    if 'used_words' not in session:
        session['used_words'] = []
        session['lifeline'] = 3
        session['score'] = 0

    return start_new_round()

def start_new_round():
    # Choose a random word
    word = random.choice(word_list)

    # Check if the word has been used already
    if word[0] in session['used_words']:
        return start_new_round()  # Recursion to get a new word if already used

    # Store the current word in the session
    session['current_word'] = word[0]
    session['current_clue'] = word[1]
    session['used_words'].append(word[0])

    # Render the game page
    return render_template("game.html",
                           clue=word[1],
                           lifeline=session['lifeline'],
                           score=session['score'],
                           max_size=len(word[0]),
                           emoji=list_emoji[session['lifeline']])

# Route to handle guesses
@app.route("/submit", methods=['POST'])
def submit():
    guess = request.form.get('guess').strip().lower()  # Get the guess from the form
    current_word = session['current_word']

    # Check if the guess is correct
    if guess == current_word:
        session['score'] += 1  # Increment the score for a correct guess
        return redirect(url_for('game'))  # Start a new round

    # Wrong guess logic
    session['lifeline'] -= 1  # Decrease the lifeline on a wrong guess

    # Check if the game is over
    if session['lifeline'] <= 0:
        message = "Game over! Your score: {}. Better luck next time!".format(session['score'])
        return render_template('game_over.html', score=session['score'], message=message, correct_word=current_word)  # Game over page

    # Render the game page again with updated lifeline and score
    return render_template("game.html",
                           clue=session['current_clue'],
                           lifeline=session['lifeline'],
                           score=session['score'],
                           max_size=len(current_word),
                           emoji=list_emoji[session['lifeline']])

@app.route('/restart')
def restart():
    session.clear()  # Clear session data
    return redirect(url_for('game'))  # Restart the game

if __name__ == '__main__':
    app.run(debug=True)
