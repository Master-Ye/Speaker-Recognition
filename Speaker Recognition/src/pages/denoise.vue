<template>
  <div class="compareTit" style="margin-bottom: -20px">
    <el-alert
      title="Tips"
      type="success"
      description="点击上传文件或麦克风后可传入音频，待获得提示后即刻下载降噪后音频"
      show-icon
      class="absolute alert"
    />
    <div>产品体验</div>
    <dv-decoration5 :dur="2" style="width: 100%; height: 100%" class="m-auto" />

    <div class="audio-card-container" v-loading="loading">
      <el-card class="audio-card" shadow="hover">
        <div slot="header" class="audio-card-header m-0 p-0">
          <img :src="img1" @click="startRecording" />
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
      <el-card class="audio-card" shadow="hover">
        <div slot="header" class="audio-card-header m-0 p-0">
          <img :src="img1" />
        </div>
        <div class="audio-card-body">
          <el-form>
            <el-form-item>
              <el-upload
                class="upload-demo flex"
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
              </el-upload>
            </el-form-item>
            <div slot="trigger" size="small" type="primary" @click="downloadit">
              下载降噪文件
            </div>
          </el-form>
        </div>
      </el-card>
    </div>
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
      start: false,
      videoPause: VideoPause,
      img1: img,
      uploadFileList: [],
      res: 0,
      fileList1: [],
      fileList2: [],
      loading: false,
      down: "",
      chunks:[],
      recorder:null,
    };
  },
  async mounted() {
    await register(await connect());
  },
  methods: { async startRecording() {
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
    handleChange1(file) {
      ElNotification({
        message: "上传成功",
        type: "success",
        duration: 3000,
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
            .post("http://localhost:5000/denoise", formData, {
              responseType: "blob",
              headers: { "Content-Type": "multipart/form-data" },
            })
            .then((res) => {
              ElNotification({
            message: "降噪完成，点击下载可下载文件",
            type: "success",
            duration: 6000,
          });
          const blob = new Blob([res.data]);
          this.down = blob;
          this.loading = false;
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

    uploadFile(file) {
      var filelist = new FormData();
      filelist.append("file", file.file);
      this.loading = true;
      axios
        .post("/denoise", filelist, {
          responseType: "arraybuffer",
          headers: { "Content-Type": "multipart/form-data" },
        })
        .then((res) => {
          ElNotification({
            message: "降噪完成，点击下载可下载文件",
            type: "success",
            duration: 6000,
          });
          const blob = new Blob([res.data]);
          this.down = blob;
          this.loading = false;
        })
        .catch( (error)=> {
          this.loading = false;
          ElNotification({
            message: "操作失败",
            type: "error",
            duration: 6000,
          });
        });
    },
    downloadit() {
      const link = document.createElement("a");
      link.download = "denoise.wav"; // a标签添加属性
      link.style.display = "none";
      link.href = URL.createObjectURL(this.down);
      link.className = "down";
      document.body.appendChild(link);
      link.click();
    },
  },
};
</script>

<style scoped>
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
  content: "\00bb"; /* CSS Entities. 如果用的是 HTML Entities, 请改成 &#8594;*/
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
  justify-content: space-between;
  transition: transform 0.3s ease-in-out;
  cursor: pointer;
  background: linear-gradient(to bottom right, rgb(9, 6, 25), rgb(18, 0, 22));
  box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.3);
  border-radius: 10px;
  padding: 20px;
  width: 18rem;
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
