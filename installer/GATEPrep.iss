; Inno Setup script — builds installer\Output\GATEPrep-Setup-<version>.exe
; Per-user install (no admin rights), Start-menu + optional desktop icon, proper uninstaller, silent-upgrade friendly.
#define AppName "GATE Prep"
#define AppVersion GetEnv("GATEPREP_VERSION")
#if AppVersion == ""
  #define AppVersion "1.0.0"
#endif

[Setup]
AppId={{6B1D2E5C-3F0A-4C9E-9B7A-0A7E9CE00001}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher=GATE Prep
DefaultDirName={localappdata}\Programs\GATEPrep
DefaultGroupName={#AppName}
PrivilegesRequired=lowest
OutputDir=Output
OutputBaseFilename=GATEPrep-Setup-{#AppVersion}
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
UninstallDisplayName={#AppName}
UninstallDisplayIcon={app}\GATEPrep.exe
CloseApplications=yes
RestartApplications=yes
DisableProgramGroupPage=yes

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Shortcuts:"

[Files]
Source: "..\dist\GATEPrep\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\{#AppName}"; Filename: "{app}\GATEPrep.exe"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\GATEPrep.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\GATEPrep.exe"; Description: "Launch {#AppName}"; Flags: nowait postinstall skipifsilent

; Your progress is stored in %LOCALAPPDATA%\GATEPrep and is intentionally NOT removed on uninstall/upgrade.
