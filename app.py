from flask import Flask
from flask import request
from flask import jsonify
module_path = ('/home/amitj/praat/')
import sys
import os
sys.path.append(module_path)
from calculate_data import calculate_data
import json

app = Flask(__name__)

@app.route('/alexapi', methods=['POST'])
def alexa_task():
    file = request.files['file']
    #import ipdb; ipdb.set_trace()
    filename = str(file.filename)
    file.save('current_data/'+file.filename)
    reply = {'msg':'Success'}
    sox_command = 'sox -r 16000 -e unsigned -b 16 -c 1 current_data/%s current_data/%s.wav'%(filename,filename[:-4])
    os.system(sox_command)
    with open('current_file.text','w+') as f:
        f.write(str(filename[:-4]))
    return jsonify({'reply':reply}), 201

@app.route('/lab',methods=['POST'])
def transcipt():
    data = json.loads(request.data)
    text = str(data['text'])
    text = text.upper()
    with open('current_file.text','r') as f:
        filename = f.read()
    with open('/tmp/dexter/'+filename+'.lab','w+') as f:
        f.write(text)
    os.system('mv current_data/%s.wav /tmp/dexter/'%filename)
    os.system('rm current_data/*')
    result = calculate_data(filename,'/tmp/dexter')
    os.system('rm /tmp/dexter/*')
    print result
    #TODO filter by timestamp
    #TODO create filename for lab file
    #TODO create lab file in the folder with .wav
    #TODO run calculate_data for filename and folder
    #TODO JSONIFY results and send to UI

@app.route('/result',methods=['GET'])
def result():
    import ipdb; ipdb.set_trace()
    with open('result.txt','r') as f:
        results = f.read().split(',')
    return json.dumps({'f1':results[0],'f2':results[1]})

if __name__ == '__main__':
    app.run(debug=True)
