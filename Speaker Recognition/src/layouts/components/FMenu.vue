<template>
  <div class="f-menu" :style="{ width: $store.state.asideWidth }">
    <el-menu
      :unique-opened="true"
      active-text-color="#ffd04b"
      :collapse-transition="false"
      class="el-menu-vertical-demo border-0"

      @select="handleSelect"
      :default-active="defaultActive"
      :collapse="isCollapse"
    >
      <el-menu-item index="/">
        <el-icon>
          <Grid />
        </el-icon>
        <span>首页</span>
      </el-menu-item>
      <el-sub-menu index="2">
        <template #title>
          <el-icon>
            <location />
          </el-icon>
          <span>预处理</span>
        </template>
        <el-menu-item-group title="问题1：低采样率、低码率，进行数据增强">
          <el-menu-item index="enhance">音频增强</el-menu-item>
        </el-menu-item-group>
        <el-menu-item-group title="问题2：背景噪声的去除">
          <el-menu-item index="denoise">音频降噪</el-menu-item>
        </el-menu-item-group>
      </el-sub-menu>
      <el-sub-menu index="2">
        <template #title>
          <el-icon>
            <location />
          </el-icon>
          <span>声纹识别</span>
        </template>
        <el-menu-item-group title="一 对 一">
          <el-menu-item index="compare">声纹比较</el-menu-item>
        </el-menu-item-group>
        <el-menu-item-group title="问题3：识别说话人身份">
          <el-menu-item index="search">声纹检索</el-menu-item>
        </el-menu-item-group>
        <el-menu-item-group title="加入声纹库">
          <el-menu-item index="add" @click="dialogFormVisible = true"
            >添加声纹</el-menu-item
          >
      </el-menu-item-group>
      <el-menu-item-group title="用户画像">
        <el-menu-item index="user"
            >声纹库</el-menu-item>
          </el-menu-item-group>
      </el-sub-menu>
      <el-menu-item index="3">
        <el-icon>
          <ArrowUpBold />
        </el-icon>
        <span>已实现功能</span>
      </el-menu-item>
      <el-menu-item index="4" disabled>
        <el-icon>
          <document />
        </el-icon>
        <span>开发中.....</span>
      </el-menu-item>
      <el-dialog v-model="dialogFormVisible" title="特征与画像存入声纹库" class="z-50">
        <el-upload
          class="upload-demo w-80"
          :data="{ files: files }"
          :on-success="handleUploadSuccess"
          :file-list="fileList"
          :multiple="true"
          :auto-upload="false"
          :on-change="handleFileChange"
          :on-remove="remove"
        >
          <template #trigger>
            <el-button type="primary">选择音频文件(可批量上传)</el-button>
          </template>

          <template #tip>
            <div v-for="(item, index) in files" :key="index">
              <div class="text-l">请输入{{ item.file.name }} 音频的说话人：</div>

              <el-input
                v-model="item.file.id"
                class="w-50"
                placeholder="Name"
                clearable
                minlength="1"
                maxlength="10"
                show-word-limit="true"
                ><template #prefix>
                  <el-icon>
                    <User />
                  </el-icon> </template
              ></el-input>
              <div class="text-l">性别</div>
              <el-input
                v-model="item.file.gender"
                class="w-50"
                placeholder="Gender"
                clearable
                minlength="1"
                maxlength="1"
                show-word-limit="true"
                ></el-input>
                <div class="text-l">年龄</div>
              <el-input
                v-model="item.file.age"
                class="w-50"
                placeholder="Age"
                clearable
                minlength="1"
                maxlength="10"
                show-word-limit="true"
                ></el-input>
              <div class="text-l">联系方式</div>
              <el-input
                v-model="item.file.phone"
                class="w-50"
                placeholder="Phone"
                clearable
                minlength="1"
                maxlength="15"
                show-word-limit="true"
                ></el-input>
                <div class="text-l">邮箱</div>
              <el-input
                v-model="item.file.email"
                class="w-50"
                placeholder="Email"
                clearable
                minlength="1"
                maxlength="20"
                show-word-limit="true"
                ></el-input>
                <div class="text-l">住址</div>
              <el-input
                v-model="item.file.location"
                class="w-50"
                placeholder="Location"
                clearable
                minlength="1"
                maxlength="10"
                show-word-limit="true"
                ></el-input>
            </div>

          </template>
        </el-upload>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="killdialog">Cancel</el-button>
            <el-button type="primary" @click="submitFiles"> 确认上传 </el-button>
          </span>
        </template>
      </el-dialog>
    </el-menu>
  </div>
