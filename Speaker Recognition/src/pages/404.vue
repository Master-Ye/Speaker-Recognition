<template>
<div>
    <el-result
        icon="warning"
        title="404提示"
        sub-title="页面走丢了"
      >
        <template #extra>
          <el-button type="primary" @click="$router.push('/')">Back</el-button>
        </template>
      </el-result>
</div>
</template>

<script>
export default {

}
</script>

<style>

</style>