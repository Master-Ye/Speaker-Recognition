<template>
  <div class="compareTit" style="margin-bottom: -20px">
    <el-alert
      title="上传文件或点击麦克风录音后可查看对应频谱，点击增强后可获取增强后频谱"
      class="fixed alert"
      type="success"
      center
      show-icon
    />
    <div>产品体验</div>
    <div>
      <el-checkbox v-model="orgin" label="原始" size="large" border />
    <el-checkbox v-model="after" label="增强后" size="large" border />

    </div>
    <dv-decoration5 :dur="2" style="width: 100%; height: 100%" class="m-auto" />

    <div class="audio-card-container" v-loading="loading">
      <div>
        <el-card class="audio-card" shadow="hover">
          <div slot="header" class="audio-card-header m-0 p-0">
            <img :src="img1" @click="startRecording" class="mic"/>
          </div>
          <div class="audio-card-body">
            <el-upload
              class="upload-demo"
              :auto-upload="true"
              :show-file-list="true"
              ref="upload1"
              :on-change="handleChange1"
              :limit="1"
              :before-upload="beforeUpload"
              action="#"
              :file-list="fileList1"
              :on-success="handleSuccess"
              :http-request="uploadFile"
            >
              <div>
                <el-button
                  type="danger"
                  :icon="videoPause"
                  circle
                  @click.stop="stopRecording"
                  v-if="start"
                />

                <div slot="trigger" size="small" type="primary">选择说话文件(.wav)</div>
              </div>
            </el-upload>
          </div>
        </el-card>
        <el-button type="success" class="btn" @click="subIt()">
          <el-icon>
            <Place />
          </el-icon>
          音频增强<el-icon>
            <Place />
          </el-icon>
        </el-button>
      </div>
      <div class="flex flex-col imgs">
        <img :src="orginImg" v-if="orgin" class="imga" />
        <img :src="afterImg" v-if="after" class="imga" />
      </div>
    </div>
  </div>
</template>

<script>
import { VideoPause } from "@element-plus/icons-vue";
import { MediaRecorder, register } from "extendable-media-recorder";
import img1 from "~/images/2.jpg";
import img from "~/images/mic.png";
import axios from "~/axios.js";
import { connect } from "extendable-media-recorder-wav-encoder";
import { ElNotification } from "element-plus";
export default {
  data() {
    return {
      start: false,
      videoPause: VideoPause,
      disable: "",
      orgin: true,
      after: false,
      img1: img,
      uploadFileList: [],
      res: 0,
      fileList1: [],
      fileList2: [],
      loading: false,
      down: "",
      orginImg: img1,
      afterImg: "",
      file: { raw: null },
      recorder: null,
      chunks: [],
    };
  },
  async mounted() {
    await register(await connect());
  },
  methods: {
    async startRecording() {
      this.start = true;
      navigator.mediaDevices.getUserMedia({ audio: true }).then((stream) => {
        this.chunks = [];

        this.recorder = new MediaRecorder(stream, { mimeType: "audio/wav" });
        this.recorder.addEventListener("dataavailable", (event) => {
          this.chunks.push(event.data);
        });
        this.recorder.start();
      });
    },
    stopRecording() {
      this.start = false;
      if (this.recorder && this.recorder.state !== "inactive") {
        this.recorder.addEventListener("stop", () => {
          const audioBlob = new File(this.chunks, { type: "audio/wav" });
          const audioUrl = URL.createObjectURL(audioBlob);
          // 将音频文件展示到卡片中，此处可以自行实现
          const formData = new FormData();
          formData.append("file", audioBlob, "recording.wav");
          axios
            .post("http://localhost:5000/orgin", formData, {
              responseType: "blob",
              headers: { "Content-Type": "multipart/form-data" },
            })
            .then((res) => {
              const blob = new Blob([res.data]);
              this.down = blob;
              this.loading = false;
              this.orginImg = window.URL.createObjectURL(res.data);
              this.orgin = true;
            })
            .catch(function (error) {
              console.log(error);
            });

          const audioBlob1 = new File(this.chunks, "filename.wav", { type: "audio/wav" });
          console.log(audioBlob1);
          this.fileList1 = [];
          this.fileList1.push(audioBlob1);
          this.file.raw = audioBlob1;
        });
        this.recorder.stop();
        this.recorder = null;
      }

      console.log(this.chunks);
      const audioBlob = new File(this.chunks, "filename.wav", {
        type: "audio/wav",
        lastModified: Date.now(),
      });
      this.fileList1.push(audioBlob);
      console.log(this.chunks.length);
    },

    uploadRecording() {
      console.log(this.chunks.length);
      if (this.chunks.length === 0) {
        // 提示用户先录制音频
        return;
      }
      const audioBlob = new File(this.chunks, "filename.wav", {
        type: "audio/wav",
        lastModified: Date.now(),
      });
      console.log(audioBlob);
      const formData = new FormData();
      formData.append("file", audioBlob, "recording.wav");
      axios
        .post("http://localhost:5000/orgin", formData, {
          responseType: "blob",
          headers: { "Content-Type": "multipart/form-data" },
        })
        .then((res) => {
          console.log(res);
          const blob = new Blob([res.data]);
          this.down = blob;
          this.loading = false;
          this.orginImg = window.URL.createObjectURL(res.data);
          this.orgin = true;
        })
        .catch(function (error) {
this.loading=false
          console.log(error);
          ElNotification({
        message: "操作失败",
        type: "error",
        duration: 3000,
      });
        });
    },
    handleChange1(file) {
      ElNotification({
        message: "上传成功",
        type: "success",
        duration: 3000,
      });
      this.file = file;
      console.log(this.file);
      this.disable = false;
    },

    uploadFile(file) {
      var filelist = new FormData();
      filelist.append("file", file.file);
      this.loading = true;
      if (filelist == null) {
        ElNotification({
          message: "请上传文件",
          type: "error",
          duration: 3000,
        });
        this.loading = false;
        return;
      }
      if (file.file.name.split(".")[1] != "wav") {
        ElNotification({
          message: "请上传wav格式文件",
          type: "error",
          duration: 3000,
        });
        this.loading = false;
        return;
      }
      axios
        .post("http://localhost:5000/orgin", filelist, {
          responseType: "blob",
          headers: { "Content-Type": "multipart/form-data" },
        })
        .then((res) => {
          console.log(res);
          const blob = new Blob([res.data]);
          this.down = blob;
          this.loading = false;
          this.orginImg = window.URL.createObjectURL(res.data);
          this.orgin = true;
        })
        .catch( (error)=> {
          this.loading = false;
          ElNotification({
          message: "获取失败，请检查网络设置",
          type: "error",
          duration: 5000,
        });

        });
    },
    subIt() {
      var filelist = new FormData();
      if(this.file.raw==null){
        ElNotification({
          message: "请上传文件",
          type: "error",
          duration: 3000,
        });
        this.loading = false;
        return;
      }
      filelist.append("file", this.file.raw);
      this.loading = true;
      axios
        .post("/enhance", filelist, {
          responseType: "blob",
          headers: { "Content-Type": "multipart/form-data" },
        })
        .then((res) => {
          console.log(res);
          const blob = new Blob([res.data]);
          this.down = blob;
          this.loading = false;
          this.afterImg = window.URL.createObjectURL(res.data);
          this.after = true;
        })
        .catch(function (error) {

          console.log(error);
        })
    },
  },
};
</script>

