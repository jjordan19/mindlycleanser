from flask import Flask, render_template, url_for, request, session, redirect, flash, Blueprint
import bcrypt
from . import app

bp = Blueprint('auth', __name__, template_folder='templates')

@bp.route("/signup")
def signup():
    return render_template('signup.html')
