const { app, BrowserWindow, Menu, Tray, ipcMain, screen } = require('electron');
const path = require('path');

let mainWindow;
let tray;

function createWindow() {
  const { width, height } = screen.getPrimaryDisplay().workAreaSize;
  
  mainWindow = new BrowserWindow({
    width: width,
    height: 100,
    x: 0,
    y: height - 100,
    frame: false,
    transparent: true,
    alwaysOnTop: true,
    skipTaskbar: true,
    resizable: false,
    movable: false,
    minimizable: false,
    maximizable: false,
    closable: false,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      enableRemoteModule: true
    }
  });

  mainWindow.loadFile('index.html');
  
  mainWindow.setIgnoreMouseEvents(false);
  
  mainWindow.on('closed', () => {
    mainWindow = null;
  });

  createTray();
}

function createTray() {
  tray = new Tray(path.join(__dirname, 'assets', 'tray-icon.png'));
  
  const contextMenu = Menu.buildFromTemplate([
    {
      label: '設定',
      click: () => {
        console.log('Settings clicked');
      }
    },
    {
      label: '図鑑',
      click: () => {
        console.log('Encyclopedia clicked');
      }
    },
    {
      type: 'separator'
    },
    {
      label: '終了',
      click: () => {
        app.quit();
      }
    }
  ]);
  
  tray.setToolTip('Bug Buddies');
  tray.setContextMenu(contextMenu);
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

ipcMain.on('feed-insects', (event, x, y) => {
  console.log(`Feed dropped at: ${x}, ${y}`);
});
