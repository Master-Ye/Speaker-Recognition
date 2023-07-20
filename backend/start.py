import base64
import io
import json
import random
import matplotlib.pyplot as plt
import librosa
import mysql.connector
import numpy
import pymysql.cursors
from PIL.Image import Image

from speechbrain.pretrained import SepformerSeparation as separator
import torchaudio
from flask_cors import CORS, cross_origin
from torchaudio import transforms
from werkzeug.utils import secure_filename

from flask import Flask, request, send_file, Response, make_response, jsonify

import os
import argparse, glob, os, torch, warnings, time
from tools import *

from ECAPAModel import ECAPAModel
db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="jiweijian",
  database="runoob"
)
parser = argparse.ArgumentParser(description = "ECAPA_trainer")
## Training Settings
parser.add_argument('--num_frames', type=int,   default=200,     help='Duration of the inumpyut segments, eg: 200 for 2 second')
parser.add_argument('--max_epoch',  type=int,   default=80,      help='Maximum number of epochs')
parser.add_argument('--batch_size', type=int,   default=400,     help='Batch size')
parser.add_argument('--n_cpu',      type=int,   default=4,       help='Number of loader threads')
parser.add_argument('--test_step',  type=int,   default=1,       help='Test and save every [test_step] epochs')
parser.add_argument('--lr',         type=float, default=0.001,   help='Learning rate')
parser.add_argument("--lr_decay",   type=float, default=0.97,    help='Learning rate decay every [test_step] epochs')

## Training and evaluation path/lists, save path



parser.add_argument('--save_path',  type=str,   default="E:/datainit/exps/exp1",                                     help='Path to save the score.txt and models')
parser.add_argument('--initial_model',  type=str,   default="C:/Users/j1813/Desktop/ECAPA/model_0017.model",                                          help='Path of the initial_model')

## Model and Loss settings
parser.add_argument('--C',       type=int,   default=1024,   help='Channel size for the speaker encoder')
parser.add_argument('--m',       type=float, default=0.2,    help='Loss margin in AAM softmax')
parser.add_argument('--s',       type=float, default=30,     help='Loss scale in AAM softmax')
parser.add_argument('--n_class', type=int,   default=5994,   help='Number of speakers')

## Command
parser.add_argument('--eval',    dest='eval', action='store_true', help='Only do evaluation')

## Initialization
warnings.simplefilter("ignore")
torch.multiprocessing.set_sharing_strategy('file_system')
args = parser.parse_args()
args = init_args(args)




## Search for the exist models
modelfiles = glob.glob('%s/model_0*.model'%args.model_save_path)
modelfiles.sort()
model = separator.from_hparams(source="speechbrain/sepformer-whamr-enhancement", savedir='pretrained_models/sepformer-whamr-enhancement',run_opts={"device":"cuda"})
app = Flask(__name__) #记住这里的变量名app
CORS(app, resources={r"/*": {"origins": "*"}})
s = ECAPAModel(**vars(args))
print("Model %s loaded from previous state!" % args.initial_model)
s.load_parameters(args.initial_model)
@app.route('/denoise', methods=['POST'])
@cross_origin()
def denoise():
    uploaded_file = request.files['file']

    filename = secure_filename(uploaded_file.filename)
    filepath = os.path.join('upload', filename)


    # Check if file with the same name already exists in the directory


    uploaded_file.save(filepath)
    est_sources = model.separate_file(path=filepath)

    torchaudio.save("modified.wav", est_sources[:, :, 0].detach().cpu(), 8000)
    return send_file('modified.wav', "/upload/modified.wav")





@app.route('/upload2', methods=['POST'])
@cross_origin()
def upload2():
    uploaded_file1 = request.files['file1']
    uploaded_file2 = request.files['file2']
    filename1 = secure_filename(uploaded_file1.filename)
    filepath1 = os.path.join('uploads', filename1)
    filename2 = secure_filename(uploaded_file2.filename)
    filepath2 = os.path.join('uploads', filename2)

    # Check if file with the same name already exists in the directory
    uploaded_file1.save(filepath1)


    uploaded_file2.save(filepath2)

    res=s.cmp2(filepath1, filepath2)
    t = {
        'res1': res.tolist()
    }
    return json.dumps(t)



