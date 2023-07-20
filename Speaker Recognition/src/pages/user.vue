<template>
  <div class="user-profile" v-for="(item, index) of profile" :key="index">
    <div v-if="item.name == this.now">
      <div class="font-serif antialiased font-bold">请选择查看的用户:</div>
      <el-select v-model="now" class="m-0" placeholder="Select">
        <el-option
          v-for="(item, index) in profile"
          :key="index"
          :label="item.name"
          :value="item.name"
        />
      </el-select>

      <div class="profile-card m-0">
        <el-card class="basic-info rounded-2xl">
          <h2 class="font-bold">{{ item.name }} 的信息</h2>

          <div class="card-content flex flex-wrap justify-between">
            <div class="w-25 h-20 border-2 rounded-2xl inline-block">
              <el-icon>
                <UserFilled />
              </el-icon>
              <div class="m-auto text-center font-bold">{{ item.name }}</div>
            </div>

            <div class="w-25 h-20 border-2 rounded-2xl inline-block">
              <el-icon v-if="profile.gender == 'Male'">
                <Male />
              </el-icon>
              <el-icon v-else>
                <Female />
              </el-icon>
              <div class="m-auto text-center font-bold">
                {{ item.gender==0?"女":"男" }} {{ item.age }}岁
              </div>
            </div>
            <div class="w-53 h-20 border-2 rounded-2xl inline-block mt-4">
              <el-icon>
                <PhoneFilled />
              </el-icon>
              <div class="m-auto text-center font-bold">{{ item.phone }}</div>
            </div>
            <div class="w-53 h-20 border-2 rounded-2xl inline-block mt-4">
              <el-icon>
                <Message />
              </el-icon>
              <div class="m-auto text-center font-bold">{{ item.email || "空" }}</div>
            </div>
            <div class="w-53 h-20 border-2 rounded-2xl inline-block mt-4">
              <el-icon>
                <Location />
              </el-icon>
              <div class="m-auto text-center font-bold">{{ item.location }}</div>
            </div>
          </div>
        </el-card>

        <el-card class="basic-info rounded-2xl gender">
          <v-chart class="chart p-0 m-0" :option="option1" autoresize />
        </el-card>
        <el-card class="basic-info rounded-2xl age">
          <v-chart class="chart p-0 m-0" :option="option2" autoresize />
        </el-card>
      </div>
    </div>
  </div>
</template>

<script>
import { getCurrentInstance } from "vue";
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { PieChart } from 'echarts/charts';
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
} from 'echarts/components';
import VChart, { THEME_KEY } from 'vue-echarts';
import {  provide } from 'vue';
import axios from "~/axios";
import { ref,computed } from 'vue'
import { ElNotification } from "element-plus";
export default {
  setup(){

    use([
  CanvasRenderer,
  PieChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
]);

provide(THEME_KEY, 'dark');

let datab = getCurrentInstance();
const option2 = computed(()=>{return  {
  title: {
    text: "年龄统计",
    left: "center"
  },
  xAxis: {
    type: 'category',
    data: ['0-20', '21-40', '41-60', '61-70', '>70']
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      data: [datab.data.one, datab.data.two,datab.data.three, datab.data.four, datab.data.five],
      type: 'bar',
      showBackground: true,
      backgroundStyle: {
        color: 'rgba(180, 180, 180, 0.2)'
      }
    }
  ]
};});
const option1 = computed(()=>{return {
  title: {
    text: "性别比例",
    left: "center"
  },
  tooltip: {
    trigger: "item",
    formatter: "{a} <br/>{b} : {c} ({d}%)"
  },
  legend: {
    orient: "vertical",
    left: "left",
    data: ["男性", "女性"]
  },
  series: [
    {
      name: "性别",
      type: "pie",
      radius: "55%",
      center: ["50%", "60%"],
      data: [
        { value: datab.data.male, name: "男性" },
        { value: datab.data.female, name: "女性" },

      ],
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: "rgba(0, 0, 0, 0.5)"
        }
      }
    }
  ]
}});
return {option1,option2}
  },
  mounted() {
      axios
      .post("/all")
      .then((res) => {
        this.profile = res.data;
        this.$store.state.profile = res.data;

        this.male = res.data.filter(user => user.gender === 1).length;
this.female = res.data.filter(user => user.gender === 0).length;
this.one = res.data.filter(user => user.age >= 0 && user.age <= 20).length;
this.two = res.data.filter(user => user.age >= 21 && user.age <= 40).length;
this.three = res.data.filter(user => user.age >= 41 && user.age <= 60).length;
this.four = res.data.filter(user => user.age >= 61 && user.age <= 70).length;
this.five = res.data.filter(user => user.age >= 71).length;
      })
      .catch((err) => {
        ElNotification.error({ title: "错误", message: "获取用户信息失败" });
      });




  },
  data() {
    return {
male:"",
female:"",
one:"",
two:"",
three:"",
four:"",
five:"",
      value: "",
      now: this.$route.params.id || "G150",
      profile: [
        {
          age: "null",
          email: "null",
          gender: "null",
          location: "null",
          name: "G150",
          phone: "1",
        },
      ],
    };
  },
  methods: {

  },
};
</script>

<style scoped>
.user-profile {
  display: flex;
justify-content: space-between;

  margin: 20px;
  position: fixed;
  top: 70px;
}

.profile-card {
  display: flex;
  justify-content: space-between;

  width: 100%;
  margin-top: 20px;
}

.basic-info,
.behavior-info,
.preferences-info {
  width: 30%;
  border-color: #fcd34d;
}

.card-content {
  margin: 20px;
}

.select {
  left: 20%;
}
.chart{
background-color: white;
  height: 50vh;
  width: 50vh;
}
.gender{
width: 35%;
height: 57vh;
}
.age{
height: 57vh;
width: 33%;
}
</style>
