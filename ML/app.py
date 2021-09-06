from flask import Flask,render_template,url_for,request, jsonify
import os
import pickle
import json
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import textclassifier
import nltk
import TranscribeTranslate as TT
from werkzeug.utils import secure_filename

app = Flask(__name__)
models={}
for i in range(0,2):
    temp_str="model"+(str)(i+1)+".pkl"
    temp_str2="model"+(str)(i+1)
    x=pickle.load(open(temp_str,'rb'))
    models[temp_str2]=x

cv=pickle.load(open('vec.pkl','rb'))
secret="admin123admin"
app.config['UPLOAD_FOLDER']='uploads_python'
app.config['MAX_CONTENT_LENGTH']=25*1024*1024

@app.route('/predict_text',methods=['POST'])
def predict_text():
    if 'api_key' not in request.args:
        return "API_KEY_MISSING"
    else:
        api_key= request.args['api_key']
        global secret

        if not api_key==secret:
            return "INVALID_API_KEY"

        global models
        global cv
        
        if 'message' not in request.json:
            return "MESSAGE_MISSING"
        if 'userid' not in request.args:
            return "USER_ID_MISSING"

        message=request.json["message"]
        userid=request.args["userid"]

        lang=TT.detect_language(message)

        if lang=="hi":
            message_translit=TT.transliterate_text(message, target='hi')
            message_translation=TT.translate_text(message_translit)
        else:
            message_translation=message
        message_translation_preprocessed=textclassifier.utils_preprocess_text(message_translation,False,True,nltk.corpus.stopwords.words("english"))
        data =[message_translation_preprocessed] #list
        #Note that vect=cv.transform(data) is <class 'scipy.sparse.csr.csr_matrix'>
        vect=cv.transform(data).toarray() #numpy.ndarray
        temp_model_name="model"+(str)(userid)
        my_prediction = models[temp_model_name].predict(vect)
        d={}
        d["msg"]=message
        d["pred"]=(int)(my_prediction[0])
        if lang=="hi":
            d["msg_translation"]=message_translation
        print(d)
        return jsonify(d)

@app.route('/predict_audio',methods=['POST'])
def predict_audio():
    if 'api_key' not in request.args:
        return "API_KEY_REQUIRED"
    else:
        api_key= request.args['api_key']
        global secret
        if not api_key==secret:
            return "INVALID_API_KEY"

        global models
        global cv

        if 'file' not in request.files:
            return "AUDIO_FILE_MISSING"
        if 'userid' not in request.args:
            return "USER_ID_MISSING"

        f = request.files['file']
        userid=request.args['userid']

        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        audio_path=os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
        transcript_tup = TT.transcribe_audio(file_input=audio_path)

        message=transcript_tup[0]
        msg_lang_code=transcript_tup[1]

        if msg_lang_code[0:2]=="hi":
            message_translation=TT.translate_text(message)
        elif msg_lang_code[0:2]=="en":
            message_translation=message

        message_translation_preprocessed=textclassifier.utils_preprocess_text(message_translation,False,True,nltk.corpus.stopwords.words("english"))
        data =[message_translation_preprocessed] #list
        #Note that vect=cv.transform(data) is <class 'scipy.sparse.csr.csr_matrix'>
        vect=cv.transform(data).toarray() #numpy.ndarray
        temp_model_name="model"+(str)(userid)
        my_prediction = models[temp_model_name].predict(vect)
        d={}
        d["msg"]=message
        d["pred"]=(int)(my_prediction[0])
        if msg_lang_code[0:2]=="hi":
            d["msg_translation"]=message_translation
        print(d)
        return jsonify(d)


@app.route('/train',methods=['GET','POST'])
def train():
    if 'api_key' not in request.args:
        return "API_KEY_REQUIRED"
    else:
        api_key= request.args['api_key']
        global secret
        if not api_key==secret:
            return "INVALID_API_KEY"

        global models
        global cv

        if 'message' not in request.args:
            return "MESSAGE_MISSING"
        if 'feedback' not in request.args:
            return "FEEDBACK_MISSING"
        if 'userid' not in request.args:
            return "USER_ID_MISSING"

        message = request.args['message']
        userid = request.args['userid']
        feedback = request.args['feedback']

        message_preprocessed=textclassifier.utils_preprocess_text(message,False,True,nltk.corpus.stopwords.words("english"))
        rectpred= np.array([(int)(feedback)])
        d={}
        d["trained_msg"]= message
        d["rect_pred"]=(int)(request.args['feedback'])
        data=[message_preprocessed]
        #cv.partial_refit(data) 
        #just to learn new features or vocabulary
        vect=cv.transform(data).toarray()
        temp_model_name="model"+(str)(userid)
        models[temp_model_name].partial_fit(vect,rectpred)
        print(d)
        return "Trained"
    

@app.route('/quit',methods=['GET'])
def quit():
    if 'api_key' not in request.args:
        return "API_KEY_REQUIRED"
    else:
        api_key= request.args['api_key']
        global secret
        if not api_key==secret:
            return "INVALID_API_KEY"
            
        global models
        for i in range(0,2):
            temp_model_name="model"+(str)(i+1)
            temp_model_pickle="model"+(str)(i+1)+".pkl"
            pickle.dump(models[temp_model_name], open(temp_model_pickle,'wb'))
    
        return "Quit"


if __name__ == '__main__':
    app.run(port=8080,debug=True)
    #app.run(debug=True)
    #using waitress as the production WSGI server
    #from waitress import serve
    #print("Serving on localhost:5000")
    #serve(app, host="localhost", port=5000)
