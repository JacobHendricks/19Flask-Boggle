from boggle import Boggle
from flask import Flask, render_template, request, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from boggle import *

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

boggle_game = Boggle()


# @app.route("/")
# def start_page():
#     """Return Start Page."""

#     return render_template("start.html")


# @app.route("/begin", methods=["POST"])
# def start_game():
#     """Clear the session of responses and add new board"""

#     session["board"] = boggle_game.make_board()

#     return redirect("/game")


# @app.route("/game")
# def game():
#     """Return boogle board."""
#     highscore = session.get("highscore", 0)
#     nplays = session.get("nplays", 0)
#     return render_template("game.html", board=session["board"], highscore=highscore, nplays=nplays)

@app.route("/")
def homepage():
    """Show board."""

    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    return render_template("index.html", board=board,
                           highscore=highscore,
                           nplays=nplays)


@app.route("/check-word")
def check_word():
    """Check if word is in dictionary."""

    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result': response})


@app.route("/post-score", methods=["POST"])
def post_score():
    """Receive score, update nplays, update high score if appropriate."""

    score = request.json["score"]
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    session['nplays'] = nplays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)
