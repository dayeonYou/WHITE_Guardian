const { app, BrowserWindow, ipcMain } = require('electron');
const ipc = ipcMain;
// include the Node.js 'path' module at the top of your file
const path = require('path')


// modify your existing createWindow() function
function createWindow () {
  const win = new BrowserWindow({
    width: 1025,
    height: 700,
    frame: false,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation : false
    }
  })  
  win.loadFile('index.html')
  
  ipc.on('minimizeApp', ()=>{
    window.minimize();
  })

  ipc.on('maximizeApp', ()=>{
    if(window.isMaximized()){
      window.restore();
    } else {
      window.maximize();
    }
  })

  ipc.on('closeApp', ()=>{
    window.close();
  })
}
app.whenReady().then(() => {
  createWindow()
})
app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit()
})