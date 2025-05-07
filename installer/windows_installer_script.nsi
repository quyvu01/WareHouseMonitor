; Script cài đặt NSIS cho Warehouse Temperature Monitor
; Sử dụng với NSIS (Nullsoft Scriptable Install System)

; Định nghĩa tên ứng dụng và phiên bản
!define APPNAME "Warehouse Temperature Monitor"
!define COMPANYNAME "Warehouse Solutions"
!define DESCRIPTION "Hệ thống giám sát nhiệt độ kho hàng"
!define VERSIONMAJOR 1
!define VERSIONMINOR 0
!define VERSIONBUILD 0

; Tên file cài đặt
OutFile "WarehouseTemperatureMonitor_Setup.exe"

; Thư mục cài đặt mặc định
InstallDir "$PROGRAMFILES\${APPNAME}"

; Yêu cầu quyền quản trị viên
RequestExecutionLevel admin

; Giao diện cài đặt
!include "MUI2.nsh"
!define MUI_ABORTWARNING
!define MUI_ICON "..\generated-icon.png"

; Các trang cài đặt
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "..\LICENSE.txt"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

; Ngôn ngữ
!insertmacro MUI_LANGUAGE "English"

Name "${APPNAME}"
Icon "..\generated-icon.png"
OutFile "WarehouseTemperatureMonitor_Setup.exe"

Section "Cài đặt" SecInstall
  SetOutPath "$INSTDIR"
  
  ; Các file của ứng dụng
  File "..\dist\WarehouseTemperatureMonitor.exe"
  File "..\dist\warehouse_temperature.db"
  File "..\dist\README.txt"
  
  ; Tạo shortcut trên Desktop
  CreateShortCut "$DESKTOP\${APPNAME}.lnk" "$INSTDIR\WarehouseTemperatureMonitor.exe"
  
  ; Tạo shortcut trong menu Start
  CreateDirectory "$SMPROGRAMS\${APPNAME}"
  CreateShortCut "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk" "$INSTDIR\WarehouseTemperatureMonitor.exe"
  CreateShortCut "$SMPROGRAMS\${APPNAME}\Uninstall.lnk" "$INSTDIR\uninstall.exe"
  
  ; Tạo uninstaller
  WriteUninstaller "$INSTDIR\uninstall.exe"
  
  ; Thông tin trong Control Panel
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayName" "${APPNAME}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "UninstallString" "$INSTDIR\uninstall.exe"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayIcon" "$INSTDIR\WarehouseTemperatureMonitor.exe,0"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "Publisher" "${COMPANYNAME}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayVersion" "${VERSIONMAJOR}.${VERSIONMINOR}.${VERSIONBUILD}"
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "VersionMajor" ${VERSIONMAJOR}
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "VersionMinor" ${VERSIONMINOR}
SectionEnd

; Uninstaller
Section "Uninstall"
  ; Xóa file ứng dụng
  Delete "$INSTDIR\WarehouseTemperatureMonitor.exe"
  Delete "$INSTDIR\warehouse_temperature.db"
  Delete "$INSTDIR\README.txt"
  Delete "$INSTDIR\uninstall.exe"
  
  ; Xóa shortcut
  Delete "$DESKTOP\${APPNAME}.lnk"
  Delete "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk"
  Delete "$SMPROGRAMS\${APPNAME}\Uninstall.lnk"
  RMDir "$SMPROGRAMS\${APPNAME}"
  
  ; Xóa thư mục cài đặt
  RMDir "$INSTDIR"
  
  ; Xóa registry
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}"
SectionEnd