@app.route('/upload', methods=['POST'])
@cross_origin()
def upload():
    uploaded_file1 = request.files['file1']
    uploaded_file2 = request.files['file2']
    filename1 = secure_filename(uploaded_file1.filename)
    filepath1 = os.path.join('uploads', filename1)
    filename2 = secure_filename(uploaded_file2.filename)
    filepath2 = os.path.join('uploads', filename2)

    # Check if file with the same name already exists in the directory


    uploaded_file1.save(filepath1)
    est_sources = model.separate_file(path=filepath1)
    modified_file_path1 = 'modified1.wav'
    torchaudio.save("modified1.wav", est_sources[:, :, 0].detach().cpu(), 8000)



    uploaded_file2.save(filepath2)
    est_sources = model.separate_file(path=filepath2)
    modified_file_path2 = 'modified2.wav'
    torchaudio.save("modified2.wav", est_sources[:, :, 0].detach().cpu(), 8000)
    # Read the modified file and return it as a response to the client
    res=s.cmp2("modified1.wav", "modified2.wav")
    t = {
        'res1': res.tolist()
    }
    return json.dumps(t)


@app.route('/upload-audio', methods=['POST'])
def upload_audio():

        # 获取音频文件二进制数据
        audio = request.files['audio'].read()

        # 连接 MySQL 数据库


        # 存储音频数据到 MySQL 数据库中
        with db.cursor() as cursor:
            sql = 'INSERT INTO audio () VALUES (%s)'
            cursor.execute(sql, (audio,))
            db.commit()

        return jsonify({'message': 'Audio file uploaded successfully'})

@app.route('/add', methods=['POST'])
@cross_origin()
def add():
    id_list = request.form.getlist('id')
    cursor = db.cursor()

    for id in id_list:
        file = request.files.get(f'file_{id}')
        gender = request.form.get(f'gender_{id}')
        email = request.form.get(f'email_{id}')
        location = request.form.get(f'location_{id}')
        age = request.form.get(f'age_{id}')
        phone = request.form.get(f'phone_{id}')
        symbol1, symbol2 = s.getSymbol(file)
        symbol1, symbol2 = json.dumps(symbol1.tolist()), json.dumps(symbol2.tolist())
        sql = "INSERT INTO voiceprint (name,symbol1,symbol2,gender,email,location,age,phone) VALUES (%s, %s,%s, %s,%s,%s,%s,%s)"
        val = (id, symbol1, symbol2, gender, email, location, age, phone)
        cursor.execute(sql, val)
    db.commit()

    t = {
        'res1': "请求成功"
    }
    return jsonify(t)



@app.route('/all', methods=['POST'])
@cross_origin()
def all():
    cursor = db.cursor()
    sql = "SELECT name, email, phone, location, age, gender FROM voiceprint"
    cursor.execute(sql)
    results = cursor.fetchall()
    users = []

    for row in results:
        user = {
            'name': row[0],
            'email': row[1],
            'phone': row[2],
            'location': row[3],
            'age': row[4],
            'gender': row[5]
        }
        users.append(user)

        # 将数据转换为JSON格式并返回
    return jsonify(users)

def mask_along_axis(x, dim):
    freq_mask_width = (0, 8)
    time_mask_width = (0, 10)
    original_size = x.shape
    batch, fea, time = x.shape
    if dim == 1:
        D = fea
        width_range = freq_mask_width
    else:
        D = time
        width_range = time_mask_width

    mask_len = torch.randint(width_range[0], width_range[1], (batch, 1), device=x.device).unsqueeze(2)
    mask_pos = torch.randint(0, max(1, D - mask_len.max()), (batch, 1), device=x.device).unsqueeze(2)
    arange = torch.arange(D, device=x.device).view(1, 1, -1)
    mask = (mask_pos <= arange) * (arange < (mask_pos + mask_len))
    mask = mask.any(dim=1)

    if dim == 1:
        mask = mask.unsqueeze(2)
    else:
        mask = mask.unsqueeze(1)

    x = x.masked_fill_(mask, 0.0)
    return x.view(*original_size)
def forward(x):
    x = mask_along_axis(x, dim=2)
    x = mask_along_axis(x, dim=1)
    return x
@app.route('/enhance', methods=['POST'])
@cross_origin()
def enhance():
    file = request.files['file']
    waveform, sample_rate = torchaudio.load(file)

    # Apply mel spectrogram transformation
    mel_transform = torchaudio.transforms.MelSpectrogram(sample_rate=16000, n_fft=512, win_length=400, hop_length=160, \
                                                         f_min=20, f_max=7600, window_fn=torch.hamming_window,
                                                         n_mels=80)  # (sample_rate=sample_rate, n_mels=80)
    mel_spec_tensor = mel_transform(waveform)
    spec = transforms.AmplitudeToDB(top_db=80)(mel_spec_tensor)

    mel_specc = numpy.squeeze(spec, axis=0)

    mel_spec_tensor = forward(mel_spec_tensor)
    spec = transforms.AmplitudeToDB(top_db=80)(mel_spec_tensor)

    mel_specc = numpy.squeeze(spec, axis=0)
    print(type(mel_specc))
    # 显示图像
    plt.imshow(mel_specc, origin="lower")
    plt.colorbar()
    plt.ylabel('HZ')
    plt.xlabel('时间/s')
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.clf()
    return Response(buffer.getvalue(), mimetype='image/png')