</template>

<script>
import { ElNotification } from "element-plus";
import img from "~/images/mic.png";
import axios from "~/axios.js";
export default {
  data() {
    return {
      img1: img,
      uploadFileList: [],
      res: 0,

      fileList: [],
      files: [],
true:true,
      man: "NULL",
      rate: "NULL",
      rate1: "NULL",
      loading: false,
      defaultActive: this.$route.path,
      dialogFormVisible: false,
    };
  },
  computed: {
    isCollapse() {
      return !(this.$store.state.asideWidth == '300px');
    },
  },
  methods: {
    killdialog() {
      this.dialogFormVisible = false;
      this.$router.back()
    },
    handleSelect(e) {
      console.log(e);
      this.$router.push("/"+e);
    },
    remove(uploadFile) {
      console.log(uploadFile);
      this.files.forEach((item, index, arr) => {
        if (item.id === uploadFile.id) {
          arr.splice(index, 1);
        }
        console.log(uploadFile);
      });
    },
    handleUploadSuccess(response) {
      // 处理上传成功后的逻辑
    },
    submitFiles() {
      this.dialogFormVisible = true;
      const formData = new FormData();
      for (let i = 0; i < this.files.length; i++) {
        console.log(this.files[i].file);
        console.log(this.files[i].file.raw);
        if (JSON.parse(JSON.stringify(this.files))[i].file.id == undefined) {
          ElNotification({
            message: "说话人不能为空",
            type: "error",
            duration: 3000,
          });
          this.$router.push("/");
          return;
        }
        formData.append("id", JSON.parse(JSON.stringify(this.files))[i].file.id);
        formData.append(
          "file_" + JSON.parse(JSON.stringify(this.files))[i].file.id,
          this.files[i].file.raw
        );
        formData.append(
          "gender_" + JSON.parse(JSON.stringify(this.files))[i].file.id,
          this.files[i].file.gender=="男"?1:0
        );
        formData.append(
          "email_" + JSON.parse(JSON.stringify(this.files))[i].file.id,
          this.files[i].file.email
        );
        formData.append(
          "location_" + JSON.parse(JSON.stringify(this.files))[i].file.id,
          this.files[i].file.location
        );
        formData.append(
          "age_" + JSON.parse(JSON.stringify(this.files))[i].file.id,
          this.files[i].file.age
        );
        formData.append(
          "phone_" + JSON.parse(JSON.stringify(this.files))[i].file.id,
          this.files[i].file.phone
        );
      }
      console.log(formData);
      console.log("id", formData.get("id"));
      axios
        .post("/add", formData)
        .then((res) => {
          console.log(res);
          ElNotification({
            message: "请求成功",
            type: "success",
            duration: 3000,
          });

        })
        .catch(() => {
          ElNotification({
            message: "请求失败，请检查声纹库是否重合及其他错误",
            type: "error",
            duration: 3000,
          });

        });
    },
    handleFileChange(UploadFile, UploadFiles) {
      console.log(UploadFile);
      console.log(UploadFiles);
      const files = UploadFiles;
      this.files = [];
      for (let i = 0; i < files.length; i++) {
        const file = files[i];
        const fileId = "";

        this.files.push({ file, id: fileId });
      }
      console.log(this.files);
    },
  },
};
</script>

<style scoped>
.f-menu {
  transition: all 0.2s;
  top: 64px;
  bottom: 0px;
  left: 0;
  overflow-x: hidden;
  overflow-y: auto;

  @apply shadow-md fixed bg-light-50;
}

el-menu-item {
  margin-top: 30px;
}
</style>
