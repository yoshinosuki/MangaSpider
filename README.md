# 一款网络爬虫

## 效果图
<img src="./README/示例.jpg">

## 使用方法
- 运行GetID，获取某个分类下的前5页内容（可自定义分类和书页）
- 运行handingOut分配任务（不要多次运行，否则会因为覆盖而产生异常）
- 运行FastDL进行下载任务
- 运行完成后在book文件夹即可找到
- 可以使用downpdf直接将文件夹内的图书转换成pdf
- 可以使用read读取book文件夹内全部图书
- 如遇修复不了的意外，可将未下载完成的图书id加入Target_Restart文件中，运行restart。
    或者运行fix.py自动检查错误

## powershell启动示例
```powershell
# 设置路径变量 python位置，该项目所在位置
$pythonExe = "C:\Personal storage\app\python\python.exe"
$scriptPath = "E:\Storage\Book\Manga\Hanime\spider1"

$choice = Read-Host "输入'111'从获取ID开始 或 输入'222'从上次下载进度开始`n"
Set-Location $scriptPath

if ($choice -eq '111') {
    & $pythonExe "$scriptPath\GetID.py"
    Start-Sleep -Seconds 3
    & $pythonExe "$scriptPath\handingOut.py"
    Start-Sleep -Seconds 3
    & $pythonExe "$scriptPath\FastDL.py"
    Start-Sleep -Seconds 3
    & $pythonExe "$scriptPath\fix.py"

    Pause
} elseif ($choice -eq '222') {
    & $pythonExe "$scriptPath\FastDL.py"
    Start-Sleep -Seconds 3
    & $pythonExe "$scriptPath\fix.py"
} else {
    Write-Host "无效输入，请输入 '111' 或 '222'."
}

```



## 文件夹（除了Book内的）不要删，也不要动！！！！

### 1.3
- **修复了因多进程导致的互锁问题**
- 加入断点续传
- 加入下载文件的完整性检查
- 优化代码结构，方便维护修改

### 1.2
- 可以使用downpdf直接将文件夹内的图片转换成pdf
- 自动生成分类pdf
- 加入多线程一键启动

### 1.1
- 正式版 一款网络爬虫
 
使用方法
- 选好想要的书籍id，填入new.txt
- 运行main.py
- 运行完成后在book文件夹即可找到
- 可以使用read读取book文件夹内全部图片