@app.route('/orgin', methods=['POST'])
@cross_origin()
def orgin():
    file = request.files['file']
    waveform, sample_rate = torchaudio.load(file)

    # Apply mel spectrogram transformation
    mel_transform = torchaudio.transforms.MelSpectrogram(sample_rate=16000, n_fft=512, win_length=400, hop_length=160, \
                                                         f_min=20, f_max=7600, window_fn=torch.hamming_window,
                                                         n_mels=80)  # (sample_rate=sample_rate, n_mels=80)
    mel_spec_tensor = mel_transform(waveform)
    spec = transforms.AmplitudeToDB(top_db=80)(mel_spec_tensor)

    mel_specc = numpy.squeeze(spec, axis=0)

    # 显示图像
    plt.imshow(mel_specc, origin="lower", cmap="jet")
    plt.colorbar()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.clf()
    return Response(buffer.getvalue(), mimetype='image/png')





@app.route('/search', methods=['POST'])
@cross_origin()
def search():

    file = request.files.get('file')

    symbol1,symbol2=s.getSymbol(file)

    mycursor = db.cursor()
    mycursor.execute("SELECT name, symbol1,symbol2 FROM voiceprint")
    rows = mycursor.fetchall()
    tensors = []
    best_id = None
    best_score = -1
    for row in rows:
        # 将记录的 symbol1 和 symbol2 字段值转化为张量
        tensor1 = torch.from_numpy(numpy.array(json.loads(row[1]))).type(torch.float32)
        tensor2 = torch.from_numpy(numpy.array(json.loads(row[2]))).type(torch.float32)
        tensor1 = tensor1.cuda()
        tensor2 = tensor2.cuda()
        print(best_id)
        print( best_score)
        score_1 = torch.mean(torch.matmul(symbol1, tensor1.T))
        score_2 = torch.mean(torch.matmul(symbol2, tensor2.T))
        sscore = (score_1 + score_2) / 2
        score = sscore.detach().cpu().numpy()


        # 更新最佳匹配
        if score > best_score:
            best_id = row[0]
            best_score = score

    # 输出最佳匹配
    print('Best match: id =', best_id, ', score =', best_score)

    # 提交更改


    t = {
        'res1': "请求成功",
        "id":best_id,
        "score":best_score.tolist()
    }
    return json.dumps(t)
@app.route('/search3', methods=['POST'])
@cross_origin()
def search3():

    file = request.files.get('file')

    symbol1,symbol2=s.getSymbol(file)

    mycursor = db.cursor()
    mycursor.execute("SELECT name, symbol1, symbol2 FROM voiceprint")
    rows = mycursor.fetchall()
    tensors = []
    best_ids = []
    best_scores = [-1, -1, -1]  # Initialize with -1s so we can compare against them
    for row in rows:
        # 将记录的 symbol1 和 symbol2 字段值转化为张量
        tensor1 = torch.from_numpy(numpy.array(json.loads(row[1]))).type(torch.float32)
        tensor2 = torch.from_numpy(numpy.array(json.loads(row[2]))).type(torch.float32)
        tensor1 = tensor1.cuda()
        tensor2 = tensor2.cuda()
        score_1 = torch.mean(torch.matmul(symbol1, tensor1.T))
        score_2 = torch.mean(torch.matmul(symbol2, tensor2.T))
        sscore = (score_1 + score_2) / 2
        score = sscore.detach().cpu().numpy()

        # 更新最佳匹配
        for i in range(3):
            if score > best_scores[i]:
                best_ids.insert(i, row[0])
                best_scores.insert(i, score)
                break

    # 输出前三个最佳匹配
    for i in range(3):
        print('Rank:', i + 1, ', ID:', best_ids[i], ', Score:', best_scores[i])

    # 提交更改
    t = {
        'res1': '请求成功',
        'id1': best_ids[0],
        'score1': best_scores[0].tolist(),
        'id2': best_ids[1],
        'score2': best_scores[1].tolist(),
        'id3': best_ids[2],
        'score3': best_scores[2].tolist()
    }
    return json.dumps(t)
if __name__ == '__main__':
    app.run(debug=True,use_reloader=False)
