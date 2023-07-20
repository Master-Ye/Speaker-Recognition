<template>
  <div class="compareTit flex justify-center items-start" style="margin-bottom: -20px">
    <el-alert
      title="Tips"
      type="success"
      description="点击上传文件或麦克风后可传入音频，点击按钮后可获得检索结果，点击结果可查看用户画像"
      show-icon
      class="fixed alert"
    />
    <div>
      <div class="fixed tip">产品体验</div>
    </div>
    <div class="block">
      <div class="audio-card-container mr-6" v-loading="loading">
        <el-card class="audio-card" shadow="hover">
          <div slot="header" class="audio-card-header m-0 p-0">
            <img :src="img1"  @click="startRecording"/>
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
              :http-request="uploadFile"
              :on-remove="remove"

            >
            <div>
                <el-button
                  type="danger"
                  :icon="videoPause"
                  circle
                  @click.stop="stopRecording"
                  v-if="start"
                />

                <div slot="trigger" size="small" type="primary">选择第一个说话文件(.wav)</div>
              </div>
            </el-upload>
          </div>
        </el-card>
      </div>
      <button class="btn" @click="submit()">检索</button>
    </div>
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>检索结果</span>
          <el-button class="button" text>The Result</el-button>
          <div>
          <el-checkbox v-model="checked" label="显示匹配度前三" size="large" /></div>
        </div>
      </template>

      <div class="text item ml-5 cursor-pointer" @click="check">最符合的人是{{ man }}，匹配度为{{ rate1 }}</div>
    </el-card>

    <v-chart class="chart border-blue-100 border ml-2 pl-0" id="main" :option="option" :autoresize="true" style="width:400px;height:400px;" v-show="checked" />
  </div>
</template>

<script scoped>
import { connect } from "extendable-media-recorder-wav-encoder";
import { VideoPause } from "@element-plus/icons-vue";
import { MediaRecorder, register } from "extendable-media-recorder";
import { ElNotification } from "element-plus";
import * as echart from 'echarts';
import img from "~/images/mic.png";
import axios from "~/axios.js";
import {ref,reactive} from "vue"

