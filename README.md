# COM_2_2_PY

### 使用说明：
本程序会使用config.txt文件中标记出的端口进行操作，目前只支持READWRITE模式
会对端口进行收发，将一个端口上收到的数据发送到另一个端口上，而且是双向的，同时将收到的数据打印到屏幕上

本程序会读取运行和main.exe同一目录下的config.txt文件，
限定两行：
COM10 115200 READWRITE
COM11 115200 READWRITE
ONLY TWO LINES PERMITTED
目前只支持READWRITE模式

contact.exe 为主程序，运行后会自动打开一个窗口对收到的数据自动进行转发
comm_gazer.exe 为辅助程序，可以通过插拔USB设备显示插拔设备的COM号从而帮助方便找到需要通信转发的端口号

