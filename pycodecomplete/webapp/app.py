import sys
import pdb

#pdb.set_trace()
sys.path.append('..')

from flask import Flask, request, render_template, jsonify
from keras.models import load_model
from keras import Sequential

from ml.code_generation import CodeGenerator
from ml.process_text import CharVectorizer

'''
from .ml.code_generation import CodeGenerator
from ...process_text import CharVectorizer
'''
char_vec = CharVectorizer(sequence_length=100)
model = load_model('../trained-models/rnn')
code_gen = CodeGenerator(model, char_vec)


app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('template.html')

@app.route('/submit')
def submit():
    return '''
        <!DOCTYPE html><html><head></head>
            <form action="/predict" method='POST' >
                <input type="text" name="user_input" />
                <input type="submit" />
            </form>
        </html>
        '''

@app.route('/submit-predict', methods=['POST'])
def sub_pre_ajax():
    user_data = request.json
    text = str(user_data['text'])

    #with open('model.pkl', 'rb') as f:
    #    model = pickle.load(f)
        
    prediction = code_gen.predict_n_with_previous(text, 10)
    print(code_gen)
    return jsonify({'prediction': text})

@app.route('/predict', methods=['POST'])
def predict():
    text = str(request.form['user_input'])

    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
        
    prediction = model.predict([text])[0] 

    return f'''
        <!DOCTYPE html>
        <html>
            <head>
            </head>
            <body>
                {prediction}
            </body>
        </html>'''
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)