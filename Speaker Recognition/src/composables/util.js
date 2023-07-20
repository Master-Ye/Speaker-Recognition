import {ElMessageBox}from "element-plus"
import "nprogress/nprogress.css"
import  nprogress from  'nprogress'
export function showModal(content,type="warning",title="")
{
return ElMessageBox.confirm(
    content,
    title,
    {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: type,
    }
  )
}
//显示Loading
export function showFullLoading(){
  nprogress.start()
}
export function hideFullLoading(){
  nprogress.done()
}