import os
import sys
from dotenv import load_dotenv


def load_config(env=".env"):
    # Grabs the folder where the script runs.
    basedir = os.path.abspath(os.path.dirname(__file__))

    load_dotenv(os.path.join(basedir, env))


def isNoneOrEmpty(string) :
  return not (string and string.isspace)
