[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{C8330D72-5C25-470F-9679-569A569A3B52}
AppName=NexaHub
AppVersion=1.0.0
AppPublisher=NexaHub
DefaultDirName={autopf}\NexaHub
DefaultGroupName=NexaHub
AllowNoIcons=yes
; Setup Icon (this is the icon for the installer file itself)
SetupIconFile=resources\icon.ico
; Uninstall Icon
UninstallDisplayIcon={app}\NexaHub.exe
Compression=lzma2
SolidCompression=yes
OutputDir=Installers
OutputBaseFilename=NexaHub_Setup_v1.0.0
; distinct from the content icon
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; The main executable and all dependencies from the dist folder
Source: "dist\main.dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\NexaHub"; Filename: "{app}\NexaHub.exe"; IconFilename: "{app}\resources\icon.ico"
Name: "{group}\{cm:UninstallProgram,NexaHub}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\NexaHub"; Filename: "{app}\NexaHub.exe"; Tasks: desktopicon; IconFilename: "{app}\resources\icon.ico"

[Run]
Filename: "{app}\NexaHub.exe"; Description: "{cm:LaunchProgram,NexaHub}"; Flags: nowait postinstall skipifsilent
