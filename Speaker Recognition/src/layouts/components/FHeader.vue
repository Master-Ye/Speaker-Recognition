<template>
    <div class="f-header">
        <span class="logo">
            <el-icon class="mr-1">
                <Odometer />
            </el-icon>
            声纹识别平台
        </span>
        <el-tooltip effect="dark" content="折叠" placement="bottom">
        <el-icon class="icon-btn" @click="$store.commit('handleAsideWidth')">

            <Fold  v-if="$store.state.asideWidth=='300px'"/>
            <Expand v-else />
        </el-icon>
        </el-tooltip>
        <el-tooltip effect="dark" content="刷新" placement="bottom">
            <el-icon class="icon-btn">
                <Refresh @click="handleRefresh()" />
            </el-icon>
        </el-tooltip>
        <div class="ml-auto flex items-center">
            <el-tooltip effect="dark" content="全屏" placement="bottom">
                <el-icon class="icon-btn" @click="toggle">

                    <FullScreen v-if="!isFullscreen"/>
                    <Aim v-else/>
                </el-icon>
            </el-tooltip>
            <el-dropdown class="dropdown" @command="handleCommand">
                <span class="flex items-center text-light-50">
                    <el-avatar class="mr-2" :size="25" :src="$store.state.user.avatar" />
                    {{ $store.state.user.username }}
                    <el-icon class="el-icon--right">
                        <arrow-down />
                    </el-icon>
                </span>
                <template #dropdown>
                    <el-dropdown-menu>
                        <el-dropdown-item command="rePassword">修改密码</el-dropdown-item>
                        <el-dropdown-item command="logout">退出登录</el-dropdown-item>
                    </el-dropdown-menu>
                </template>
            </el-dropdown>
        </div>
    </div>
</template>

<script setup>
import { showModal } from "~/composables/util"
import { removeToken } from "~/composables/auth"
import { useRouter } from "vue-router"
import {useFullscreen} from "@vueuse/core"
const {isFullscreen,toggle}=useFullscreen()
const router = useRouter()

const handleCommand = (c) => {
    switch (c) {
        case "logout":
            logout();
            break;
        case "rePassword":
            console.log("")
            break;
    }

}
function logout() {
    showModal("是否要退出登录").then(res => {
        console.log("退出登陆")
        removeToken()
        router.push("/login")
    })

}
const handleRefresh = () => location.reload()
</script>

<style scoped>
.f-header {
    @apply flex items-center bg-indigo-500 text-light-50 fixed top-0 left-0 right-0;
    height: 64px;
}

.logo {
    width: 250px;
    @apply flex justify-center items-center text-xl font-thin;
}

.icon-btn {
    @apply flex justify-center items-center;
    width: 42px;
    height: 64px;
    cursor: pointer;
}

.icon-btn:hover {
    @apply bg-indigo-400;
}

.f-header .dropdown {
    height: 64px;
    cursor: pointer;
    @apply flex justify-center items-center mx-5;
}
</style>