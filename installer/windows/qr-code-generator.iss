#define AppName "QR Code Generator"
#define AppVersion "0.1.0"
#define AppExeName "QR Code Generator.exe"

[Setup]
AppId={{FA8DDF23-9E31-4A2B-9D1C-11A9ABDA5F52}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher=QR Code Generator
DefaultDirName={autopf}\QR Code Generator
DefaultGroupName={#AppName}
PrivilegesRequired=lowest
ArchitecturesInstallIn64BitMode=x64
OutputDir=..\..\dist
OutputBaseFilename=QR-Code-Generator-Setup
SetupIconFile=..\..\build\qr_gen_icon.ico
UninstallDisplayIcon={app}\{#AppExeName}
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional shortcuts:"

[Files]
Source: "..\..\dist\QR Code Generator\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\{#AppName}"; Filename: "{app}\{#AppExeName}"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#AppExeName}"; Description: "Launch {#AppName}"; Flags: postinstall nowait skipifsilent
