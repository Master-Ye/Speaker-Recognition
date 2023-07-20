'''
This part is used to train the speaker model and evaluate the performances
'''

import torch, sys, os, tqdm, numpy, soundfile, time, pickle
import torch.nn as nn
from tools import *
from loss import AAMsoftmax
from model import ECAPA_TDNN


class ECAPAModel(nn.Module):
    def __init__(self, lr, lr_decay, C, n_class, m, s, test_step, **kwargs):
        super(ECAPAModel, self).__init__()
        ## ECAPA-TDNN
        self.speaker_encoder = ECAPA_TDNN(C=C).cuda()
        ## Classifier
        self.speaker_loss = AAMsoftmax(n_class=n_class, m=m, s=s).cuda()

        self.optim = torch.optim.Adam(self.parameters(), lr=lr, weight_decay=2e-5)
        self.scheduler = torch.optim.lr_scheduler.StepLR(self.optim, step_size=test_step, gamma=lr_decay)

    def forward(self, x):
        # 模型推理过程
        y = self.getSymbol(x)  # 调用 getsymbol 方法
        return y




    def outjug(self, find_file):
        self.eval()
        x = -1
        wav_path = "D:/2/test/wav/"
        wav_file = os.listdir(wav_path)
        f = open("D:/2/all_list.txt", 'w', encoding="utf-8")
        #find_file = "E:/datainit/test/wav/id10270/5r0dWxy17C8/00001.wav"
        cnt = 0
        for i, m4a in enumerate(wav_file):
            pathh = wav_path + m4a
            m4aa_file = os.listdir(pathh)
            for j, m4aa in enumerate(m4aa_file):
                pathhh = pathh + "/" + m4aa
                m4aaa_file = os.listdir(pathhh)
                for k, m4aaa in enumerate(m4aaa_file):
                    cnt = cnt + 1
                    #print("1 " + wav_path + m4a + "/" + m4aa + "/" + m4aaa + " " + find_file)
                    print("1 " + wav_path + m4a + "/" + m4aa + "/" + m4aaa + " " + find_file, file=f)
                    if (cnt % 3 == 0): break
                if (cnt % 3 == 0): break
        f.close()
        files = []
        embeddings = {}
        lines = open("D:/2/all_list.txt").read().splitlines()
        for line in lines:
            files.append(line.split()[1])
            files.append(line.split()[2])
        setfiles = list(set(files))
        setfiles.sort()
        for idx, file in tqdm.tqdm(enumerate(setfiles), total=len(setfiles)):
            audio, _ = soundfile.read(file)
            data_1 = torch.FloatTensor(numpy.stack([audio], axis=0)).cuda()
            max_audio = 300 * 160 + 240
            if audio.shape[0] <= max_audio:
                shortage = max_audio - audio.shape[0]
                audio = numpy.pad(audio, (0, shortage), 'wrap')
            feats = []
            startframe = numpy.linspace(0, audio.shape[0] - max_audio, num=5)
            for asf in startframe:
                feats.append(audio[int(asf):int(asf) + max_audio])
            feats = numpy.stack(feats, axis=0).astype(numpy.float)
            data_2 = torch.FloatTensor(feats).cuda()
            with torch.no_grad():
                embedding_1 = self.speaker_encoder.forward(data_1, aug=False)
                embedding_1 = F.normalize(embedding_1, p=2, dim=1)
                embedding_2 = self.speaker_encoder.forward(data_2, aug=False)
                embedding_2 = F.normalize(embedding_2, p=2, dim=1)
            embeddings[file] = [embedding_1, embedding_2]
        cnt = 0
        for line in lines:
            cnt = cnt + 1
            if(cnt % 3 == 1) : score = 0
            embedding_11, embedding_12 = embeddings[line.split()[1]]
            embedding_21, embedding_22 = embeddings[line.split()[2]]
            score_1 = torch.mean(torch.matmul(embedding_11, embedding_21.T))
            score_2 = torch.mean(torch.matmul(embedding_12, embedding_22.T))
            sscore = (score_1 + score_2) / 2
            score = score + sscore.detach().cpu().numpy()
            if(score > x) :
                x = score
                res = line.split()[1]
                res = res.split('/')[4]
        return res

    def outrate(self, file_path):
        wav_file = os.listdir(file_path)
        sum = 0
        cnt = 0
        for i, m4a in enumerate(wav_file):
            pathh = file_path + m4a  #file_path = "E:/datainit/test/wav/"
            m4aa_file = os.listdir(pathh)
            for j, m4aa in enumerate(m4aa_file):
                pathhh = pathh + "/" + m4aa
                m4aaa_file = os.listdir(pathhh)
                for k, m4aaa in enumerate(m4aaa_file):
                    fl = pathhh + "/" + m4aaa
                    print("fl =", fl)
                    sum = sum + 1
                    ss = self.outjug(fl)

                    print("fl->", fl.split('/')[4])
                    print("ss =", ss)
                    if(ss == fl.split('/')[4]) : cnt = cnt + 1

                    print("rate_now =", cnt / sum)
                    break ####
                break ####


        return cnt / sum

    def outrate1(self, wav_path):
        self.eval()
        wav_file = os.listdir(wav_path)
        x = -1
        sum = 0
        cnt = 0
        num = 0
        ll = []
        embeddings = {}
        for i, m4a in enumerate(wav_file):
            pathh = wav_path + m4a
            m4aa_file = os.listdir(pathh)
            for j, m4aa in enumerate(m4aa_file):
                pathhh = pathh + "/" + m4aa
                # print("pathhh =", pathhh)
                ttemp = pathhh[-3] + pathhh[-2] + pathhh[-1]
                if (ttemp != "wav"): continue
                num = num + 1
                ll.append(pathhh)
                if (num % 3 == 0): break
            for j, m4aa in enumerate(reversed(m4aa_file)):
                pathhh = pathh + "/" + m4aa
                # print("pathhh =", pathhh)
                ttemp = pathhh[-3] + pathhh[-2] + pathhh[-1]
                if (ttemp != "wav"): continue
                num = num + 1
                ll.append(pathhh)
                if (num % 3 == 0): break
        for file in ll:
            audio, _ = soundfile.read(file)

            print("file =", file)

            data_1 = torch.FloatTensor(numpy.stack([audio], axis=0)).cuda()
            max_audio = 300 * 160 + 240
            if audio.shape[0] <= max_audio:
                shortage = max_audio - audio.shape[0]
                audio = numpy.pad(audio, (0, shortage), 'wrap')
            feats = []
            startframe = numpy.linspace(0, audio.shape[0] - max_audio, num=5)
            for asf in startframe:
                feats.append(audio[int(asf):int(asf) + max_audio])
            feats = numpy.stack(feats, axis=0).astype(numpy.float)
            data_2 = torch.FloatTensor(feats).cuda()
            with torch.no_grad():
                embedding_1 = self.speaker_encoder.forward(data_1, aug=False)
                embedding_1 = F.normalize(embedding_1, p=2, dim=1)
                embedding_2 = self.speaker_encoder.forward(data_2, aug=False)
                embedding_2 = F.normalize(embedding_2, p=2, dim=1)
            embeddings[file] = [embedding_1, embedding_2]

        for i, m4a in enumerate(wav_file):
            pathh = wav_path + m4a
            m4aa_file = os.listdir(pathh)
            for j, m4aa in enumerate(m4aa_file):
                pathhh = pathh + "/" + m4aa
                ttemp = pathhh[-3] + pathhh[-2] + pathhh[-1]
                if (ttemp != "wav"): continue
                sum = sum + 1
                audio, _ = soundfile.read(pathhh)
                data_1 = torch.FloatTensor(numpy.stack([audio], axis=0)).cuda()
                max_audio = 300 * 160 + 240
                if audio.shape[0] <= max_audio:
                    shortage = max_audio - audio.shape[0]
                    audio = numpy.pad(audio, (0, shortage), 'wrap')
                feats = []
                startframe = numpy.linspace(0, audio.shape[0] - max_audio, num=5)
                for asf in startframe:
                    feats.append(audio[int(asf):int(asf) + max_audio])
                feats = numpy.stack(feats, axis=0).astype(numpy.float)
                data_2 = torch.FloatTensor(feats).cuda()
                with torch.no_grad():
                    embedding_21 = self.speaker_encoder.forward(data_1, aug=False)
                    embedding_21 = F.normalize(embedding_21, p=2, dim=1)
                    embedding_22 = self.speaker_encoder.forward(data_2, aug=False)
                    embedding_22 = F.normalize(embedding_22, p=2, dim=1)
                x = -1
                for k in ll:
                    embedding_11, embedding_12 = embeddings[k]
                    score_1 = torch.mean(torch.matmul(embedding_11, embedding_21.T))
                    score_2 = torch.mean(torch.matmul(embedding_12, embedding_22.T))
                    sscore = (score_1 + score_2) / 2
                    score = sscore.detach().cpu().numpy()
                    if (score > x):
                        x = score
                        print(k)
                        res = k.split('/')[2]
                print("find =", res, "answer =", pathhh.split('/')[2])
                if (res == pathhh.split('/')[2]): cnt = cnt + 1
                print("rate_now =", cnt / sum)
        return cnt / sum
    def cmp2(self, find_file1, find_file2):
        self.eval()
        files = []
        embeddings = {}
        files.append(find_file1)
        files.append(find_file2)
        setfiles = list(set(files))
        setfiles.sort()
        for idx, file in tqdm.tqdm(enumerate(setfiles), total=len(setfiles)):
            audio, _ = soundfile.read(file)
            data_1 = torch.FloatTensor(numpy.stack([audio], axis=0)).cuda()
            max_audio = 300 * 160 + 240
            if audio.shape[0] <= max_audio:
                shortage = max_audio - audio.shape[0]
                audio = numpy.pad(audio, (0, shortage), 'wrap')
            feats = []
            startframe = numpy.linspace(0, audio.shape[0] - max_audio, num=5)
            for asf in startframe:
                feats.append(audio[int(asf):int(asf) + max_audio])
            feats = numpy.stack(feats, axis=0).astype(numpy.float)
            data_2 = torch.FloatTensor(feats).cuda()
            with torch.no_grad():
                embedding_1 = self.speaker_encoder.forward(data_1, aug=False)
                embedding_1 = F.normalize(embedding_1, p=2, dim=1)
                embedding_2 = self.speaker_encoder.forward(data_2, aug=False)
                embedding_2 = F.normalize(embedding_2, p=2, dim=1)
            embeddings[file] = [embedding_1, embedding_2]
        embedding_11, embedding_12 = embeddings[find_file1]
        embedding_21, embedding_22 = embeddings[find_file2]
        score_1 = torch.mean(torch.matmul(embedding_11, embedding_21.T))
        score_2 = torch.mean(torch.matmul(embedding_12, embedding_22.T))
        sscore = (score_1 + score_2) / 2
        score = sscore.detach().cpu().numpy()
        if (score > 0.5):
            res = True
        else:
            res = False
        return score
    def getSymbol(self, file):
        self.eval()
        embeddings=[]

        audio, _ = soundfile.read(file)
        data_1 = torch.FloatTensor(numpy.stack([audio], axis=0)).cuda()
        max_audio = 300 * 160 + 240
        if audio.shape[0] <= max_audio:
                shortage = max_audio - audio.shape[0]
                audio = numpy.pad(audio, (0, shortage), 'wrap')
        feats = []
        startframe = numpy.linspace(0, audio.shape[0] - max_audio, num=5)
        for asf in startframe:
                feats.append(audio[int(asf):int(asf) + max_audio])
        feats = numpy.stack(feats, axis=0).astype(numpy.float)
        data_2 = torch.FloatTensor(feats).cuda()
        with torch.no_grad():
                embedding_1 = self.speaker_encoder.forward(data_1, aug=False)
                embedding_1 = F.normalize(embedding_1, p=2, dim=1)
                embedding_2 = self.speaker_encoder.forward(data_2, aug=False)
                embedding_2 = F.normalize(embedding_2, p=2, dim=1)


        return embedding_1, embedding_2





    def load_parameters(self, path):
        self_state = self.state_dict()
        loaded_state = torch.load(path)
        for name, param in loaded_state.items():
            origname = name
            if name not in self_state:
                name = name.replace("module.", "")
                if name not in self_state:
                    print("%s is not in the model." % origname)
                    continue
            if self_state[name].size() != loaded_state[origname].size():
                print("Wrong parameter length: %s, model: %s, loaded: %s" % (
                origname, self_state[name].size(), loaded_state[origname].size()))
                continue
            self_state[name].copy_(param)