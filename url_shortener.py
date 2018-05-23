"""
A simple URL shortener service that runs on Flask.

Each URL shortening request is assigned a unique_id which is used to 
generate the shortened URL. url_dict stores the mapping between shortened URL
and original URL.
"""

import base64
import flask
import threading
import urllib

app = flask.Flask(__name__)

# The host URL for our simple URL shortening service.
HOST_URL = "http://localhost:5000/"

# URL dictionary storing a maping between short_url to original URL.
url_dict = dict()

# Global unique ID used to create unique short URLs.
unique_id = 0
# Protects access to unique_id
lock = threading.RLock()

def int_to_bytes(x):
    return x.to_bytes((x.bit_length() + 7) // 8, "big")

def get_unique_urlsafe_string():
    global unique_id
    with lock:
        unique_id += 1
        encoded = base64.urlsafe_b64encode(int_to_bytes(unique_id))
        return encoded.decode("utf-8").rstrip("=")

@app.route("/", methods=["GET", "POST"])
def home():
    if flask.request.method == "GET":
        return flask.render_template("index.html")
    # POST request which creates the short_url given a URL.
    url = flask.request.form.get("url")
    if not urllib.parse.urlparse(url).scheme:
        url = "http://" + url
    short_url = get_unique_urlsafe_string()
    url_dict[short_url] = url
    return flask.render_template("index.html", short_url=HOST_URL + short_url)

@app.route("/<short_url>")
def redirect_short_url(short_url):
    return flask.redirect(url_dict.get(short_url, HOST_URL))

if __name__ == "__main__":
    app.run(debug=True)
