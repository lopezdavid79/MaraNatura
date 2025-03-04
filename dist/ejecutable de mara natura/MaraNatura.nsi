!include "LogicLib.nsh"
!include "MUI2.nsh"

Name "MaraNatura v1.0.0"
OutFile "MaraNatura-Instalador.exe"
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

    ; Incluye el ejecutable principal
    File "MaraNatura.exe"

    ; Incluye la carpeta "data" y su contenido
    File /r "data\*.*"

    ; Incluye la carpeta "Sounds" y su contenido
    File /r "Sounds\*.*"

    ; Incluye otros archivos y carpetas necesarios (reemplaza con los nombres reales)
    File "otro_archivo.txt"
    File /r "otra_carpeta\*.*"

    ; Crea los accesos directos
    CreateDirectory "$SMPROGRAMS\MaraNatura"
    CreateShortCut "$SMPROGRAMS\MaraNatura\MaraNatura.lnk" "$INSTDIR\MaraNatura.exe"
    CreateShortCut "$DESKTOP\MaraNatura.lnk" "$INSTDIR\MaraNatura.exe"

    ; Escribe la ruta de instalación en el registro
    WriteRegStr HKCU "Software\MaraNatura" "Install_Dir" "$INSTDIR"
SectionEnd

Function .onInit
FunctionEnd