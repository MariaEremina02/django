import os
from pathlib import Path

import environ

env = environ.Env(DEBUG=(bool, False))

BASEDIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(BASEDIR.joinpath('.env'))