export default {
  async mounted() {
    await register(await connect());
  },
 data() {
    return {
      recorder: null,
      chunks: [],
      start: false,
      videoPause: VideoPause,
      img1: img,
      uploadFileList: [],
      res: 0,
      file: "",
      fileList2: [],
      man: "NULL",
      rate: "NULL",
      rate1:"NULL",
      loading: false,
      showChart:false,
      checked:false,
      datas :[{
  ranking: 1,
  station: '无',
  value: 16.74
},
  {
    ranking: 2,
    station: '无',
    value: 14.97
  },
  {
    ranking: 3,
    station: '无',
    value: 13.03
  }
],
    };
  },

  methods:
  {async startRecording() {
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
      this.loading = true;
      this.start = false;
      if (this.recorder && this.recorder.state !== "inactive") {
        this.recorder.addEventListener("stop", () => {
          const audioBlob = new File(this.chunks, { type: "audio/wav" });
          const audioUrl = URL.createObjectURL(audioBlob);
          // 将音频文件展示到卡片中，此处可以自行实现
          const formData = new FormData();
          formData.append("file", audioBlob, "recording.wav");
          axios
        .post("/search3", formData)
        .then((response) => {
          console.log(response);
          this.man = response.data.id1;
          this.rate = parseInt(response.data.score1 * 100);
this.datas[0].station=response.data.id1
this.datas[0].value=parseInt(response.data.score1*100)
this.datas[1].station=response.data.id2
this.datas[1].value=parseInt(response.data.score2*100)
this.datas[2].station=response.data.id3
this.datas[2].value=parseInt(response.data.score3*100)
let myChart = echart.init(document.getElementById("main"));
  var datas =this.datas

var seriesName = ['匹配度(%)'];
var attackSourcesColor1 = ['#FF557F', '#FFAA00', '#5470C6', '#1E9FFF'];
function contains(arr, dst) {
  var i = arr.length;
  while ((i -= 1)) {
    if (arr[i] == dst) {
      return i;
    }
  }
  return false;
}
var attackSourcesColor = [
  new echart.graphic.LinearGradient(0, 1, 1, 1, [{
    offset: 0, color: 'rgba(255,85,127,1)'
  },
    {
      offset: 1, color: 'rgba(255,85,127,1)'
    },
  ]),
  new echart.graphic.LinearGradient(0, 1, 1, 1, [{
    offset: 0, color: 'rgba(255,170,0,1)'
  },
    {
      offset: 1, color: 'rgba(255,170,0,1)'
    },
  ]),
  new echart.graphic.LinearGradient(0, 1, 1, 1, [{
    offset: 0, color: 'rgba(84,112,198,1)'
  },
    {
      offset: 1, color: 'rgba(84,112,198,1)'
    },
  ]),
  new echart.graphic.LinearGradient(0, 1, 1, 1, [{
    offset: 0, color: 'rgba(30,159,255,.82)'
  },
    {
      offset: 1, color: 'rgba(30,159,255,.82)'
    },
  ]),
];

var rankings = [];
var stationData = [];
var values = [];

datas.forEach(function (it, index) {
  rankings.push(it.ranking);
  stationData.push(it.station);
  values.push(it.value);
});

function dataFormat(data) {
  var arr = [];
  data.forEach(function (item, i) {
    let itemStyle = {
      color: i > 3 ? attackSourcesColor[3]: attackSourcesColor[i],
    };
    arr.push({
      value: item,
      itemStyle: itemStyle,
    });
  });
  return arr;
}

let option = {
  // backgroundColor: '#000',
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'shadow',
    },
  },

  grid: {
    left: '0%',
    right: '2%',
    bottom: '3%',
    top: '2%',
    containLabel: true,
  },
  xAxis: {
    type: 'value',
    splitLine: {
      show: false,
    },
    axisLabel: {
      show: false,
    },
    axisTick: {
      show: false,
    },
    axisLine: {
      show: false,
    },
  },
  yAxis: [{
    type: 'category',
    inverse: true,
    axisLine: {
      show: false,
    },
    axisTick: {
      show: false,
    },
    data: stationData,
    axisLabel: {
      margin: 30,
      fontSize: 14,
      align: 'left',
      padding: [3,
        0,
        0,
        0],
      color: '#000',
      rich: {
        nt1: {
          color: '#fff',
          backgroundColor: attackSourcesColor1[0],
          width: 20,
          height: 18,
          fontSize: 12,
          align: 'center',
          borderRadius: 50,
          lineHeight: '5',
          padding: [2,
            0,
            0,
            0],
          // padding:[0,0,2,0],
        },
        nt2: {
          color: '#fff',
          backgroundColor: attackSourcesColor1[1],
          width: 20,
          height: 18,
          fontSize: 12,
          align: 'center',
          borderRadius: 50,
          padding: [2,
            0,
            0,
            0],
        },
        nt3: {
          color: '#fff',
          backgroundColor: attackSourcesColor1[2],
          width: 20,
          height: 18,
          fontSize: 12,
          align: 'center',
          borderRadius: 50,
          padding: [2,
            0,
            0,
            0],
        },
        nt: {
          color: '#fff',
          backgroundColor: attackSourcesColor1[3],
          width: 20,
          height: 18,
          fontSize: 12,
          align: 'center',
          borderRadius: 50,
          padding: [2,
            0,
            0,
            0],
        },
      },
      formatter: function (value, index) {
        index = contains(stationData, value) + 1;
        if (index - 1 < 3) {
          return ['{nt' + index + '|' + index + '}'].join('\n');
        } else {
          return ['{nt|' + index + '}'].join('\n');
        }
      },
    }
  },

    {
      type: 'category',
      inverse: true,
      axisTick: 'none',
      axisLine: 'none',
      show: true,
      axisLabel: {

          color: '#666',
          fontSize: '12',

      },
      data: dataFormat(values),
    },

    {
      // 条状标题
      type: 'category',
      inverse: true,
      offset: -10,
      position: 'left',
      axisTick: 'none',
      axisLine: 'none',
      show: true,
      axisLabel: {
        interval: 0,
        color: ['#666'],
        align: 'left',
        verticalAlign: 'bottom',
        lineHeight: 42,
        fontSize: 14,
      },
      data: dataFormat(stationData),
    },
  ],
  series: [{
    zlevel: 1,
    name: seriesName[0],
    type: 'bar',
    barWidth: 15,
    data: dataFormat(values),
    align: 'center',
    itemStyle: {

        borderRadius: 10,

    },
    label: {
      //条状中的样式
      show: true,
      fontSize: 10,
      color: '#fff',
      //条装中字体颜色
      textBorderWidth: 2,
      padding: [2,
        0,
        0,
        0],
    },
  }
  ],
}
    myChart.setOption(option);
          this.rate1=this.rate+"%"
          this.loading = false;
this.file=""
          ElNotification({
            message: "请求成功",
            type: "success",
            duration: 3000,
          });
        })
        .catch((err) => {
          console.log(err)
            this.loading=false
          ElNotification({
            message: "请求失败",
            type: "error",
            duration: 3000,
          });
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
    handleChange1(uploadFile) {
      this.file = uploadFile;
    },
    submit() {
      this.loading = true;
      const formData = new FormData(); // new FormData
      if (this.file == "") {
        ElNotification({
          message: "请上传文件",
          type: "info",
          duration: 3000,
        });
        this.loading=false
        return;
      }
      formData.append("file", this.file.raw);
console.log(this.file)
      axios
        .post("/search3", formData)
        .then((response) => {
          console.log(response);
          this.man = response.data.id1;
          this.rate = parseInt(response.data.score1 * 100);
this.datas[0].station=response.data.id1
this.datas[0].value=parseInt(response.data.score1*100)
this.datas[1].station=response.data.id2
this.datas[1].value=parseInt(response.data.score2*100)
this.datas[2].station=response.data.id3
this.datas[2].value=parseInt(response.data.score3*100)
let myChart = echart.init(document.getElementById("main"));
  var datas =this.datas

var seriesName = ['匹配度(%)'];
var attackSourcesColor1 = ['#FF557F', '#FFAA00', '#5470C6', '#1E9FFF'];
function contains(arr, dst) {
  var i = arr.length;
  while ((i -= 1)) {
    if (arr[i] == dst) {
      return i;
    }
  }
  return false;
}
var attackSourcesColor = [
  new echart.graphic.LinearGradient(0, 1, 1, 1, [{
    offset: 0, color: 'rgba(255,85,127,1)'
  },
    {
      offset: 1, color: 'rgba(255,85,127,1)'
    },
  ]),
  new echart.graphic.LinearGradient(0, 1, 1, 1, [{
    offset: 0, color: 'rgba(255,170,0,1)'
  },
    {
      offset: 1, color: 'rgba(255,170,0,1)'
    },
  ]),
  new echart.graphic.LinearGradient(0, 1, 1, 1, [{
    offset: 0, color: 'rgba(84,112,198,1)'
  },
    {
      offset: 1, color: 'rgba(84,112,198,1)'
    },
  ]),
  new echart.graphic.LinearGradient(0, 1, 1, 1, [{
    offset: 0, color: 'rgba(30,159,255,.82)'
  },
    {
      offset: 1, color: 'rgba(30,159,255,.82)'
    },
  ]),
];

var rankings = [];
var stationData = [];
var values = [];

datas.forEach(function (it, index) {
  rankings.push(it.ranking);
  stationData.push(it.station);
  values.push(it.value);
});

function dataFormat(data) {
  var arr = [];
  data.forEach(function (item, i) {
    let itemStyle = {
      color: i > 3 ? attackSourcesColor[3]: attackSourcesColor[i],
    };
    arr.push({
      value: item,
      itemStyle: itemStyle,
    });
  });
  return arr;
}

let option = {
  // backgroundColor: '#000',
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'shadow',
    },
  },

  grid: {
    left: '0%',
    right: '2%',
    bottom: '3%',
    top: '2%',
    containLabel: true,
  },
  xAxis: {
    type: 'value',
    splitLine: {
      show: false,
    },
    axisLabel: {
      show: false,
    },
    axisTick: {
      show: false,
    },
    axisLine: {
      show: false,
    },
  },
  yAxis: [{
    type: 'category',
    inverse: true,
    axisLine: {
      show: false,
    },
    axisTick: {
      show: false,
    },
    data: stationData,
    axisLabel: {
      margin: 30,
      fontSize: 14,
      align: 'left',
      padding: [3,
        0,
        0,
        0],
      color: '#000',
      rich: {
        nt1: {
          color: '#fff',
          backgroundColor: attackSourcesColor1[0],
          width: 20,
          height: 18,
          fontSize: 12,
          align: 'center',
          borderRadius: 50,
          lineHeight: '5',
          padding: [2,
            0,
            0,
            0],
          // padding:[0,0,2,0],
        },
        nt2: {
          color: '#fff',
          backgroundColor: attackSourcesColor1[1],
          width: 20,
          height: 18,
          fontSize: 12,
          align: 'center',
          borderRadius: 50,
          padding: [2,
            0,
            0,
            0],
        },
        nt3: {
          color: '#fff',
          backgroundColor: attackSourcesColor1[2],
          width: 20,
          height: 18,
          fontSize: 12,
          align: 'center',
          borderRadius: 50,
          padding: [2,
            0,
            0,
            0],
        },
        nt: {
          color: '#fff',
          backgroundColor: attackSourcesColor1[3],
          width: 20,
          height: 18,
          fontSize: 12,
          align: 'center',
          borderRadius: 50,
          padding: [2,
            0,
            0,
            0],
        },
      },
      formatter: function (value, index) {
        index = contains(stationData, value) + 1;
        if (index - 1 < 3) {
          return ['{nt' + index + '|' + index + '}'].join('\n');
        } else {
          return ['{nt|' + index + '}'].join('\n');
        }
      },
    }
  },

    {
      type: 'category',
      inverse: true,
      axisTick: 'none',
      axisLine: 'none',
      show: true,
      axisLabel: {

          color: '#666',
          fontSize: '12',

      },
      data: dataFormat(values),
    },

    {
      // 条状标题
      type: 'category',
      inverse: true,
      offset: -10,
      position: 'left',
      axisTick: 'none',
      axisLine: 'none',
      show: true,
      axisLabel: {
        interval: 0,
        color: ['#666'],
        align: 'left',
        verticalAlign: 'bottom',
        lineHeight: 42,
        fontSize: 14,
      },
      data: dataFormat(stationData),
    },
  ],
  series: [{
    zlevel: 1,
    name: seriesName[0],
    type: 'bar',
    barWidth: 15,
    data: dataFormat(values),
    align: 'center',
    itemStyle: {

        borderRadius: 10,

    },
    label: {
      //条状中的样式
      show: true,
      fontSize: 10,
      color: '#fff',
      //条装中字体颜色
      textBorderWidth: 2,
      padding: [2,
        0,
        0,
        0],
    },
  }
  ],
}
    myChart.setOption(option);
          this.rate1=this.rate+"%"
          this.loading = false;
this.file=""
          ElNotification({
            message: "请求成功",
            type: "success",
            duration: 3000,
          });
        })
        .catch((err) => {
          console.log(err)
            this.loading=false
          ElNotification({
            message: "请求失败",
            type: "error",
            duration: 3000,
          });
        });
    },
    check(){
if(this.man!=="NULL")
this.$router.push({ name: 'user', params: { id: this.man }})
else {
      ElNotification({
          message: "出错",
          type: "error",
          duration: 3000,
        })
    }


  },
}}
</script>

<style>
.compareTit {
  @apply font-serif font-semibold text-xl;

  text-align: center;

  margin-bottom: -2px;
}

img {
  padding: 0px;
  margin: 0px;
}
.tip {
  top: 23%;
  left: 50%;
}
.alert {
  top: 70px;
  left: 37%;
  width: 700px;
}
.btn {
  background: #1a175e;
  /* 创建渐变 */
  background-image: -webkit-linear-gradient(top, #eb94d0, #2079b0);
  background-image: -moz-linear-gradient(top, #eb94d0, #2079b0);
  background-image: -ms-linear-gradient(top, #eb94d0, #2079b0);
  background-image: -o-linear-gradient(top, #eb94d0, #2079b0);
  background-image: linear-gradient(to bottom, #eb94d0, #2079b0);
  /* 给按钮添加圆角 */
  -webkit-border-radius: 28;
  -moz-border-radius: 28;
  border-radius: 28px;
  text-shadow: 3px 2px 1px #9daef5;
  -webkit-box-shadow: 6px 5px 24px #666666;
  -moz-box-shadow: 6px 5px 24px #666666;
  box-shadow: 6px 5px 24px #666666;
  font-family: Arial;
  color: #fafafa;
  font-size: 20px;
  padding: 9px;
  text-decoration: none;
  width: 120px;
  height: 50px;
}
.btn:hover {
  background: #2079b0;
  background-image: -webkit-linear-gradient(top, #2079b0, #eb94d0);
  background-image: -moz-linear-gradient(top, #2079b0, #eb94d0);
  background-image: -ms-linear-gradient(top, #2079b0, #eb94d0);
  background-image: -o-linear-gradient(top, #2079b0, #eb94d0);
  background-image: linear-gradient(to bottom, #2079b0, #eb94d0);
  text-decoration: none;
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
}

</style>
