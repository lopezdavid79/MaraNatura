!include "LogicLib.nsh"
!include "MUI2.nsh"

Name "MaraNatura v1.0.1"
OutFile "MaraNatura-v1.0.1-Instalador.exe"
InstallDir "$PROGRAMFILES\MaraNatura"
InstallDirRegKey HKCU "Software\MaraNatura" ""

!define MUI_ABORTWARNING

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_LANGUAGE "Spanish"

Section "Instalar"
    SetOutPath "$INSTDIR"

    ; Incluye todos los archivos y carpetas dentro de la carpeta principal MaraNatura
    File /r "*"

    ; Crea los accesos directos
    CreateDirectory "$SMPROGRAMS\MaraNatura"
    CreateShortCut "$SMPROGRAMS\MaraNatura\MaraNatura.lnk" "$INSTDIR\MaraNatura.exe"
    CreateShortCut "$DESKTOP\MaraNatura.lnk" "$INSTDIR\MaraNatura.exe"

    ; Escribe la ruta de instalación en el registro
    WriteRegStr HKCU "Software\MaraNatura" "Install_Dir" "$INSTDIR"
SectionEnd

Function .onInit
FunctionEnd