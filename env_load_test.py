from datetime import datetime, timedelta, time as dt_time
from pytz import timezone
import pytz
import time
import random
from threading import Thread
from flask import Flask, render_template, redirect, url_for, flash, render_template_string
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
import redis
from flask import session
import os
from process import AskChatGPT
from dotenv import load_dotenv
import logging




load_dotenv()  # 加载 .env 文件
url = os.environ.get('URL')
secret_key = os.environ.get('SECRET_KEY')
print("url",url)
print("secret_key",secret_key)