<style scoped>
.mic:active:after {
  content: ""; /* 添加一个伪元素 */
  position: absolute; /* 使伪元素绝对定位 */
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.3); /* 设置背景色 */
  z-index: 1; /* 使伪元素在图片上方 */
  animation: click-effect 0.2s linear forwards; /* 添加动画效果 */
}

/* 定义点击动效的关键帧 */
@keyframes click-effect {
  from { transform: scale(1); opacity: 1; }
  to { transform: scale(1.2); opacity: 0; }
}
.imga {
  height: 23rem;
  width: 35rem;
}

.compareTit {
  @apply font-serif font-semibold text-xl justify-center;

  text-align: center;
  display: block;
  margin-bottom: -2px;
}

img {
  padding: 0px;
  margin: 0px;
}

.alert {
  top: 70px;
  left: 37%;
  width: 700px;
}

.btn1 {
  display: inline-block;
  border-radius: 4px;
  background-color: #f4511e;
  border: none;
  color: #ffffff;
  text-align: center;
  font-size: 2.8px;
  padding: 0px;
  width: 80px;
  transition: all 0.5s;
  cursor: pointer;
  margin: 0px;
  height: 80px;
}

.btn1 span {
  cursor: pointer;
  display: inline-block;
  position: relative;
  transition: 0.5s;
}

.btn1 span:after {
  content: "\00bb";
  /* CSS Entities. 如果用的是 HTML Entities, 请改成 &#8594;*/
  position: absolute;
  opacity: 0;
  top: 0;
  right: -20px;
  transition: 0.5s;
}

.btn1:hover span {
  padding-right: 2px;
}

.btn1:hover span:after {
  opacity: 1;
  right: 0;
}

.audio-card {
  margin: 0 auto;
  background-color: #1e1e1e;
  color: white;
  border-radius: 10px;
  padding: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.3s ease-in-out;
  cursor: pointer;
  background: linear-gradient(to bottom right, rgb(9, 6, 25), rgb(18, 0, 22));
  box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.3);
  border-radius: 10px;
  padding: 20px;
  width: 18rem;
  height: 19rem;
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
  align-items: center;
  justify-content: center;
}
</style>
