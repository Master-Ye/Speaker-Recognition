<template>
  <div class="compareTit" style="margin-bottom: -20px">
    <el-alert
      title="Tips"
      type="success"
      description="点击上传文件或麦克风后可传入音频，点击识别即可检测相似度"
      show-icon
      class="absolute alert"
    />
    <div>产品体验</div>
    <dv-decoration5 :dur="2" style="width: 100%; height: 100%" class="m-auto" />

    <div class="audio-card-container">
      <el-card class="audio-card" shadow="hover">
        <div slot="header" class="audio-card-header m-0 p-0">
          <img :src="img1" @click="startRecording1"/>
        </div>
        <div class="audio-card-body">
          <el-upload
            class="upload-demo"
            :auto-upload="false"
            :show-file-list="true"
            ref="upload1"
            :on-change="handleChange1"
            :limit="1"
            :before-upload="beforeUpload"
            action="#"
            :file-list="fileList1"
            :on-success="handleSuccess"
          >
          <div>
                <el-button
                  type="danger"
                  :icon="videoPause"
                  circle
                  @click.stop="stopRecording1"
                  v-if="start1"
                />

                <div slot="trigger" size="small" type="primary">选择第一个说话人音频(.wav)</div>
              </div>
          </el-upload>
        </div>
      </el-card>
      <div>
        <dv-decoration-9
          style="width: 150px; height: 150px"
          class="m-auto mt-8"
          v-if="loading"
        >
          <div color-green font-600 class="content" bg="~ dark/0">{{ res }}%</div>
        </dv-decoration-9>
        <dv-loading v-else style="width: 150px; height: 150px" class="m-auto mt-8">
          <div color-white>Loading...</div>
        </dv-loading>
        <h1 class="mt-3">相似度</h1>
<el-text class="mx-1" type="warning">结果:</el-text>
           <el-text class="mx-1 text-2xl" type="warning"  v-if="origin">音频来自同一说话人</el-text>
           <el-text class="mx-1 text-2xl" type="warning"  v-if="after">音频不来自同一说话人</el-text>
      </div>
      <el-card class="audio-card" shadow="hover">
        <div slot="header" class="audio-card-header m-0 p-0">
          <img :src="img1" @click="startRecording2"/>
        </div>
        <div class="audio-card-body">
          <el-upload
            class="upload-demo"
            :auto-upload="false"
            :show-file-list="true"
            ref="upload2"
            :limit="1"
            :before-upload="beforeUpload"
            action="http://localhost:5000/upload"
            :file-list="fileList2"
            :on-change="handleChange2"
            :on-success="handleSuccess"
          >
          <div>
                <el-button
                  type="danger"
                  :icon="videoPause"
                  circle
                  @click.stop="stopRecording2"
                  v-if="start2"
                />

                <div slot="trigger" size="small" type="primary">选择说话文件(.wav)</div>
              </div>
          </el-upload>
        </div>
      </el-card>
    </div>
    <el-button type="success" class="btn" @click="subitIt()">
      <el-icon>
        <Place />
      </el-icon>
      识别<el-icon>
        <Place />
      </el-icon>
    </el-button>
  </div>
</template>

