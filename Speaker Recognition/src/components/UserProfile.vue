<template>
    <div class="user-profile"  v-for="(item,index) of profile"  :key="index" >

      <h2>{{ item.name }} 的用户画像</h2>
      <div class="profile-card">
        <el-card class="basic-info rounded-2xl" >
          <div slot="header">
            <h2 class="font-bold">个人信息</h2>
          </div>
          <div class="card-content flex flex-wrap justify-between">
            <div class="w-25 h-20  border-2 rounded-2xl inline-block " >
              <el-icon><UserFilled /></el-icon>
<div class="m-auto text-center font-bold">{{ item.name }}</div>
          </div>

          <div class="w-25 h-20  border-2 rounded-2xl inline-block " >
            <el-icon v-if=" profile.gender=='Male' " ><Male  /></el-icon>
            <el-icon v-else><Female /></el-icon>
<div class="m-auto text-center font-bold">{{ item.gender }} {{ item.age }}岁</div>
          </div>
          <div class="w-53 h-20  border-2 rounded-2xl inline-block mt-4" >
            <el-icon><PhoneFilled /></el-icon>
<div class="m-auto text-center font-bold">{{ item.phone }}</div>
          </div>
          <div class="w-53 h-20  border-2 rounded-2xl inline-block mt-4" >
            <el-icon><Message /></el-icon>
<div class="m-auto text-center font-bold">{{ item.email }}</div>

          </div>
          <div class="w-53 h-20  border-2 rounded-2xl inline-block mt-4" >
           <el-icon><Location /></el-icon>
<div class="m-auto text-center font-bold">{{ item.location }} </div>
          </div>
          </div>
        </el-card>
        <el-card class="behavior-info">

        </el-card>

      </div>
    </div>
  </template>

  <script>
  export default {
    name: "UserProfile",
    props: {
      profile: Array,
    },
    data(){
      return {
 index:0,
      }
    }
  };
  </script>

  <style scoped>

.user-profile {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 20px;
}

.profile-card {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  width: 100%;
  margin-top: 20px;
}

.basic-info,
.behavior-info,
.preferences-info {
  width: 30%;
}

.card-content {
  margin: 20px;
}
</style>

