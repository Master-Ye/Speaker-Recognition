<template>
  <div>
    <img :src="img" alt="img"  class="w-400px h-200px img1"/>


    <el-carousel :interval="4000" type="card" class="mt-60">
      <el-carousel-item v-for="item in robot" :key="item" style="border: 2px soild">
        <img :src="item.src"/>
      </el-carousel-item>
    </el-carousel>


  </div>
</template>

<script>
import  img from "~/images/40.png";
import img1 from '~/images/5.jpg'
import img2 from '~/images/6.jpg'
import img3 from "~/images/2.png"
import img4 from "~/images/8.png"
import img5 from "~/images/7.png"
export default {
  data() {
    return {
      robot: [{src:img5},{src:img4}],
      img:img,

    };
  }
}
</script>

<style scoped>

.img1{position: absolute;
top: 64px;

}
.text{
position: absolute;
top: 150px;
}
.el-carousel__item h3 {
  color: #475669;
  opacity: 0.75;

  margin: 0;
  text-align: center;
}
.lunbo{


}
.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n + 1) {
  background-color: #d3dce6;
}
img{

margin:0px;
background: no-repeat;
background-size:100% 100%;
background-attachment:fixed;
}
</style>