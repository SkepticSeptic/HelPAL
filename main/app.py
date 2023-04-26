import os
from datetime import datetime

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

def log_request(animal, response):
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_filename = f"{timestamp}.log"
    log_path = os.path.join(log_dir, log_filename)

    with open(log_path, 'w') as log_file:
        log_file.write(f"User Input: {animal}\n")
        log_file.write(f"GPT Output: {response}\n")

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        animal = request.form["animal"]

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(animal),
            temperature=0.6,
            max_tokens=250,
        )
        log_request(animal, response) #CREATE LOG
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(animal):
    return os.getenv("TRAINING_DATA").format(
        animal.capitalize()
    )

if __name__ == "__main__":
    app.run()
