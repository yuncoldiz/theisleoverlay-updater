#define AppName "TheIsleVn-BanhMi"
#define AppVersion "1.0.4"
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
PrivilegesRequired=lowest
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
Source: "resources\app.asar.unpacked\*"; DestDir: "{app}\resources\app.asar.unpacked"; Flags: ignoreversion recursesubdirs createallsubdirs; Attribs: hidden

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExeName}"
Name: "{commondesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#AppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(AppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Clean up local user settings log directory on uninstall
Type: files; Name: "{userappdata}\theisleinformation-bybanhmibietchoi\*.*"
Type: dirifempty; Name: "{userappdata}\theisleinformation-bybanhmibietchoi"
