const koffi = require('koffi');
const user32 = koffi.load('user32.dll');
const kernel32 = koffi.load('kernel32.dll');

const GetLastError = kernel32.func('uint32 __stdcall GetLastError()');
const HWND = koffi.pointer('HWND', koffi.opaque());
const EnumWindowsProc = koffi.proto('int __stdcall EnumWindowsProc(HWND hwnd, intptr lparam)');
const EnumWindows = user32.func('int __stdcall EnumWindows(EnumWindowsProc *cb, intptr lparam)');

let count = 0;
const cb = koffi.register((hwnd, lparam) => {
  count++;
  return 1;
}, 'EnumWindowsProc *');

try {
  const res = EnumWindows(cb, 0);
  console.log('EnumWindows result:', res, 'Count:', count, 'LastError:', GetLastError());
} catch (e) {
  console.error('Error:', e);
} finally {
  koffi.unregister(cb);
}
