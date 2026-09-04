const nw = require('../src_extracted/electron/native-windows.cjs');
const GAME_WINDOW_RE = /theisle|isle-win64/i;

const hwnd = nw.findWindow((title, path, pid) => {
  console.log('Checked:', { title, path, pid });
  return GAME_WINDOW_RE.test(path);
});

console.log('Result hwnd:', hwnd);
