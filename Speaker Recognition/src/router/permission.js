import router from "~/router/index.js";
import { getToken } from "~/composables/auth.js";
import{ showFullLoading ,hideFullLoading} from "~/composables/util";
import * as echarts from "echarts";
router.beforeEach(async(to, from, next) => {
//显示loading
showFullLoading()
  let token = getToken();
if(!token&&to.path!="/login"){
return next({path:"/login"})
}

let title=(to.meta.title?to.meta.title:"")+"--声纹识别"
document.title=title
next()

});
router.afterEach((to, from) => {
    hideFullLoading()
  })