import re
import pickle
from flask import Flask, request, jsonify, render_template


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('main.html')



def preprocess(text):
    '''This function preprocesses the text'''
    preprocessed_text = []
    text = text.replace('\\r', ' ')
    text = text.replace('\\"', ' ')
    text = text.replace('\\n', ' ')
    text = re.sub('[^A-Za-z0-9]+', ' ', text)
    # https://gist.github.com/sebleier/554280
    #sentance = ' '.join(e for e in sentance.split() if e.lower() not in stopwords)
    preprocessed_string = text.lower().strip()

    return preprocessed_string


def vectorize(text):
    '''This function takes the text and vectorizes ithe text using keras vectorizer.pkl'''
   
    vectorizer =  pickle.load(open('vectorizer.pkl', 'rb'))
    #preprocessed_string = [preprocessed_string]
    final = vectorizer.transform([text])
    
    return final


@app.route('/predict',methods=['POST'])
def predict():
    '''This function predicts the class(real or fake)'''
    #text = ''
    #if request.method == 'POST':
    text = request.form.values()
    for i in text:
        text = i
        break
    
    text = preprocess(text)
    text = vectorize(text)
    
    predictor = pickle.load(open('classifier.pkl', 'rb'))
    prob = predictor.predict_proba(text)
    cls = predictor.predict(text)
    
    if cls[0] == 'fake':
        a = round(prob[0][0], 2)
    else:
        a = round(prob[0][1], 2)
        
    return render_template('main.html', prediction_text="The given Text is: {}".format(cls[0]), probability="Probability of given text being {} is: {}".format(cls[0], a))


#a = "missing details orlando shooting 911 transcrip"
#print(predict())
if __name__ == '__main__':
    app.run(debug=True)