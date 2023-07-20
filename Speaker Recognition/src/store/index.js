
import { createStore } from 'vuex'

// 创建一个新的 store 实例
const store = createStore({
  state () {
    return {
      user:{
        username:"admin",
avatar:"11",

      },
      asideWidth:"300px",
user:[],
profile:[]
    }
  },
  mutations:{
handleAsideWidth(state){
state.asideWidth=state.asideWidth=="300px"?"64px":"300px"
  }

}})
export default store