from ancapp import app
from flask import Flask, render_template, url_for, request, redirect, session, g

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/login")
def index():
    pass
