<template>
  <el-row class="login-container">
    <el-col :lg="16" :md="12" class="left">
      <div>
        <div style="color: yellow">知言</div>
<div style="color: white" >基于编码器-时延网络的声纹识别平台</div>
        <div style="color: white">Welcome</div>


      </div>
      <img :src="img" alt="img" />

    </el-col>

    <el-col :lg="8" :md="12" class="right">
      <h2 class="title">欢迎回来</h2>
      <div>
        <span class="line"></span>
        <span>账号密码登录</span>
        <span class="line"></span>
      </div>
      <el-form ref="formRef" :rules="rules" :model="form" class="w-[250px]">
        <el-form-item prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名">
            <template #prefix>
              <el-icon>
                <User />
              </el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="form.password" placeholder="请输入密码" type="password" show-password>
            <template #prefix>
              <el-icon>
                <Lock />
              </el-icon>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" class="w-[250px]" round @click="onSubmit" :loading="loading
          ">登录</el-button>
        </el-form-item>
      </el-form>
    </el-col>
  </el-row>
</template>

<script setup>
import  img from "~/images/5.png";
import axios from "~/axios";
import { reactive, ref } from "vue";
import { User, Lock } from "@element-plus/icons-vue";
import { login } from "~/api/manager";
import { ElNotification } from 'element-plus'
import { useCookies } from '@vueuse/integrations/useCookies'
import { useRouter } from "vue-router";
const router =useRouter()
const cookie = useCookies()
// do not use same name with ref
const loading = ref(false)
const form = reactive({
  username: "",
  password: "",
});
const rules = {
  username: [{ required: true, message: "用户名不能为空", trigger: "blur" }],
  password: [{ required: true, message: "密码不能为空", trigger: "blur" }],
};

const onSubmit = () => {
  formRef.value.validate((vaild) => {
    if (!vaild) {
      return false;
    }

    console.log("验证通过");
  })
  if (form.username == "admin" && form.password == "admin") {
    ElNotification({
      title: 'Success',
      message: '登录成功',
      type: 'success',
      duration: 3000
    })
    router.push("/")
    cookie.set("admin-token", "123456")
axios.post("/all").then((res) => {this.$store.state.profile=res.data}).catch((err) =>{ ElNotification({
            message: "声纹库请求失败",
            type: "info",
            duration: 3000,
          });})
  }
  else {
    ElNotification({

      message: err.response.data.msg || "请求失败",
      type: 'error',
      duration: 3000
    })

  }
}
/*login(form.username, form.password)
  .then((res) => {
    console.log(res);
    ElNotification({
      title: 'Success',
      message: '登录成功',
      type: 'success',
    })
    const cookie = useCookies()
    cookie.set("admin-token", "")
  })
  .catch((err) => {
    ElNotification({

      message: err.response.data.msg || "请求失败",
      type: 'error',
      duration: 3000
    }).finally(() => {
loading.value = false
})
  });
})
};*/
const formRef = ref(null);
</script>

<style>
* {
  margin: 0;
  padding: 0;
}

.login-container {
  @apply bg-indigo-500 min-h-screen;
}

.login-container .left,
.login-container .right {
  @apply flex justify-center items-center;
}

.login-container .right {
  @apply bg-light-50 flex-col;
}

.left>div>div:first-child {
  @apply font-bold text-5xl mb-4;
}

.left>div>div:last-child {
  @apply font-bold text-5xl mb-4;
}

.right .title {
  @apply font-bold text-3xl text-gray-800;
}

.right>div {
  @apply flex items-center justify-center my-5 text-gray-300 space-x-2;
}

.line {
  @apply h-[1px] w-16 bg-gray-200;
}

</style>
