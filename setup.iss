#define AppName "TheIsleVn-BanhMi"
#define AppVersion "1.0.6"
#define AppPublisher "BanhMiBietChoi"
#define AppExeName "TheIsleVn-BanhMi.exe"

[Setup]
; Unique App ID for Windows installation registry
AppId={{2A8E6C2D-6F2D-4E1B-943C-A1A4A0F9B2C2}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
DefaultDirName={localappdata}\Programs\{#AppName}
AppendDefaultDirName=no
DefaultGroupName={#AppName}
DisableProgramGroupPage=yes
DisableWelcomePage=no
DisableDirPage=no
PrivilegesRequired=admin
CloseApplications=force
RestartApplications=no
; Setup compiler configurations
OutputDir=.
OutputBaseFilename={#AppName}-Setup
SetupIconFile=src_extracted\electron\tray.ico
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; --- VISIBLE FILES ---
; The main executable runs directly and is the only app file visible to users
Source: "TheIsleVn-BanhMi.exe"; DestDir: "{app}"; Flags: ignoreversion

; --- HIDDEN FILES (Attribs: hidden) ---
; All DLLs, paks, bins, and resources are set to hidden for a clean folder layout
Source: "d3dcompiler_47.dll"; DestDir: "{app}"; Flags: ignoreversion; Attribs: hidden
Source: "ffmpeg.dll"; DestDir: "{app}"; Flags: ignoreversion; Attribs: hidden
Source: "icudtl.dat"; DestDir: "{app}"; Flags: ignoreversion; Attribs: hidden
Source: "libEGL.dll"; DestDir: "{app}"; Flags: ignoreversion; Attribs: hidden
Source: "libGLESv2.dll"; DestDir: "{app}"; Flags: ignoreversion; Attribs: hidden
Source: "vk_swiftshader.dll"; DestDir: "{app}"; Flags: ignoreversion; Attribs: hidden
Source: "vulkan-1.dll"; DestDir: "{app}"; Flags: ignoreversion; Attribs: hidden
Source: "chrome_100_percent.pak"; DestDir: "{app}"; Flags: ignoreversion; Attribs: hidden
Source: "chrome_200_percent.pak"; DestDir: "{app}"; Flags: ignoreversion; Attribs: hidden
Source: "resources.pak"; DestDir: "{app}"; Flags: ignoreversion; Attribs: hidden
Source: "snapshot_blob.bin"; DestDir: "{app}"; Flags: ignoreversion; Attribs: hidden
Source: "v8_context_snapshot.bin"; DestDir: "{app}"; Flags: ignoreversion; Attribs: hidden
Source: "vk_swiftshader_icd.json"; DestDir: "{app}"; Flags: ignoreversion; Attribs: hidden

; Locales folder (hidden)
Source: "locales\*"; DestDir: "{app}\locales"; Flags: ignoreversion recursesubdirs createallsubdirs; Attribs: hidden

; Resources folders (hidden & clean: excludes massive dev backup files to keep setup small)
Source: "resources\app.asar"; DestDir: "{app}\resources"; Flags: ignoreversion; Attribs: hidden
Source: "resources\app-update.yml"; DestDir: "{app}\resources"; Flags: ignoreversion; Attribs: hidden
Source: "resources\elevate.exe"; DestDir: "{app}\resources"; Flags: ignoreversion; Attribs: hidden
Source: "resources\bin\*"; DestDir: "{app}\resources\bin"; Flags: ignoreversion recursesubdirs createallsubdirs; Attribs: hidden
Source: "resources\app.asar.unpacked\*"; DestDir: "{app}\resources\app.asar.unpacked"; Flags: ignoreversion recursesubdirs createallsubdirs; Attribs: hidden

; Temporary Npcap driver installer (extracted only if machine does not have Npcap)
Source: "dependencies\npcap-installer.exe"; DestDir: "{tmp}"; Flags: ignoreversion deleteafterinstall; Check: NeedsNpcap

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExeName}"
Name: "{commondesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: desktopicon

[Run]
; Silently install Npcap driver if missing before launching app
Filename: "{tmp}\npcap-installer.exe"; StatusMsg: "Đang mở trình cài đặt Npcap Driver..."; Flags: waituntilterminated; Check: NeedsNpcap
Filename: "{app}\{#AppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(AppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Clean up local user settings log directory on uninstall
Type: files; Name: "{userappdata}\theisleinformation-bybanhmibietchoi\*.*"
Type: dirifempty; Name: "{userappdata}\theisleinformation-bybanhmibietchoi"

[Code]
function NeedsNpcap(): Boolean;
begin
  // Returns True if Npcap is NOT installed yet on the system
  if RegKeyExists(HKEY_LOCAL_MACHINE, 'SOFTWARE\Npcap') or
     RegKeyExists(HKEY_LOCAL_MACHINE, 'SOFTWARE\WOW6432Node\Npcap') or
     FileExists(ExpandConstant('{win}\System32\Npcap\wpcap.dll')) or
     FileExists(ExpandConstant('{win}\SysWOW64\Npcap\wpcap.dll')) then
  begin
    Result := False;
  end
  else
  begin
    Result := True;
  end;
end;
