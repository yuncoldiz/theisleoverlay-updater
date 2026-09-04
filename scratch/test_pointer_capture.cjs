const { app, BrowserWindow } = require('electron');

app.whenReady().then(() => {
  const win = new BrowserWindow({ width: 400, height: 400, show: false });
  win.loadURL('data:text/html,<!DOCTYPE html><html><body><div id="box" style="width:200px;height:200px;background:red;"></div><script>box.onpointerdown = (e) => { Promise.resolve().then(() => { try { box.setPointerCapture(e.pointerId); console.log("Capture SUCCESS"); } catch(err) { console.log("Capture FAILED:", err.name, err.message); } }); };</script></body></html>');
  win.webContents.on('console-message', (e, level, message) => {
    console.log('[BROWSER CONSOLE]', message);
    app.quit();
  });
  win.webContents.once('did-finish-load', () => {
    win.webContents.sendInputEvent({ type: 'pointerDown', x: 50, y: 50, button: 'left', clickCount: 1 });
  });
});
