import os
from dotenv import load_dotenv


def load_config(env=".env"):
    try:
      # Grabs the folder where the script runs.
      basedir = os.path.abspath(os.path.dirname(__file__))
      load_dotenv(os.path.join(basedir, env))
    except Exception as err :
      print(f'[load_config] {err}')

def isNoneOrEmpty(string) :
  return not (string and string.isspace)
