# PedestriansDetection
> 本项目为第八届中国软件杯大学生软件设计大赛赛题“公共地点人流量计算的云监管平台”作品，由图南队共同完成。

### 项目说明
本项目总体共分三部分cloud、terminal、mobile分别为云端、边缘端、移动端代码。  
- 云端：进行数据存储、人头数排序  
- 边缘端：与摄像头相连接，实时分析视频数据并计算人头数，将数据传送至云端，同时在人头数达到阈值时自动报警。  
- 移动端：数据在微信小程序上进行展示  

---
### 运行方式

#### 启动云端
运行环境：  
-	Window 10 64位  
-	确保80端口未被占用（如被占用，可使用其它端口，方法见步骤4）  
注：为使运行方便，数据库已迁移至sqlite3数据库  

运行步骤：  
1)	打开“云端”文件夹，双击“点我运行.bat”，屏幕上出现一个黑窗口  
 
2)	待屏幕中出现“Starting development server at……”字样即启动成功  
 
3)	在本机使用浏览器访问http://127.0.0.1/index 即可访问云平台页面，其它计算机访问http:// + ip地址 + /index（须与本机保持网络联通）  
 
4)	如80端口被占用，可进入manage文件夹，运行cmd命令：  

#### 启动边缘端

运行环境：  
- Windows 10 64位  
- 与云端主机网络联通  
运行步骤：  
1)	在三台电脑上分别打开“边缘端”文件夹，双击“点我运行.bat”，屏幕上出现一个黑窗口  
 
2)	根据提示分别输入云端主机与端口号（默认为80）  
 
3)	分别输入地点编号并选择示例视频（或摄像头）  
 
4)	到云平台可监测到数据变化  

#### 小程序端

微信小程序无可执行文件、安装包，可使用微信扫描以下小程序码进行体验：  
- 小程序的云端部署在我们自己服务器上  
- 运行环境：可联网的移动设备  

---

### 程序截图  

![监控页面](http://www.tunan.work:8090/upload/2019/8/%E7%9B%91%E6%8E%A7%E9%A1%B5%E9%9D%A2-924e9fad6aaa417a9b72ff4f70345b8e.png)
