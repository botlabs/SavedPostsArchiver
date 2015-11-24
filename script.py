import praw
import requests

# Account settings (private)
USERNAME = ''
PASSWORD = ''

# OAuth settings (private)
CLIENT_ID = ''
CLIENT_SECRET = ''
REDIRECT_URI = 'http://127.0.0.1:65010/authorize_callback'

# Settings
OUTFILE = 'saved.txt'
USER_AGENT = "Saved posts archiver"
AUTH_TOKENS = ["identity","history"]

def get_access_token():
    response = requests.post("https://www.reddit.com/api/v1/access_token",
      # client id and client secret are obtained via your reddit account
      auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET),
      # provide your reddit user id and password
      data = {"grant_type": "password", "username": USERNAME, "password": PASSWORD},
      # you MUST provide custom User-Agent header in the request to play nicely with Reddit API guidelines
      headers = {"User-Agent": USER_AGENT})
    response = dict(response.json())
    return response["access_token"]

def get_praw():
    r = praw.Reddit(USER_AGENT)
    r.set_oauth_app_info(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
    r.set_access_credentials(set(AUTH_TOKENS), get_access_token())
    return r

def main(r):
    try:
        with open(OUTFILE, 'w', encoding='UTF-8') as f:
            for item in r.user.get_saved(limit=None):
                f.write(item.permalink + "\n")
    except praw.errors.OAuthInvalidToken:
        # print("Retrieving new token...")
        # r = get_praw()
        print("Fatal: Token expired while retrieving saved objects.")

if __name__ == "__main__":
    main(get_praw())
