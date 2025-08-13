# 安装基本属性：
npm install electron --save-dev
运行时node 另外打包
# Example:
```
// const { app, BrowserWindow } = require('electron')
import { app, BrowserWindow } from 'electron'
const createWindow = () => {
  const win = new BrowserWindow({
    width: 800,
    height: 600
  })

  win.loadFile('index.html')
}

app.whenReady().then(() => {
  createWindow()
})
```

app, which controls your application's event lifecycle.
BrowserWindow, which creates and manages app windows.
小驼峰 实例，大驼峰构造函数