<script>
import { connect } from "extendable-media-recorder-wav-encoder";
import { VideoPause } from "@element-plus/icons-vue";
import { MediaRecorder, register } from "extendable-media-recorder";
import img from "~/images/mic.png";
import axios from "~/axios.js";
import { ElNotification } from "element-plus";
export default {
  data() {
    return {
      origin:false,
      after:false,
start1:false,
start2:false,
videoPause: VideoPause,
      img1: img,
      uploadFileList: [{raw:null},{raw:null}],
      res: 0,
      fileList1: [],
      fileList2: [],
      loading: true,
      chunks1:[],
      chunks2:[],
      recorder1:null,
      recorder2:null,
    };
  },
  async mounted() {
    await register(await connect());},
  methods: {

    handleChange1(uploadFile) {
      this.uploadFileList[0] = uploadFile;
    },
    handleChange2(uploadFile) {
      this.uploadFileList[1] = uploadFile;
    },
    subitIt() {
      console.log( "11", this.uploadFileList)
      if (this.uploadFileList[0].raw == null|| this.uploadFileList[1].raw == null) {
        ElNotification({
          message: "请上传文件",
          type: "error",
          duration: 3000,
        });
        return;
      }
      console.log(this.uploadFileList);
      const formData = new FormData(); // new FormData
      this.uploadFileList.forEach((file, index) => {
        index = index + 1;
        formData.append("file" + index, file.raw);
      });
      console.log(formData);
      this.loading = false;

      axios.post("/upload", formData).then((response) => {
        console.log(response);

        this.res = parseInt(response.data.res1 * 100);
        if(this.res>50){
          this.origin=true;
          this.after=false;}
        else{
          this.origin=false;
          this.after=true;}
        this.loading = true;
      }).catch((error)=>{this.loading=true;ElNotification({
          message: "操作失败",
          type: "error",
          duration: 3000,
        });});
    },
    async startRecording1() {
      this.start1 = true;
      navigator.mediaDevices.getUserMedia({ audio: true }).then((stream) => {
        this.chunks1 = [];

        this.recorder1 = new MediaRecorder(stream, { mimeType: "audio/wav" });
        this.recorder1.addEventListener("dataavailable", (event) => {
          this.chunks1.push(event.data);
        });
        this.recorder1.start();
      });
    },
    async startRecording2() {
      this.start2 = true;
      navigator.mediaDevices.getUserMedia({ audio: true }).then((stream) => {
        this.chunks2 = [];

        this.recorder2 = new MediaRecorder(stream, { mimeType: "audio/wav" });
        this.recorder2.addEventListener("dataavailable", (event) => {
          this.chunks2.push(event.data);
        });
        this.recorder2.start();
      });
    },
    stopRecording1() {
      this.start1 = false;
      if (this.recorder1 && this.recorder1.state !== "inactive") {
        this.recorder1.addEventListener("stop", () => {
          const audioBlob = new File(this.chunks1, { type: "audio/wav" });
this.uploadFileList[0].raw=audioBlob;
        });
        this.recorder1.stop();
        this.recorder1 = null;
      }

      console.log(this.chunks1);
      const audioBlob = new File(this.chunks1, "filename.wav", {
        type: "audio/wav",
        lastModified: Date.now(),
      });
      this.uploadFileList[0].raw=audioBlob;
      this.fileList1.push(audioBlob);
      console.log(this.chunks1.length);
    },
    stopRecording2() {
      this.start2 = false;
      if (this.recorder2 && this.recorder2.state !== "inactive") {
        this.recorder2.addEventListener("stop", () => {
          const audioBlob = new File(this.chunks2, { type: "audio/wav" });

          // 将音频文件展示到卡片中，此处可以自行实现
this.uploadFileList[1].raw=audioBlob;

        });
        this.recorder2.stop();
        this.recorder2 = null;
      }

      console.log(this.chunks2);
      const audioBlob = new File(this.chunks2, "filename.wav", {
        type: "audio/wav",
        lastModified: Date.now(),
      });
      this.fileList2.push(audioBlob);
      console.log(this.chunks2.length);
    },
  },
};
</script>

<style scoped>
.compareTit {
  @apply font-serif font-semibold text-xl justify-center flex;

  text-align: center;
  display: block;
  margin-bottom: -40px;
}
.btn {
  width: 100px;
  height: 80px;
  line-height: 90px;
  text-align: center;
  color: #fff;
  font-size: 25px;
  text-transform: uppercase;
  cursor: pointer;
  background: linear-gradient(90deg, #03a9f4, #f441a5, #ffeb3b, #03a9f4);
  background-size: 400%;
  border-radius: 60px;
}

.btn::before {
  content: "";
  position: absolute;
  top: -5px;
  left: -5px;
  right: -5px;
  bottom: -5px;
  z-index: -1;
  background: linear-gradient(90deg, #03a9f4, #f441a5, #ffeb3b, #03a9f4);
  background-size: 400%;
  border-radius: 40px;
  opacity: 0;
  transition: 0.5s;
}

img {
  padding: 0px;
  margin: 0px;
}

.audio-card {
  width: 18rem;
  margin: 0 auto;
  background-color: #1e1e1e;
  color: white;
  border-radius: 10px;
  padding: 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  transition: transform 0.3s ease-in-out;
  cursor: pointer;
  background: linear-gradient(to bottom right, rgb(9, 6, 25), rgb(18, 0, 22));
  box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.3);
  border-radius: 10px;
  padding: 20px;

  height: 18rem;
  color: #fff;
  position: relative;
  overflow: hidden;
}

.audio-card:hover {
  transform: translateY(-5px);
}

.audio-card:hover:before {
  animation: fadeIn 0.6s ease forwards;
}
.alert {
  top: 70px;
  left: 37%;
  width: 700px;
}

@keyframes fadeIn {
  0% {
    opacity: 0;
  }

  100% {
    opacity: 1;
  }
}

.audio-card-header {
  color: #333;
  font-size: 18px;
  font-weight: bold;
}

.audio-card-body {
  padding: 20px;
}

.upload-demo {
  margin-top: 20px;
}

.audio-card-container {
  display: flex;
}
</style>
