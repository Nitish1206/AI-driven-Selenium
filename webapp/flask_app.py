from flask import Flask, render_template, request,flash,redirect,url_for
import time


app = Flask(__name__)



@app.route('/')
def render_kyc_form():
    return render_template('index.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')




if __name__ == '__main__':
   

    app.run(host='0.0.0.0' , port=5000 , debug=True)
