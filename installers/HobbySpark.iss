;##############################################################################
; HobbySpark Installer
; Part 1 / 3
;##############################################################################

#define MyAppName "HobbySpark"
#define MyAppVersion GetStringFileInfo(AddBackslash(SourcePath) + "..\dist\HobbySpark\HobbySpark.exe", "ProductVersion")
#if MyAppVersion == ""
    #define MyAppVersion "1.0.0"
#endif

#define MyAppPublisher "HobbySpark Industries"
#define MyAppURL ""
#define MyAppExeName "HobbySpark.exe"

[Setup]
AppId={{A36D7F42-1C76-4C77-BB77-56E8B55C3F01}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}

DefaultDirName={autopf}\HobbySpark
DefaultGroupName=HobbySpark

OutputDir=Output
OutputBaseFilename=HobbySparkSetup

Compression=lzma2
SolidCompression=yes
WizardStyle=modern

PrivilegesRequired=admin
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

DisableProgramGroupPage=yes
ChangesAssociations=no
AllowNoIcons=yes
CloseApplications=yes
RestartApplications=yes

SetupIconFile=icon.ico
UninstallDisplayIcon={app}\HobbySpark.exe

VersionInfoCompany=HobbySpark Industries
VersionInfoCopyright=© 2026 HobbySpark
VersionInfoDescription=HobbySpark Installer
VersionInfoProductName=HobbySpark
VersionInfoProductVersion={#MyAppVersion}

LicenseFile=license.txt

WizardResizable=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: desktopicon; Description: "Create a Desktop Shortcut"; GroupDescription: "Additional Icons:"

[Files]

;---------------------------------------------------------------------------
; HobbySpark Application
;---------------------------------------------------------------------------

Source: "..\dist\HobbySpark\*"; \
    DestDir: "{app}"; \
    Flags: ignoreversion recursesubdirs createallsubdirs

;---------------------------------------------------------------------------
; Bundled Installers
;---------------------------------------------------------------------------

Source: "python.exe"; \
    DestDir: "{tmp}"; \
    Flags: deleteafterinstall

Source: "arduino-cli.msi"; \
    DestDir: "{tmp}"; \
    Flags: deleteafterinstall

[Icons]

Name: "{group}\HobbySpark"; \
    Filename: "{app}\HobbySpark.exe"

Name: "{group}\Uninstall HobbySpark"; \
    Filename: "{uninstallexe}"

Name: "{autodesktop}\HobbySpark"; \
    Filename: "{app}\HobbySpark.exe"; \
    Tasks: desktopicon

;##############################################################################
; Pascal Code
; Part 2 / 3
;##############################################################################

[Code]

var
  PythonInstalled: Boolean;
  ArduinoCLIInstalled: Boolean;

function IsPythonInstalled(): Boolean;
var
  ResultCode: Integer;
begin
  Result :=
    Exec('cmd.exe',
      '/C python --version',
      '',
      SW_HIDE,
      ewWaitUntilTerminated,
      ResultCode) and (ResultCode = 0);
end;

function IsArduinoCLIInstalled(): Boolean;
var
  ResultCode: Integer;
begin
  Result :=
    Exec('cmd.exe',
      '/C arduino-cli version',
      '',
      SW_HIDE,
      ewWaitUntilTerminated,
      ResultCode) and (ResultCode = 0);
end;

procedure InstallPython();
var
  ResultCode: Integer;
begin
  if IsPythonInstalled() then
    Exit;

  WizardForm.StatusLabel.Caption :=
    'Installing Python...';

  if not Exec(
      ExpandConstant('{tmp}\python.exe'),
      '/quiet InstallAllUsers=1 PrependPath=1 Include_launcher=1',
      '',
      SW_SHOW,
      ewWaitUntilTerminated,
      ResultCode) then
  begin
    MsgBox(
      'Unable to launch the Python installer.',
      mbError,
      MB_OK);

    RaiseException('Python installation failed.');
  end;

  if ResultCode <> 0 then
  begin
    MsgBox(
      'Python installation failed.'#13#10 +
      'Exit Code: ' + IntToStr(ResultCode),
      mbError,
      MB_OK);

    RaiseException('Python installation failed.');
  end;
end;

procedure InstallArduinoCLI();
var
  ResultCode: Integer;
begin
  if IsArduinoCLIInstalled() then
    Exit;

  WizardForm.StatusLabel.Caption :=
    'Installing Arduino CLI...';

  if not Exec(
      'msiexec.exe',
      '/i "' +
      ExpandConstant('{tmp}\arduino-cli.msi') +
      '" /qn',
      '',
      SW_SHOW,
      ewWaitUntilTerminated,
      ResultCode) then
  begin
    MsgBox(
      'Unable to launch the Arduino CLI installer.',
      mbError,
      MB_OK);

    RaiseException('Arduino CLI installation failed.');
  end;

  if ResultCode <> 0 then
  begin
    MsgBox(
      'Arduino CLI installation failed.'#13#10 +
      'Exit Code: ' + IntToStr(ResultCode),
      mbError,
      MB_OK);

    RaiseException('Arduino CLI installation failed.');
  end;
end;

procedure ConfigureArduinoCLI();
var
  ResultCode: Integer;
begin

  WizardForm.StatusLabel.Caption :=
    'Configuring Arduino CLI...';

  if not Exec(
      'cmd.exe',
      '/C arduino-cli config init',
      '',
      SW_HIDE,
      ewWaitUntilTerminated,
      ResultCode) then
    RaiseException('Unable to initialize Arduino CLI.');

  if ResultCode <> 0 then
    RaiseException('Arduino CLI configuration failed.');

  if not Exec(
      'cmd.exe',
      '/C arduino-cli core update-index',
      '',
      SW_HIDE,
      ewWaitUntilTerminated,
      ResultCode) then
    RaiseException('Unable to update Arduino index.');

  if ResultCode <> 0 then
    RaiseException('Arduino CLI update-index failed.');

  if not Exec(
      'cmd.exe',
      '/C arduino-cli core install arduino:avr',
      '',
      SW_HIDE,
      ewWaitUntilTerminated,
      ResultCode) then
    RaiseException('Unable to install Arduino AVR core.');

  if ResultCode <> 0 then
    RaiseException('Arduino AVR core installation failed.');
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep <> ssInstall then
    Exit;

  InstallPython;
  InstallArduinoCLI;
  ConfigureArduinoCLI;
end;

;##############################################################################
; Final Sections
; Part 3 / 3
;##############################################################################

[Registry]

Root: HKLM; \
    Subkey: "Software\HobbySpark"; \
    ValueType: string; \
    ValueName: "InstallDir"; \
    ValueData: "{app}"; \
    Flags: uninsdeletekey

[Run]

Filename: "{app}\HobbySpark.exe"; \
    Description: "Launch HobbySpark"; \
    Flags: nowait postinstall skipifsilent

[UninstallDelete]

Type: filesandordirs; \
    Name: "{app}"

[UninstallRun]

Filename: "cmd.exe"; \
    Parameters: "/C arduino-cli cache clean"; \
    Flags: runhidden skipifdoesntexist

[Messages]

BeveledLabel=HobbySpark Installer
ButtonNext=Next >
ButtonBack=< Back
ButtonInstall=&Install
ButtonFinish=&Finish

WelcomeLabel1=Welcome to the HobbySpark Setup Wizard
WelcomeLabel2=This wizard will install HobbySpark on your computer.

FinishedHeadingLabel=Installation Complete
FinishedLabel=HobbySpark has been successfully installed.

ExitSetupMessage=Are you sure you want to exit the HobbySpark installer?

PreparingLabel=Preparing to install HobbySpark...

[CustomMessages]

InstallingPython=Installing Python...
InstallingArduinoCLI=Installing Arduino CLI...
InstallingAVR=Installing Arduino AVR Core...

[InstallDelete]

Type: files; \
    Name: "{tmp}\python.exe"

Type: files; \
    Name: "{tmp}\arduino-cli.msi"

