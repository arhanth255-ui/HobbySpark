;###############################################################################
;
; HobbySpark Installer
; Version 1.0
;
; Part 1/?
;
;###############################################################################

#ifndef AppVersion
#define AppVersion "DEV"
#endif

#define MyAppName        "HobbySpark"
#define MyAppVersion     AppVersion
#define MyAppPublisher   "HobbySpark Industries"
#define MyAppExeName     "HobbySpark.exe"

[Setup]

AppId={{A1D35F0A-9E7D-45D0-97AF-91C34E2D1B61}

AppName={#MyAppName}
AppVersion={#MyAppVersion}

AppPublisher={#MyAppPublisher}

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

DisableDirPage=no
DisableProgramGroupPage=yes

AllowNoIcons=yes

SetupIconFile=icon.ico

UninstallDisplayIcon={app}\{#MyAppExeName}

VersionInfoCompany=HobbySpark Industries
VersionInfoProductName=HobbySpark
VersionInfoProductVersion=1.0.0.0
VersionInfoDescription=HobbySpark Installer
VersionInfoCopyright=© 2026 HobbySpark

CloseApplications=yes
RestartApplications=yes

WizardResizable=yes

UsePreviousAppDir=no
UsePreviousLanguage=yes

[Languages]

Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]

Name: desktopicon; Description: "Create Desktop Shortcut"; GroupDescription: "Additional Icons:"

[Dirs]

Name: "{app}"

[Files]

;==============================================================================
; HobbySpark
;==============================================================================

Source: "..\dist\HobbySpark\*"; \
    DestDir: "{app}"; \
    Flags: ignoreversion recursesubdirs createallsubdirs

;==============================================================================
; Dependencies
;==============================================================================

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

;###############################################################################
; Code
;###############################################################################

[Code]

const
  PythonInstaller = '{tmp}\python.exe';
  ArduinoInstaller = '{tmp}\arduino-cli.msi';

var
  InstallLabel: TNewStaticText;

function RunAndWait(FileName, Params: String): Integer;
var
  ResultCode: Integer;
begin
  Log('Running: ' + FileName + ' ' + Params);

  if not Exec(
      FileName,
      Params,
      '',
      SW_SHOW,
      ewWaitUntilTerminated,
      ResultCode)
  then
  begin
      MsgBox(
        'Unable to execute:'#13#10 + FileName,
        mbCriticalError,
        MB_OK);

      WizardForm.Close;
  end;

  Result := ResultCode;
end;

procedure Status(const S: String);
begin
  Log(S);

  if Assigned(InstallLabel) then
      InstallLabel.Caption := S;

  WizardForm.StatusLabel.Caption := S;
end;

function PythonInstalled(): Boolean;
var
  Code: Integer;
begin
  Result :=
      Exec(
          'cmd.exe',
          '/C python --version',
          '',
          SW_HIDE,
          ewWaitUntilTerminated,
          Code)
      and
      (Code = 0);
end;

function ArduinoCLIInstalled(): Boolean;
var
  Code: Integer;
begin
  Result :=
      Exec(
          'cmd.exe',
          '/C arduino-cli version',
          '',
          SW_HIDE,
          ewWaitUntilTerminated,
          Code)
      and
      (Code = 0);
end;

procedure InstallPython;
var
  ExitCode: Integer;
begin

  if PythonInstalled() then
  begin
      Log('Python already installed.');
      Exit;
  end;

  Status('Installing Python...');

  ExitCode :=
      RunAndWait(
          ExpandConstant(PythonInstaller),
          '/quiet InstallAllUsers=1 PrependPath=1 Include_launcher=1');

  if ExitCode <> 0 then
  begin
      MsgBox(
          'Python installation failed.'#13#10 +
          'Exit code: ' + IntToStr(ExitCode),
          mbCriticalError,
          MB_OK);

      WizardForm.Close;
  end;

end;

procedure InstallArduinoCLI;
var
  ExitCode: Integer;
begin

  if ArduinoCLIInstalled() then
  begin
      Log('Arduino CLI already installed.');
      Exit;
  end;

  Status('Installing Arduino CLI...');

  ExitCode :=
      RunAndWait(
          'msiexec.exe',
          '/i "' +
          ExpandConstant(ArduinoInstaller) +
          '" /qn');

  if ExitCode <> 0 then
  begin

      MsgBox(
          'Arduino CLI installation failed.'#13#10 +
          'Exit code: ' + IntToStr(ExitCode),
          mbCriticalError,
          MB_OK);

      WizardForm.Close;

  end;

end;

procedure ConfigureArduinoCLI;
var
  ExitCode: Integer;
begin

  Status('Initializing Arduino CLI...');

  ExitCode :=
      RunAndWait(
          'cmd.exe',
          '/C arduino-cli config init');

  if ExitCode <> 0 then
  begin
      MsgBox(
          'Unable to initialize Arduino CLI.',
          mbCriticalError,
          MB_OK);

      WizardForm.Close;
      Exit;
  end;

  Status('Updating board index...');

  ExitCode :=
      RunAndWait(
          'cmd.exe',
          '/C arduino-cli core update-index');

  if ExitCode <> 0 then
  begin
      MsgBox(
          'Unable to update the Arduino board index.',
          mbCriticalError,
          MB_OK);

      WizardForm.Close;
      Exit;
  end;

  Status('Installing Arduino AVR Core...');

  ExitCode :=
      RunAndWait(
          'cmd.exe',
          '/C arduino-cli core install arduino:avr');

  if ExitCode <> 0 then
  begin
      MsgBox(
          'Failed to install the Arduino AVR Core.',
          mbCriticalError,
          MB_OK);

      WizardForm.Close;
      Exit;
  end;

  Log('Arduino AVR Core installed successfully.');

end;

procedure InitializeWizard;
begin

  InstallLabel :=
      TNewStaticText.Create(WizardForm);

  InstallLabel.Parent :=
      WizardForm;

  InstallLabel.Left := ScaleX(0);
  InstallLabel.Top := ScaleY(180);
  InstallLabel.Width := ScaleX(430);

  InstallLabel.Caption :=
      'Preparing installation...';

end;

procedure CurStepChanged(CurStep: TSetupStep);
begin

  if CurStep <> ssPostInstall then
      Exit;

  Status('Checking Python...');
  InstallPython;

  Status('Checking Arduino CLI...');
  InstallArduinoCLI;

  Status('Configuring Arduino CLI...');
  ConfigureArduinoCLI;

  Status('Installation complete.');

end;

;###############################################################################
; Registry
;###############################################################################

[Registry]

Root: HKLM; \
    Subkey: "Software\HobbySpark"; \
    ValueType: string; \
    ValueName: "InstallDir"; \
    ValueData: "{app}"; \
    Flags: uninsdeletekey

Root: HKLM; \
    Subkey: "Software\HobbySpark"; \
    ValueType: string; \
    ValueName: "Version"; \
    ValueData: "{#MyAppVersion}"; \
    Flags: uninsdeletevalue

;###############################################################################
; Run
;###############################################################################

[Run]

Filename: "{app}\HobbySpark.exe"; \
    Description: "Launch HobbySpark"; \
    Flags: nowait postinstall skipifsilent

;###############################################################################
; Uninstall
;###############################################################################

[UninstallRun]

Filename: "cmd.exe"; \
    Parameters: "/C arduino-cli cache clean"; \
    Flags: runhidden skipifdoesntexist

[UninstallDelete]

Type: filesandordirs; \
    Name: "{app}"

;###############################################################################
; Install Delete
;###############################################################################

[InstallDelete]

Type: files; Name: "{tmp}\python.exe"
Type: files; Name: "{tmp}\arduino-cli.msi"

;###############################################################################
; Finished
;###############################################################################

