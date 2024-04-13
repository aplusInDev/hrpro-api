#!/usr/bin/env python3

from flask import jsonify, request
from api.v1.views import app_views

@app_views.route('/query-example', methods=['GET'])
def query_example():
    # if key doesn't exist, returns None
    language = request.args.get('language')

    # if key doesn't exist, returns a 400, bad request error
    framework = request.args['framework']

    # if key doesn't exist, returns None
    website = request.args.get('website')

    # return jsonify({"test": "ok"})
    # try http://127.0.0.1:5000/api/v1/query-example?language=Python&framework=Flask&website=DigitalOcean
    return jsonify({'language': language, 'framework': framework, 'website': website})

# allow both GET and POST requests
@app_views.route('/form-example', methods=['GET', 'POST'])
def form_example():
    # handle the POST request
    if request.method == 'POST':
        language = request.form.get('language')
        framework = request.form.get('framework')
        return '''
                  <h1>The language value is: {}</h1>
                  <h1>The framework value is: {}</h1>'''.format(language, framework)

    # otherwise handle the GET request
    return '''
           <form method="POST">
               <div><label>Language: <input type="text" name="language"></label></div>
               <div><label>Framework: <input type="text" name="framework"></label></div>
               <input type="submit" value="Submit">
           </form>'''

@app_views.route('/new_form', methods=['POST'])
def post_new_form():
    data = request.form
    return jsonify(data)
