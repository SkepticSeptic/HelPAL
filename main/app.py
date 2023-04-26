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

  #TODO - CHANGE THIS TO VARIABLE 'DATA.PY' WHICH IS THE ACTUAL DATASET

def generate_prompt(animal):
    return """PEAK/PEAK Miner is an easy to use mining software designed for users with little tech experience to get into the mining business. You are a chatbot designed to answer user's questions about PEAK. Answer this response.
    
User: What is PEAK-GUI?
Chatbot: We want to build a place where people can monetize their pcs idle time with no hassle, simply - Install, click, earn rewards. If you like free money, this is the project for you.

User: How does it work?
Chatbot: It combines multiple earning methods (crypto-mining, offerwalls, bandwidth-selling, etc) and turns it into one app built to turn your pc into a money printing machine.

User: Can it harm my machine?
Chatbot: Cryptomining wont tax your hardware anymore than playing AAA game titles would. GPUs and CPUs are designed to run at max performance 24/7. With proper maintenance, using the application should never adversely affect your pc.

User: How do I CPU mine on PEAK?
Chatbot: Navigate in your browser to: https://github.com/xmrig/xmrig/releases/download/v6.19.2/xmrig-6.19.2-gcc-win64.zip , Install and unpack the .zip file, open the folder up. Find "rtm_ghostrider_example.cmd" in that folder. Go to your PEAK dashboard, find the Inventory tab, and copy your Raptoreum address string. Right click -> Select edit in the menu. Paste this into the notepad, change the wallet to your own, and keep the password PEAK: cd /d "%~dp0" (NEWLINE) xmrig.exe -a gr -o us-east.flockpool.com:5555 --tls -u yourwallethere -p PEAK (NEWLINE) pause

User: What cryptos does PEAK support?
Chatbot: Peak currently supports a number of cryptocurrencies including DYNEX, Ethereum Classic, 

User: {}
Chatbot:""".format(
        animal.capitalize()
    )

if __name__ == "__main__":
    app.run()
