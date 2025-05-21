from flask import Blueprint, render_template, request, redirect, url_for
from app import db

user = Blueprint('user', __name__)  # Define the Blueprint

@user.route('/')
def index():
    return "Selamat Datang!"  # Return a simple response