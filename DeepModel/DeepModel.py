# -*- coding: utf-8 -*-

import os, random, base64, re, joblib, string
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'
import tensorflow as tf
from tensorflow.keras.layers import Dense, Embedding, Flatten, Input, Concatenate, Add, Subtract, Lambda, Multiply, Dropout, Activation, Reshape, BatchNormalization, LSTM, RepeatVector, Bidirectional, Conv1D, PReLU, MaxPooling1D, GlobalMaxPooling1D, SpatialDropout1D
from tensorflow.keras.models import Sequential, Model
import numpy  as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from tqdm import tqdm
from copy import copy

MAX_TOKEN = 260
NOP = 256
PAD = 257
BOS = 258
EOS = 259
EMB_DIM = 32
HIDDEN_DIM = 64
MAX_LEN = 300
MAX_SEQ_LEN = 18432

def char2int(item):
    values = []
    for char in item:
        values.append(ord(char))
    return values


def make_decoder_dataset(data):
    def make_label(y):
        debugger_1 = ['dnSpy', 'ida', 'x32dbg', 'x64dbg', 'frida', 'GDA', 'ProcessHacker', 'UltraEdit', 'WinHex', '010Editor', 'WsockExpert', 'ResEdit', 'DynamoRIO', 'WinDbg', 'apimonitor', 'Windbg', 'IDA', 'Charles', 'ProcDump', 'DebugDiag']
        debugger_2 = ['.i64', '.i32', 'ollydbg', '.dd32', '.dd64', 'die.exe', 'dumpcap.exe', 'pchunter', 'xuetr', 'ollyice','peid','sysinternals','lordpe','reflexil','confuseEx','androidkiller','apktoolbox','dex2jar','jd-gui','antispy','powertool','gmer','hash','cheat','ntsd','nanomite','compdisasm','beyond','registryworkshop','httpspy','fiddler','minisniffer','packassist','wireshark','scylla','studype','pestudio','keymake','baymax', 'windbg.exe']
        developper_1 = ['Visual Studio', 'Java Dev', 'Wireshark', 'javac', 'clang', 'ssh', 'MSBuild', 'ipython', 'git', 'nginx', 'Anaconda', 'ServiceHub.', 'VMware', 'vbox', 'Blend for', 'Notepad++', 'Python ', 'RealVNC', 'Sublime Text', 'TortoiseSVN', 'Xshell', 'mingw-w64']
        developper_2 = ['CMake', 'Cygwin', 'Code.exe', 'adb.exe', 'cmake-gui.exe', 'python.exe', 'vmnat.exe', 'wsl.exe', 'cpptools.exe', 'node.exe', 'JetBrains', 'sdk platform-tools', '.vim', '.pyc']

        candidate_debugger, candidate_developper = [], []
        debugger_1_count, debugger_2_count, developper_1_count, developper_2_count = 0, 0, 0, 0
        for j in set(y):
            for k in debugger_1:
                if j.startswith(k):
                    debugger_1_count += 1
                    candidate_debugger.append(j)
            if j in debugger_2:
                debugger_2_count += 1
                candidate_debugger.append(j)
            for k in developper_1:
                if j.startswith(k):
                    developper_1_count += 1
                    candidate_developper.append(j)
            if j in developper_2:
                developper_2_count += 1
                candidate_developper.append(j)
        #print(candidate_debugger)
        #print(candidate_developper)
        if debugger_1_count > 0 and debugger_2_count > 0:
            return 1
        if developper_1_count > 1 and developper_2_count > 1:
            return 2
        return 0

    def parse_data(data):
        data = re.split("[;\\\\]", data.encode('ascii',errors='ignore').decode())
        data = set([i[:16] for i in data])
        return list(data)
    X = parse_data(data)
    y = make_label(X)
    return X, y

def generate_data():
    def get_base_input():
        return ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'feature.txt', 'todo.txt', 'crack.txt', 'micaut', '.SBV', 'EventSystem', 'StaticDi', '.qcel', 'MessageV', 'WebEnrlS', 'MSExtPri', 'WcsPlugI', 'certocm', '.ipr', 'mspdbsrv.exe', 'Outlook', '.uxdc', '.F4V', 'wercplsupport', 'OfficeCo', 'SearchIndexer.exe', 'ExcelWor', '8.1', 'RAServer', 'QPCore', 'local', 'MessagingService', 'Cellular', '.crw', '.oc_', 'QingCloud Guest Agent', '.publ', 'Total Commander x64.lnk', '.ppsx', 'TXFTNAct', 'WindowsL', 'CDPUserSvc', 'cphs', 'UdkUserSvc_b7008', 'VMware Workstation', 'WMP', 'SettingC', 'cct', '.onep', 'NetworkC', '.icl', '.mak', '.eps', 'SyncEngi', 'SpeechUX', 'Wireshark.exe', '.gcsx', 'FaxComEx', 'ie_to_ed', 'W32Time', 'NgcProCs', 'WECAPI5', '.vste', 'VsWizard', 'javapath', 'DevicesFlowUserSvc_2490547b', 'MSDADC', '.jav', 'WSMan', 'odtfile', '.giti', 'certadm', 'xslfile', 'audiodg.exe', 'PNGFilte', 'bthserv', 'cdmpfile', 'GitWCRev', 'NcbService', 'AppMgmt', 'Publishe', 'Graphviz', '.ashx', 'SVCID', 'TXPlatfo', '.desk', '.msc', '.SUB', 'Icad', '.TS', 'vmware-authd.exe', 'NbTextLa', 'Property', 'desktop.ini', 'LayoutRe', '.386', 'svn+ssh', 'Program Files (x86)', '.easm', 'LicenseManager', '.vmt', 'bin64', '.qrc', 'Visio', 'ADSystem', '.WMZ', '.cab', '.poth', 'MSInfoFi', '.sldx', 'PeerDraw', 'AppVClient', 'JavaWebS', 'Faultrep', 'RDSProfi', 'WwanSvc', 'np_tdiep', '.cs', '.k25', '.sequ', 'Scripts', 'Launcher', 'ODCfile', '.h', '.pubx', 'MSDAER', 'JNLPFile', '.pkgd', '.c', 'Assigned', 'WMLSS', '.mos', '.rat', 'migfile', 'xmlfile', '.appx', 'MSStorag', 'chkfile', 'pla', '.sdl', 'Dnvm', 'SgrmBroker.exe', 'desktopt', '.edmx', '.xz', 'CoordService.exe', 'windows', '.maw', '.zst', '.ova', 'Anaconda3 (64-bit)', '.clas', 'SPPUI', 'NaturalAuthentication', 'ContentD', '.prc', 'SyncRibb', 'TSVNCache.exe', 'QQPCExternal.exe', 'InputPro', '.htc', '.mani', 'WManSvc', 'GPCSEWra', 'CallIGCC', 'VMwareHostd', 'JobObjSe', 'WINWORD.EXE', 'RemoteDe', '.dbg', 'Wbem', 'ECMAScri', 'DcomLaunch', 'MSDDS', 'FileManager.lnk', 'OpenSear', '.hdmp', '.tac', 'STSUpld', '.WTV', '.them', 'MicrosoftEdge.exe', '.vsse', '.acl', 'batfile', 'CryptSvc', '.aps', '.spc', 'WindowsI', '.hxf', '.qmc6', 'defragsvc', '.dotm', '.mht', '.xht', 'VBS', 'potrun', 'DRM', '.mag', '.udt', '.hxh', 'BDATuner', 'MapiCvt', '.dsw', 'MSOLAPUI', '.hxr', '.osdx', '.vwr', 'VMwareHo', 'Cmiv2', 'imesxfil', 'WMPlayer', 'nsi', 'wwauth3r', 'CSSfile', '.SUP', '.vst', 'DOCSITE', 'anifile', '.cdmp', 'ActiveSy', 'ScanProf', 'FontCache3.0.0.0', '.fif', 'APPLICAT', 'wpa', 'lmhosts', '.api', 'vcard_wa', 'PdfDisti', '.cdx', 'AarSvc_418a97f', 'ProfSvc', 'Mts', '.vssx', 'MMCCtrl', 'Oracle', '.dmp', 'NisSrv.exe', 'DialogBlockingService', '.rc', '.sor', 'WUDFHost.exe', 'RecentDo', 'StdFont', '.tab', 'Smart', 'URLRedir', 'MailMsgA', 'MSDMine', 'fonfile', '.nett', 'CCXProcess.exe', 'AppReadiness', 'vm', '.bcp', 'igfxCUIService.exe', 'MTSAdmin', 'zapfile', '.ghi', '.pcb', 'msinkdiv', '.ace', '.ipp', 'OneNoteD', 'GoogleUp', 'vxdfile', 'CaptureService_2490547b', '.nk2', 'QQPCRTP', 'DNWithSt', '.vob', 'Tsmmc', '.mtx', 'oms', '.icc', 'ServiceHub.DataWarehouseHost.exe', '.zoo', 'IGCCTray.exe', 'acrotray.exe', '.vbht', 'DxDiag', '.bh', '.xsc', '.idb', 'BdeUISrv', 'IMAPI', 'Portable', 'zsh', 'Software', '.dng', 'UserDataSvc_2490547b', '.cur', '.p10', 'SecProvi', 'ScriptCo', '.pl', 'RSoPProv', 'wcxfile', 'Google Chrome.lnk', 'usysdiag.exe', 'edgeupdatem', 'CloudSyn', '.lzh', '.xix', 'hlpfile', 'svn', 'LogonUI.exe', '.idq', '.coff', 'msiserver', '.tsp', 'ssh-agent.exe', 'Memory Compression', 'Name', '.kci', '.ics', 'IntelliJ', 'Binn', '.sr2', '.mts', 'HRShell', '.jnlp', 'ssh-agent', 'IMESingl', '.heif', 'CorSymBi', '.m4p', '.jtx', 'VPNv2', '.CUE', 'PimIndexMaintenanceSvc_2490547b', 'VaultSvc', 'TimeBrokerSvc', '.vsdx', 'EFS', '.vdw', 'CredentialEnrollmentManagerUserSvc', '.au', 'drvfile', '.mhtm', '.pef', 'tgit', 'OneSyncSvc_418a97f', 'pbkfile', 'ListPad', 'ImeKeyEv', 'MSAddnDr', '.pptm', 'CTEX', '.qmc0', '.xltm', 'EntityDa', 'dqyfile', '.psha', '.sqlp', 'backgroundTaskHost.exe', '.razo', '.swf', 'SavedDsQ', '.qmc4', 'http', 'system32', '.mk3d', 'MsRDP', 'RtkAudUService64.exe', 'Media', 'MMCListP', 'DesktopB', 'CAJSHost.exe', 'MSP', 'git', '.cpp', 'MSSearch', '.tsv', '.docm', 'wmafile', 'GraphicsPerfSvc', 'rlefile', 'ty', 'TrustedInstaller', '.odcn', 'BOOTSTRA', 'WBEMComL', 'jnlps', 'XEV', 'ELeadPro', 'RDS', 'VSWFFlav', 'UserData', 'WeTERMService.exe', 'Te.Service', 'rtmp', 'VMware NAT Service', '.site', 'auphd', '.mlc', '.IDX', '.USF', '.mda', 'LiveScri', 'YoudaoDict.exe', 'lvr', 'NetTcpPortSharing', '.ppa', 'OneNote', 'LanmanWorkstation', 'UevAgentService', 'Psisdecd', 'TvRating', 'stisvc', 'Communic', 'tzautoupdate', 'Office', 'wisvc', 'oqyfile', '.in_', 'Director', 'feeds', 'Winmgmt', 'IMOfferR', 'GC', '.rtf', '.dotx', 'Acrobat', 'Dispatch', '.xlt', 'aipai', 'MimeDir', '.M2V', '.odcc', '.pwz', 'Research', 'ScriptedSandbox64.exe', 'QQPCTxtExt.exe', 'diagnosticshub.standardcollector.service', 'Totalcmd64.exe', 'OpenSSH', '.ipfi', 'SDSHELLE', 'emffile', 'vmictimesync', '.xlsh', 'NetworkE', '.raf', 'Microsoft.VsHub.Server.HttpHost.exe', 'sacsvr', 'blnsvr.exe', '.vim', 'VC', 'cpptools.exe', '.caa', 'HTML', 'HyperV', 'ShapeCol', '.snk', '.dsh', '.filt', 'tbauth', 'COMAdmin', 'ADsDSOOb', 'SSDPSRV', '.emf', '.wbca', 'launchre', '.psc1', '.TPR', '.mp4v', 'QQShellE', 'WindowsPowerShell', '.fdc', 'CRichPic', 'KtmRm', '130', '.SND', '.dsn', 'CodeSetup-stable-7f6ab5485bbc008386c4386d08766667e155244e.tmp', 'wordmhtm', 'HHCtrl', '.pyc', 'WMVFile', 'DusmSvc', 'WbioSrvc', 'WarpJITSvc', '.odt', 'CABFolde', 'v1.0', 'taskhostex.exe', '.M3U', 'WMISnapi', '.xts', '.dct', 'ultra compare.lnk', '.htx', 'WMPTheme', 'KIPX', 'IntelCpHeciSvc.exe', 'Xtranspo', 'MediaFou', 'RemoteAs', 'msstyles', 'RequestM', '.acce', '.sap', '.vsx', 'VideoRen', 'cmd.exe', 'KeyIso', 'powershell.exe', '.wmz', '.dic', '.txz', 'CRichOle', 'WindowsD', 'XblGameSave', 'cbdhsvc_2490547b', '.odct', '.tr1', 'Modules', '.psh', 'RstMwService', '.blg', 'P7RFile', '.dff', '.ccx', '.m4b', 'SystemSe', 'DBRSTPRX', 'sqlwriter.exe', '.dbml', '.mig', 'ttcfile', 'ProcessD', 'U-2.0.lnk', 'PimIndexMaintenanceSvc', 'CloudBac', 'HipsDaemon', 'TieringEngineService', '.syml', '.mdw', 'TokenBroker', 'ms', 'notepad.exe', 'AllSyncR', '.mdt', 'inffile', '.vtx', 'OneCoreC', 'FNPLicensingService.exe', '.ZFSe', '.gdl', 'MSScript', 'OneApp', 'HtmlDlgS', '.snoo', 'Everything.exe', 'YoudaoWSH.exe', '.TTML', 'tortoise', 'JRO', 'statemod', '.vstm', '.mde', '.appr', '.pyo', '.trx', 'Security', '.TOM', 'vmicheartbeat', 'Microsoft.Photos.exe', '.resw', 'IImeIPoi', 'JavaScri', 'https', 'stssync', 'AboveLoc', 'CDPUserSvc_b7008', 'dllhost.exe', '.webm', 'PrintWorkflowUserSvc', 'IDBHO', '.nst', 'iOA', 'Provisio', 'webcals', 'JScript', 'ConsentUxUserSvc', '.cpl', 'SearchUI.exe', 'MSDASQL', 'WalletService', 'SQLfile', '.ilk', '.mmf', '.plg', 'Control', 'NbDocVie', '.K3G', '.pbk', 'ADsSecur', '.ASS', 'Spp', '.dtx', 'Download', 'OneNote.lnk', '.avif', '.hsh', '.xevg', 'Conflict', 'NbDocCst', 'LxpSvc', 'XLServicePlatform', '.php3', '.SMI', 'VSMGMT', 'YunDetectService.exe', 'odcdatab', '.qpak', '.tt', 'p2pimsvc', '.odl', 'AccessCo', 'DevicePickerUserSvc_b7008', 'RDSServe', 'WScript', '.adp', 'Scriptle', '.rll', '.jar', '.ods', '.sbr', '.adn', 'DataCollector.exe', 'JSEFile', 'OutlSMTP', 'igfxCUIService2.0.0.0', 'Rdpvcoma', '.msst', '.xltx', '.ps1x', 'Package', 'mtrs', 'P7SFile', 'SSPWorks', '.devi', '.M1A', 'Behavior', 'ImeLmTes', 'InkObjCo', 'lnkfile', 'BFE', 'LibraryF', 'new', 'MIDFile', 'SrContro', 'NetworkP', '.py', 'VacSvc', 'LDAP', 'SSCProt', 'DevicesFlowUserSvc', 'ServiceHub.ThreadedWaitDialog.exe', 'Desktop.lnk', '.prin', '.vspr', 'StdPictu', 'PdfFile', 'pfmfile', 'SppComAp', 'ratfile', 'Adobe', 'diagsvc', '.scc', 'RCM', 'browser_broker.exe', 'ndfapi', '.p7b', 'WFDSConMgrSvc', 'PresentationFontCache.exe', '.svg', '.vss', 'AccClien', 'WeTERM.exe', 'FormHost', 'RowsetHe', 'WeDrive', 'rundll32.exe', 'VMAuthdService', 'MSDASQLE', 'NetServe', 'OrgPlusW', 'CLRMetaD', '.txt', 'cmake-gui.exe', 'DoSvc', '.ttf', '.rf5', '.ps1', '.cat', 'acrobat', 'LayoutFo', '.vsp', 'TextInpu', 'Tablet PC', '.RCV', 'Netlogon', 'PhoneSvc', '.dll', 'FodHelpe', 'ddsfile', '.aifc', 'EMAIL2', '.sy_', 'wininit.exe', 'SecureAs', '-yuteng&felixbo.txt', 'CodeSetup-stable-7f6ab5485bbc008386c4386d08766667e155244e.exe', 'Msshed', '.cd', '.scp', 'DeviceDi', '.dbs', 'Microsoft Office ', 'TipAutoC', '.inc', 'CDO', '.tts', 'SQLOLEDB', 'curfile', 'BuildService.exe', '.cmd', 'Adobe Acrobat Distiller DC.lnk', '.xdp', '.vsps', 'iFt.lnk', '.stvp', '.wmp', '10', '.ogg', '.hdp', 'CfgComp', 'smss.exe', 'Applicat', '.xsl', 'smphost', '.asax', 'otffile', 'SNMPTRAP', 'bash.exe', 'chm', 'CaptureService', 'DMAcc', '.wlt', '.qmcf', '.mydo', '.rc2', 'Windows', 'WlanSvc', 'MessagingService_b7008', '.vsto', 'DMClient', 'soap', '.RAM', '.wpz', '.dsgl', 'MOFL', 'Windows Store.lnk', '.csh', 'DocWrap', 'RACplDlg', 'ExcelCha', 'cnki', 'RoamingS', 'WOW6432N', 'YoudaoGe', 'Wired', 'GSview', 'SPPWMI', '.mode', '.hxv', 'Code.exe', 'DevicePickerUserSvc', '.MIDI', 'QQPhotoD', 'DXImageT', '.load', '.m1v', '.libr', 'SmsRouter', '*', 'SEMgrSvc', 'QMContex', 'zjf', '.asc', 'wbengine', '.ADT', '.out', '.Job', '.ori', 'service4', 'LR', 'MSHelp', 'wsqmcons.exe', 'Passport', 'BrowserB', 'tools', '.xsd', 'TextInputHost.exe', '.asf', '.res', '.sst', '.asa', 'ERCLuaEl', '.sed', '.MXF', 'AcroSend', 'Vim', 'Uev', 'jarfile', '.qmb', '.vmsd', 'DefaultL', 'potplaye', 'NameTran', '.pyw', '.wma', '.mar', 'prffile', 'Outlook.lnk', 'AdobeUpdateService', 'COMEXPS', 'BTAGService', 'PyCharm Community Edition 2021.2', 'SirepCli', 'TimwpDll', 'AllProto', 'Wordpad', 'VsHub.exe', 'Registry', 'Blend for Visual Studio 2015.lnk', '.inl', '.scr', 'Professional', 'comfile', 'MsoTDAdd', 'ClipSVC', '.MPL', '.uvu', 'sdchange', 'rlogin', '.wax', 'VSPerfCo', 'accessht', '.chs', '.cc', 'CAJVChec', '.cdxm', '.snd', 'svgfile', 'VSWinExp', 'RemoteHe', 'kali.exe', 'WEPHOSTSVC', 'webcal', 'unified_', 'Msxml', '.sr_', 'Totalcmd64.lnk', '.WK3', '.rct', 'PyCharm Community Edition 2020.3.3', 'icmfile', 'vpnagent', 'MSILink', 'COMSNAP', 'PEID V0.95.EXE', 'WerSvc', '.vcxi', 'SDENGINE', 'GuestAgent.exe', '.netp', 'Microsoft Visual Studio 2012', '.bin', '.mpeg', 'Enterpri', '.sty', '.hlsl', '.lvr', 'AdobePDF', 'SSOLUICo', 'MSTSWebP', '.iqy', 'AGMService.exe', 'ShellExperienceHost.exe', '.ans', 'RtkAudioUniversalService', '.dwfx', '.hxi', 'mintty.exe', 'InstallService', 'PotPlaye', 'PTRegTer', '.json', 'WlanAdho', 'DebugSam', 'vmtoolsd.exe', '.DTSH', 'RpcEptMapper', '.mad', '.srf', 'PocketOu', 'NcdAutoSetup', 'ImeCommo', '.tb7', '.camp', 'Drive', 'PenIMC4v', '.exc', 'IKEEXT', 'UnistoreSvc_b7008', 'WiaDevMg', 'MSDTC', 'CImeComm', 'Microsoft Edge.lnk', 'iexplore.exe', '.001', 'BrokerInfrastructure', 'Adobe Acrobat DC.lnk', 'SearchCo', 'Macromed', 'AdobeARMservice', 'themefil', '.drf', '.mfla', 'EventSys', 'AADJ', '.jbf', 'CTREEVIE', '.nh', '.faq', '.wpl', 'LSM', 'FlashUtil_ActiveX.exe', 'Users', '.dotnet', '.wmf', '.hsha', '.targ', '.TAK', '.fdf', 'Catsrv', 'WindowsB', '.otm', '2019', '.one', 'hns', '.UDL', 'ScDeviceEnum', 'Accounts', 'QQPCRTP.exe', '.csha', '.tm4', '.xlm', '.TTS', 'HotSpot', '.MPEG', 'EapMscha', 'ChsIME.exe', 'UXDCFILE', 'DevQueryBroker', 'OutlPOPP', 'DevicesFlowUserSvc_418a97f', 'Scripted', '.lacc', '.data', 'OneDrive.exe', '.m4v', 'LibraryL', '.mk', 'ConsoleP', 'JNTFilte', 'notepad++.exe', '.mpg', 'iFLYMouse.exe', 'CorSymWr', '.m3u', '.js', 'CAJViewe', 'Windows TShell', '.sln', 'FaxTiff', 'DeviceAssociationService', 'Microsoft SQL Server', '.mid', 'Administrative Tools', 'MsKeyboardFilter', 'W7TODMSC', '.less', 'PFXFile', '.mast', 'PimIndexMaintenanceSvc_418a97f', 'mk', '.movi', '.wdp', 'CCWU', 'MSiSCSI', '.conf', 'AppData', '.ADTS', 'Interfac', '.URL', '.sc2', 'WinNTSys', 'cmd', '.RT', '.xlth', 'c:', '.laye', 'tsvncmd', 'Certific', 'vmnat.exe', 'MediaDev', 'gupdatem', 'HRSword.lnk', 'RuntimeBroker.exe', 'edgeupdate', 'AUFile', 'PDFMOutl', 'MAPI', 'StaticMe', 'Accessibility', 'Excel.lnk', 'usr', 'vmicshutdown', 'MSFSStor', 'UnistoreSvc_2490547b', 'Microsoft VS Code', '.hol', '.vsz', 'MsRdpWeb', 'EventLog', 'StartUp', 'MessagingService_418a97f', '.sit', 'DmEnrollmentSvc', 'zynamics BinDiff 4.2', '.vdx', '.jobo', '.user', '.test', 'ADOX', '.p7m', 'npQMExte', 'WpnService', 'GDA3.96.exe', 'XML', 'ServiceHub.Host.CLR.x86.exe', '.cspr', 'WindowsS', 'Anaconda3', '.elm', 'AcroExch', '.DTS', '.AddI', 'Policy', '.webt', '.odh', 'CertPropSvc', 'RasMan', 'python.exe', 'regedit.exe', 'WpnUserService', '.docx', 'ProgramData', 'DirContr', '.sys', 'workfolderssvc', 'Daum', '.wiz', '.ptx', 'Schedule', 'Visual Studio Code.lnk', 'insight3', '.wiq', 'WXWorkWeb.exe', '.APE', '.ms-w', 'Msi', 'CoreMessagingRegistrar', 'IMAPI2FS', 'RmSvc', '.NSV', 'lsass.exe', 'ApplicationFrameHost.exe', 'MusicSea', 'vmcompute', '.xpro', 'Word.lnk', 'ADOR', 'ConsentUxUserSvc_b7008', 'SkyDrive', 'Spooler', 'hexin', '.3g2', '.wxml', 'devenv.exe', 'LanmanServer', '.p12', 'Programs', 'Tim', 'iOANetTool.exe', '.IVF', 'Llvm', 'RdpCoreT', 'Baiduyun', 'sh_auto_', 'UmOutloo', '.gitm', '.asm', '.s', 'AGSService.exe', 'htmlfile', '.jtp', '.pps', 'PrintWorkflowUserSvc_418a97f', 'ShellNam', 'CorTrans', 'NTSTATUS codes.lnk', 'SCPolicySvc', 'COMSVCS', '.M3U8', '.bay', 'IncrediBuild_Coordinator', 'service', 'StartMenuExperienceHost.exe', '.mgep', 'MySQL', 'WiFi', 'SstpSvc', '.br', '.exp', 'P7MFile', 'AdobeNotificationClient.exe', 'lltdsvc', 'AcrobatP', 'STClient', '.bz', '.wmdb', 'DXTransf', 'PowerPoi', 'Rdpcomap', 'MSASR', 'PDFPrevH', '.tiff', '.mfcr', 'ImeBroke', 'OpenConsole.exe', '.xlxm', 'PcaSvc', '.asx', 'WMP11', 'MSSQL', 'CscService', '.PSB', 'UALSVC', '.map', '.pic', 'igccservice', 'FDResPub', 'ScriptBr', 'RealVNC', '.pif', '.mau', '.dqy', '.scf', 'Taskmgr.exe', 'pjpegfil', 'csig', 'YoudaoDictHelper.exe', 'ADsNames', '.cda', 'MSBuild.exe', '.vmpl', 'AzRoles', 'aspfile', 'VCBSnaps', 'AcroPDF', 'Xshell 6', 'PyCharmC', 'RotMgr', '.ogv', 'Java Development Kit', '.hxd', '.lst', '.xml', 'regfile', 'Location', 'VsGraphi', 'License', 'WindowsApps', 'PhotosAp', '.gene', 'CM_Cellu', '.vsss', 'iaStorAfsService', 'SensorService', '.TTA', 'ServiceHub.TestWindowStoreHost.exe', '.5vw', 'BaiduNetdiskUtility', '.WV', 'FSLoader', 'x64dbg.lnk', '.ofs', 'AppID', '.ovf', 'FrameServer', '.xlw', '.NSR', '.rpc', '.thmx', '.scss', 'vmicvss', 'WdiServiceHost', 'Undecide', '.ogm', '.maq', 'qmgcfile', '.pal', 'wdpfile', 'IDA Pro', '.jpg', 'PDFMVisi', '.cnt', '.DPL', '.msi', 'dumpcap.exe', 'GIFFilte', 'AudioVBS', 'OfficeTh', 'MCSF', 'MPlayer', 'SSCE', 'UsoSvc', 'nvagent', '.xld', 'lfsvc', 'VMware', '.dd64', 'VUPlayli', '.raw', '.dvi', '.igp', '.wizh', '.acti', 'iOABoot', 'dwm.exe', '.vmxf', 'PCBFile', 'campfile', '.heic', '.jnt', 'LargeInt', 'AJRouter', 'QueryWin', 'jnlp', 'Forms', '.wvx', 'Internet', 'FaxContr', '.VBE', '.mplo', 'MicrosoftEdgeCP.exe', '.adts', '.ini', 'Frequent', 'windbgx64_local.lnk', 'pnffile', 'Journal', '.mdmp', 'netprofm', '.aaui', 'Visual Studio 2015', 'com', 'iOAGuard.exe', 'SelectPa', '.WMD', 'Python 2.7', 'DsSvc', '.gra', 'Ghostscript', 'WINDOWS', 'WeChatApp.exe', 'WeMail.exe', 'IntelCpH', '.idl', '.WAX', '.i64', '.vcw', 'WpnUserService_418a97f', 'Msrtedit', 'ChromeHT', 'TrkWks', '.wcx', 'Trident', 'wemeet', 'DllHostI', '.LMP4', 'RpcLocator', 'PROTOCOL', '.ib_l', 'QQPYBrok', 'MSExtLoc', 'cmdline-tools', '.weba', 'DevicePickerUserSvc_2490547b', 'dasHost.exe', 'vm3dservice.exe', 'bootstra', 'tsuserex', '.gsha', 'AcroAcce', 'Network', 'vmnetdhcp.exe', 'System32', 'ELMFile', '.ani', 'search', '.fnt', 'Windows Performance Toolkit', 'ADOMD', 'AdobeCollabSync.exe', 'OWS', 'BaiduYun', 'OLETrans', 'WpcMonSvc', '.crtx', 'Wcmsvc', 'XblAuthManager', 'SearchApp.exe', '.ibq', 'MSOLAP', 'UserLibr', 'UnistoreSvc_418a97f', '.mpv2', 'Microsoft Silverlight 5 SDK - ()', 'Microsoft Visual Studio', '.chm', 'spectrum', '.MP2V', 'vms', 'PlayToRe', 'PerfFile', 'miktex', '.xfdf', '.pdf', '.wmx', '.cr3', 'BarCodeP', 'OLE', '.mpe', 'Source Insight 3', 'iOAGuard', 'UdkUserSvc', 'ShellHWDetection', 'mtm', 'IntelCpHDCPSvc.exe', 'WMSDKHTT', 'Git', 'SharedRealitySvc', 'UnifiedW', '.jpeg', 'csc', '.pyd', 'SearchFilterHost.exe', 'Windows Kits', 'Dhcp', 'Microsoft.Alm.Shared.Remoting.RemoteContainer.dll', 'QQPYSkin', 'SmartVPN.exe', '.EAC3', 'swprv', 'sppsvc', 'SSOAxCtr', '.xps', '120', 'COMSysApp', 'iOARtp', '.cove', 'vmware', 'QQPYSetu', '.vmba', 'RetailDemo', '.wm', '.ib_m', '.midi', '.pklg', 'mp3file', 'Vim 8.2', 'caffeine32.exe', 'Acrobat.exe', 'powerpoi', '.hif', '.orf', 'SharePoi', 'PushToInstall', 'odc', 'AarSvc_b7008', 'AutoProx', '.sql', '.wtx', 'svsvc', 'jusched.exe', 'NlaSvc', '.ppsm', '.acp', '.dsha', 'IE', 'JobObjIO', 'XboxNetApiSvc', 'appdata', '.ppt', '.eyb', 'DispBrokerDesktopSvc', 'GoogleChromeElevationService', '.glox', 'objref', 'mapi16', 'icssvc', 'exefile', 'MSEdgeMH', '.tbz2', 'ADs', '.xaml', 'insight', 'xhtmlfil', '.MPG', '.lnk', '.AMV', '.apc', '.html', 'MSComctl', 'Tools', '.vmtm', 'GoogleCrashHandler64.exe', '.shtm', 'PLA', '.pkt', '.WK', 'SysWOW64', 'WinEdt', 'PenInput', '.cgm', '.disc', '.MP2', '.tlz', 'DeviceInstall', '.gif', 'Search', 'users', '.dcs', '.ogx', 'IDApro', 'Sense', '.aac', 'JobObjLi', '.sfca', '.tpc', 'excelmht', 'WIN8_PRO', '.hxq', '.cer', 'QzonePla', 'YourPhone.exe', 'TabletInputService', 'spoolsv.exe', '.pst', 'giffile', 'Search.lnk', '.adt', 'qmbsrv', 'Compress', '.wmv', '.evt', '.p7c', 'iphlpsvc', 'cbdhsvc_b7008', 'MIME', 'PowerPoint.lnk', 'UIProxy', 'vsls', '.kdh', 'DsmSvc', '.sett', '.mav', '.sym', '.dds', 'Elevated', 'SrDrvWuH', 'WinNT', 'Proxifier.lnk', '.aspx', 'TDCCtl', 'OfficeClickToRun.exe', '.iso', '.dat', '.wll', '.mp2', 'CDPUserSvc_418a97f', 'SecurityHealthService', 'vds', '.vcs', '.dcr', 'DeviceRe', 'SymBinde', 'ida.lnk', 'MiKTeX', 'Wireless', 'SAPI_One', 'IgfxExt', '.M2TS', 'RDP', 'PlugPlay', 'CTapiLua', 'TCSCConv', '.dd32', 'ierss', 'SearchProtocolHost.exe', 'Fsrm', 'X509Enro', 'LEXFile', 'config', '.etl', 'VNC', 'ServiceHub.SettingsHost.exe', '.ost', '.sct', 'DeviceUp', '.XOML', 'AAM', 'Previous', 'Template', 'AdHocRep', 'LicLua', 'WPDConte', 'PhotoVie', 'wireshar', 'CaptureService_b7008', 'FontCache', 'Windows Phone SDK 8.1', 'MSExtOrg', '.tod', 'idaq.exe', 'PerfWatson2.exe', 'FaxServe', 'ExcelPlu', 'Printers', '.vspf', 'DevicePickerUserSvc_418a97f', 'Connecte', 'DBROWPRX', '.msp', 'MsTscAx', 'MSRDC', '.pbf', 'sdk', '.bpdx', 'HWXInk', '.part', 'FHConfig', 'mtr', 'RDBFileP', 'DPS', 'KmSvc', 'LxssManager', '[System Process]', 'CRichDat', 'SoundRec', 'SUPL', 'IMAPI2', '.bkf', '.img', 'IconLibr', 'TGitCache.exe', 'Briefcas', '.wsc', 'IMECheck', 'AdobeUpdateService.exe', 'igfxEM.exe', 'conhost.exe', 'MSSppLic', '.vb', 'Python 3.6', '.vmsn', 'QQPet', 'qmbsrv.exe', 'DisplayEnhancementService', 'armsvc.exe', '.mdp', 'FBiblio', '.hxx', '.jfif', '.vxd', '.AIFC', 'DLNA', 'python36', 'NetSetupSvc', '.eml', '.TRP', '.snip', 'MSOrgCha', 'QQPCSoftMgr.exe', '.mat', '.com', 'MSIME', '.exe', '.jsx', '.ac3', 'TortoiseSVN', '.wbk', '.caf', 'WinInetC', '.htt', 'MSDAORA', '.MPC', 'DSRefObj', '.pmr', 'PeerFact', 'Results', 'wordhtml', '.bat', 'HtmlDlgH', 'HNetCfg', 'SQLNCLI1', 'bidispl', 'Sysmon', 'EapTlsCf', 'UmRdpService', '.secs', 'rtsp', '.aif', 'Airplane', '.opus', '.labe', '.aiff', 'x86-remote.lnk', 'gmmpfile', '.lz', 'JpnRanke', 'Blend', 'SDRSVC', 'mspaint.exe', 'sshd.exe', 'WMPNSSCI', '.wxpr', '.3gpp', '.hxt', '.tsx', 'DiagTrack', '.pma', 'Register', 'Notepad++.lnk', 'SensorDataService', 'PinnedFr', '.webp', '.bib', '.det', 'mscfile', '.rle', 'IpOverUsbSvc.exe', '.ASF', '.egg', '.vmss', 'StorSvc', '.fdm', '.potm', 'WGestures', 'QQProtect.exe', 'tsvn', 'Excel', '.lpcm', '.resm', 'dllfile', 'SyncMgrC', 'TxCTx', '.lgn', 'Wow6432N', 'CryptPKO', '.vhdp', '7-Zip', '.tif', 'NODEMGR', '.rgs', 'RemoteRegistry', '.prf', 'AcroBrok', 'seclogon', '.grp', '.vcpr', 'IMEPad', 'Snapins', 'adobe', 'SQLWriter', '.AIFF', 'HipsTray.exe', 'vmicrdv', 'WinInetB', 'scrfile', 'Scriptin', 'WmiPrvSE.exe', 'AdvMLThreatMatrix.jpg', 'U-2.0', 'TpcCom', 'CorSymRe', 'VSFileHa', 'DataCtl', '.vspx', 'WebClient', 'UPnP', 'BalloonService', 'DynamoRIO-Windows-8.0.0-1', 'Microsoft', '.CDA', 'SCardSvr', 'DfsShell', 'qedit', 'AcroCEF.exe', 'UserDataSvc', 'MiKTeX 2.9', 'MMC', '.oft', '.doch', 'WinRM', 'res', 'SamSs', 'Terminal', '.vhdx', 'tfs', 'VMUSBArbService', '.MPE', '.ts', '.xrm-', 'WAB', 'OneSyncSvc_b7008', 'smartscreen.exe', '.atc', 'YunWebDe', '.VTT', 'ctex', 'vim82', 'SensorsA', 'SDBACKUP', 'device', 'MSVidCtl', 'C:', 'VisioVie', 'certific', '.work', 'x', 'wcncsvc', '.etp', 'Shell', 'TXGYMail', 'cttunesv', 'IPROSetMonitor.exe', '.eprt', 'MSITStor', 'OVCtl', 'UserManager', '.msg', 'OPCFile', 'Packaged', '.dib', '.css', '.syc', 'CDPUserSvc_2490547b', '7', 'AdobeIPCBroker.exe', 'SgrmBroker', 'CaptureService_418a97f', 'DeviceAssociationBrokerSvc_b7008', '.ext', 'NCProv', 'Python36', '.evtx', 'init', 'VMnetDHCP', '.xlk', 'mraut', 'SysMain', 'Program Files', 'SyncMgrF', '.ico', 'Video.UI.exe', '.gqsx', 'VsaVbRT', 'wordxmlf', '.mfp', '.MID', '.iiq', '.diag', 'tapisrv', 'wscsvc', 'WMDMCESP', 'WinNTNam', '.wab', 'Windows Phone SDK 8.0', '.dctx', 'Visual Studio 2019', '.odc', '.vsmd', 'CDPSvc', '.hxw', '.hxa', '.pyz', '.nfo', 'GCSXFile', 'QQPCRealTimeSpeedup.exe', '.rmi', 'WPDSp', 'MapsBroker', '.ocx', 'WXDrive.exe', 'ASP', '.potx', 'WDExpres', 'MSPersis', 'Themes', '.shpr', 'Microsof', 'Microsoft DNX', '.m2ts', 'WinHttpAutoProxySvc', '.tm7', '.pfx', '.M2T', 'WINMGMTS', 'HomePage', 'VBEFile', 'AarSvc', 'upnphost', '.perf', 'QC', 'WPDBusEnum', 'Proxifier.exe', 'JSFile', 'AtWorkRe', 'MSExtUse', '.fbx', 'Classes', '.vhd', 'WordDocu', 'PDFMLotu', 'InkSeg', 'WIA', 'NgcSvc', 'sihost.exe', '.SRT', 'ITSProto', '.pdb', 'SysColor', 'accountp', 'WindowsInternal.ComposableShell.Experiences.TextInput.InputApp.exe', '.bas', '.3fr', '.m4a', '.webs', 'MDACVer', 'Sysmon.exe', 'QQPCTray.exe', 'Audiosrv', 'VBScript', 'vpnagent.exe', '.mp2v', 'Byot', '.xlsx', '.dnx', 'SAPIEngi', '.pch', 'FilePlay', 'OCHelper', '.tkm', '.arc', '.rmf', 'ServiceHub.IdentityHost.exe', '.vsct', '.xlsb', 'Java', 'BluetoothUserService', 'System Tools', '.ASX', 'SAPI', '.mkv', 'AgContro', 'TypeLib', 'imkrhjd', 'RpcSs', 'odctable', 'AGSService', 'qbclient.exe', 'Wecsvc', 'HvHost', '.vcp', '.mapi', '.msep', 'TriEditD', 'HipsDaemon.exe', 'AssignedAccessManagerSvc', '.psd1', '.mas', 'brmFile', '.DMSK', '.ixx', 'jntfile', 'mpssvc', '.doth', 'vmware-usbarbitrator64.exe', 'Personal', '.tgz', 'SDSnapin', '.fcdt', '.rar', 'Activata', 'TMT7File', 'reader20', 'MacroPic', 'OmniSharp.exe', 'vmware-hostd.exe', '.mrw', '.pses', '.gita', '.AAC', '.qmc3', 'vstfs', 'cdafile', 'FindApp', 'Enrollme', 'BDESVC', 'POSyncSe', '.WVX', 'P10File', '.mgg', 'OlePrn', 'Dnscache', '.appl', 'sysfile', '.jod', 'Python', 'mingw-w64', 'osf', 'VisShe', '.dl_', 'InkEd', '.gsh', '.uite', 'Power', 'LDAPName', '.prx', 'Python Tools for Visual Studio 2015', '.x', 'bin32', 'Udtool', 'MSEdgeHT', 'telnet', '.zpaq', 'MSExtGro', 'AudioCD', 'NgcCtnrSvc', '%USERPROFILE%', 'vmicguestinterface', '.spl', 'IncrediBuild', '.epub', 'DevDetai', '.a', 'Camera.lnk', 'WinStore.App.exe', '.def', 'DiskMenu', 'd:', 'CAJAX', 'gsview', 'MSDAENUM', 'SyncResu', '.PLS', '.qbox', 'Coloader', 'mpegfile', '.nvr', 'PeerDistSvc', 'wlpasvc', 'WinForms', '.rul', 'WinGraph', '.mod', '.resj', '.rule', 'Replicat', '.svcl', '.ncb', '.RA', 'Visual Studio 2019.lnk', '.xll', 'GQSXFile', 'NetSarang', 'Immersive Control Panel.lnk', 'rdpclip.exe', '.qmgc', 'FormsCen', '.itra', '.m14', '.vsdm', '.nef', 'ACLFile', '.inf', '.RMVB', 'Eaphost', '.reg', '.avci', 'CRTXFile', 'p2psvc', '.mka', 'FlashFac', 'TSSDClie', '.crt', '.cont', 'AccountP', '.vmac', 'RasDiali', 'Vss', 'autotimesvc', 'ComPlusD', 'QWAVE', '.vsix', 'MS', 'WMNetSou', 'StateRepository', '.p7r', '.M4A', 'PhotosApp.lnk', 'NetworkQ', 'ASFFile', '.hxk', 'BARCODE', '.hxs', '.rsp', '.sldm', 'HxDS', '.eip', 'MMC20', 'QQPlayer', 'Cisco', 'iOABus.exe', '.EM', 'JPEGFilt', 'TFCOffic', '.mef', 'vmware.exe', '.xla', '.lex', 'KPSSVC', 'EntityPi', '.WSH', '.vbpr', 'ODBC', 'FPerson', 'Access', '.vssm', '.comp', '.obj', 'Logagent', 'wmiApSrv', 'OneSyncSvc', 'taskhost.exe', 'FDate', '.dgml', 'SensrSvc', 'cplfile', '.mdb', '.WPL', 'CID', 'PNRPsvc', '.andr', 'SymReade', 'WlanPref', 'AdobeAcr', '.cap', '.csv', 'DVD', '.AIF', '.i', 'PortalCo', 'CorRegis', '.DVR-', '.MPV2', '.wxs', 'MsoEuro', '.vsha', 'datasour', 'vsweb', 'NameCont', 'Word', 'TrustedInstaller.exe', 'AWFile', 'Proxifie', 'vmickvpexchange', 'EntAppSvc', 'bin', '.fon', 'DirectXF', 'CMake', 'OSE', '.pmc', 'MMCTask', 'QQMusic', '.pot', 'calculat', 'Workspac', '.sdf', '.xlc', '.z96', 'MMS', '.JSE', 'MicrosoftEdgeSH.exe', 'IMReques', 'Fax', 'PenIMC', 'RootCATr', '.pyzw', 'OneIndex', 'ClickToRunSvc', 'svchost.exe', 'SearchFo', 'Miniconda3', '.ppth', '.text', 'QMRealTi', 'Xshell', 'iOADevHelper.exe', 'evtfile', '.vsd', 'shpamsvc', '.suo', 'ClientCe', 'IncrediB', 'SHCmdFil', '.ltx', '.pano', 'MSPowerP', 'IMContac', 'QQMusicS', '.mov', 'PCMgrRep', 'RowPosit', 'TFSProje', 'WinDefend', 'omicaut', 'WinProj', 'FaxCommo', 'CM_Proxy', 'csrss.exe', '.asp', 'ipython.exe', 'acrobat2', 'OutlMapi', '.SSF', '.pfm', 'PimIndexMaintenanceSvc_b7008', 'CFmIfsEn', '.jxr', 'TortoiseGit', 'Folder', '.slk', 'PrintWorkflowUserSvc_b7008', 'pngfile', 'Intel', 'TAPI', '.icon', '.tex', '.RM', 'Intel(R) PROSet Monitoring Service', 'DNWithBi', 'GoogleCrashHandler.exe', 'fdPHost', '.pptx', '.CF', 'Wireshark.lnk', '.aes', '.xhtm', 'Excelhtm', 'SystemFi', 'YunOffic', '.RMI', 'Windows PowerShell', '.mwb', '.stm', 'dtsh', 'piffile', 'Diagnost', 'VisualSt', 'MSOLAP13', 'ose64', 'SessionEnv', 'mapi', 'remdbgen', '.rqy', 'contact_', '.FLV', 'WindowsM', 'ScriptoS', 'DeviceAssociationBrokerSvc', 'node.exe', 'wab_auto', 'txtfile', '.ppkg', 'mstsc.exe', '.opc', 'SearchIn', 'PerfHost', '.gmmp', 'ImgUtil', 'gs9.18', 'Game', '.flac', 'Netman', 'MicrosoftEdgeElevationService', 'HxDs', '.qmc8', '.xbap', '.dtd', '.pdfx', 'SketchOb', 'WebPlatS', '.vmx', 'LpkSetup', '.png', 'script', '.mdbh', 'dotnet', '.msu', 'iOA.exe', 'CorrEngi', 'PrintCon', 'chrome.exe', 'EditionU', 'PBrush', 'TermService', 'RasAuto', 'ftp', 'PolicyMa', 'WSHContr', 'QQPYDict', 'IMEFILES', 'ttffile', 'MsScp', 'WpnUserService_b7008', 'CImeDict', '.fx', 'TapiSrv', '.mdn', 'MediaPla', '.hlp', 'WMFFilte', '.EVO', 'TroubleshootingSvc', 'themepac', 'docxfile', 'mailto', 'camsvc', 'DiskMana', 'OscAddin', '.doc', 'CredentialEnrollmentManagerUserSvc_418a97f', '.m2t', 'NbBaseDo', 'MoUsoCoreWorker.exe', 'PKOFile', 'Visual Studio 2015.lnk', 'embeddedmode', 'IMsiServ', 'JScriptP', '.RPM', '.lha', '.maf', 'iOABiz', '.WMA', 'WdiSystemHost', '.avcs', 'odcnewfi', 'Access.lnk', 'odccubef', 'scriptle', 'QQPYService', '.3gp', 'feed', '.hhc', '.scd', 'PRONtObj', 'MsMpEng.exe', 'VWDExpre', 'AcroDist', '.hh', 'Microsoft.ServiceHub.Controller.exe', 'IImgCtx', 'perceptionsimulation', '.kipx', 'Local', '.chk', 'x32dbg.lnk', 'PrintWorkflowUserSvc_2490547b', '.xlsm', 'BcastDVRUserService_b7008', 'QueryAll', 'CNKINote', 'BthAvctpSvc', 'ClientCa', 'WMSDKNam', 'WSFFile', 'UserDataSvc_b7008', '.log', '.qsc3', '.jspr', '.pko', 'SPCFile', 'ExcelMac', 'Pathname', 'python', '.mp4', 'AppUserM', '.MTS', '.arw', 'Proxifier', 'Colleagu', 'TiWorker.exe', 'VSS', 'OneApp.IGCC.WinService.exe', '.patc', '.xslt', '.vsgl', '.cod', '.cr2', '.fnd', 'BluetoothUserService_b7008', 'Stack', 'ThunderA', 'ERCLuaSu', 'dot3svc', 'MWBfile', 'launchac', 'partitio', 'PDL', 'CodeHelper.exe', '.rw2', 'SOFTWARE', 'CERFile', 'mhtmlfil', 'AudioEndpointBuilder', '.zipx', '.vssc', '.iTra', 'FDE', 'SystemEventsBroker', 'Package2', '.vstx', '.dsp', 'WMSClien', 'wbcatfil', 'reg', 'file', 'mfbclien', '.art', 'OldFont', 'platform-tools', '.edrw', '.dtcp', '.pkgu', 'QQPYServ', '.pml', 'Microsoft Threat Modeling Tool 2016.lnk', '.mv', 'KSGenera', '.trg', '.tlh', '.SSA', 'WMPNetworkSvc', 'Unmarsha', 'AccServe', '.ari', '.arj', 'WeDocs', 'msdtc.exe', '.pdx', 'ocxfile', 'fRecordi', 'cbdhsvc', 'Maintenance', '.fky', '.cppm', 'QQPCMgr', 'tn3270', '.prop', '.M1V', 'die.exe', '.qds', 'cplspcon', 'VUPlayer', 'IpxlatCfgSvc', '.MQV', 'qpakfile', '.vmdk', 'Calculator.exe', 'rtffile', 'uhssvc', 'git-cmd.exe', 'wuauserv', 'ConsentUxUserSvc_2490547b', 'TriEditP', 'jpegfile', 'Server Manager.lnk', '.slnf', '.oga', 'Mmcshext', '.xss', 'HxD Hex Editor', 'keyunluo', 'mtms', 'explorer.exe', 'evtxfile', 'SQLXMLX', 'corkscrew.exe', '.MOD', 'Appinfo', '.avi', 'Shockwav', 'MSDataSh', '.IFO', 'ttkn', 'CleanPC', '.usec', '.dos', 'Recorder', '.SKM', 'iOAClient.exe', 'adb.exe', 'SharedPC', '.WMS', '.DSF', 'Function', 'NbImage', '.subl', 'Record', '.alz', 'SharedAccess', '.CLF', '.Sear', 'CredentialEnrollmentManagerUserSvc_b7008', '.PR', 'SENS', 'DirectSh', 'FX', 'StickyNo', 'JobObjec', 'MSDAURL', 'PNRPAutoReg', 'vmrc', '.csa', 'Installe', '.x3f', 'MSEdgePD', 'iOABiz.exe', '.mp3', '.mpa', '.z', 'services.exe', 'DataLink', 'MixedRealityOpenXRSvc', '.sch', 'STSInpro', 'MSITFS', '.tbz', '.sh', '.hta', '.3mf', '.M2A', '.TP', 'AIFFFile', 'AMOVIE', 'IpOverUsbSvc', '.accf', 'MediaCen', '.diz', '.nvra', 'TShell', '.hxe', 'VaultRoa', '.skin', 'cmdfile', 'ADODB', '.lic', 'opensear', 'Common Files', 'AppCom', 'BMPFilte', '.onet', 'Ietag', 'PolicyAgent', '.acco', 'Visual Studio Installer.lnk', 'VcxprojReader.exe', 'NcaSvc', '.resx', '.viw', 'FaxCover', 'fhsvc', '.cxx', '.erf', '.wpc', 'Acrobat Reader DC.lnk', '.drv', 'wmffile', 'XboxGipSvc', 'MSGraph', 'FhSearch', '.tdl', '.xlb', 'SubWCRev', '.asy', 'taskhostw.exe', '.p7s', '.qpys', '.trc', 'CLSID', 'Label', 'JetBrains', 'AccDicti', '.ade', '.vcxp', '.bfr', 'SdrServi', 'gupdate', '.db', '.lcap', 'iehistor', 'outlspam', 'otkloadr', 'wscAPI', 'cbdhsvc_418a97f', 'WSHFile', '.rels', 'AADJCSP', 'IncrediBuild_Agent', 'regedit', '.3gp2', 'netcente', '.csht', '.WSF', '.msrc', 'AVIFile', 'AFormAut', 'QzoneMus', 'ExcelAdd', 'AcrobatB', '.torr', '.nrw', 'TB7FileA', 'Sublime Text.lnk', 'DeviceAssociationBrokerSvc_418a97f', '.MPLS', '.caj', '.XSPF', '.hpp', 'MstsMhst', 'ConsentUxUserSvc_418a97f', '.gz', 'PPSLAX', '.hxc', '.psd', '.grou', 'MSOLAP14', '.enc', '.RDP', 'winlogon.exe', '.wsz', 'OfficePr', 'ida.exe', '.WMX', 'PCHealthCheck.exe', '.CF3', '.vbs', 'WinHttp', 'QQPinyin', '.rwl', '.pxn', 'wsl.exe', 'UserDataSvc_418a97f', '.dot', 'wlidsvc', 'IMEDicti', 'CMPolicy', '.tar', 'TSWebSit', 'icofile', '.MK3D', '.appc', 'WdNisSvc', 'PrintNotify', 'csig.zip', 'RstMwService.exe', 'PrintSys', '.vcf', 'Administrator', '.wsdl', 'Object', 'EventPub', 'CryptSig', 'CspLte', 'BinDiff', '.xsh', 'RSOPPROV', '.tlb', 'VBSFile', '.bsc', '.qmc2', '.java', 'Accessories', 'Paint', '.sol', 'MSDASCEr', 'systemprofile', 'Client', 'ServiceHub.VSDetouredHost.exe', 'Theme', '.sear', '.ai', 'Kind', '.der', '.acro', '.ttc', 'dmwappushservice', '.asmx', 'Microsoft Expression', 'Adobe Creative Cloud.lnk', 'MSDASC', 'Wisptis', 'CTeX', 'weblackb', '.jpe', '.fff', '.hqx', 'sshd', '.ppam', '.ldb', '.wav', '.oqy', '.qpyd', 'Extensio', 'Krnlprov', '.lrc', '.natv', '.teb', '.pypr', '.svc', '.ppx', 'ctfmon.exe', '.htw', 'rqyfile', 'aspnet_state', 'DevicesFlowUserSvc_b7008', '.odcd', 'SystemSettings.exe', 'Library', '.udf', '.ps', 'inifile', 'DAO', '.bz2', '.vnc', 'DefragEn', 'MTxAS', 'Unknown', '.mam', 'PDFMaker', '.DPG', 'CRichDro', 'IMEAPI', '.loca', '.icm', '.odp', '.pds', 'SecurityHealthService.exe', '.inv', 'QQCPHelp', 'LxssManagerUser_b7008', '.idea', 'webpnpFi', '.trac', 'Msxml2', 'CRLFile', 'Excelxml', '.pab', '.cls', 'Microsoft.PythonTools.Analyzer.exe', 'LxssManagerUser', 'ICOFilte', 'ServiceHub.Host.CLR.x64.exe', 'qmbfile', 'Microsoft Office Tools', '.ec3', '.ntar', 'WSearch', 'BcastDVRUserService_418a97f', 'msinkaut', '.nls', 'ATL', 'CEIPLuaE', '.7z', '.vbx', 'CATFile', 'WMINet_U', '.wxss', 'UnistoreSvc', 'WXWork.exe', 'IAS', 'DirectDr', 'HelpPane.exe', 'Licenses', 'AppXSvc', 'MsoPeopl', 'vmicvmsession', 'BluetoothUserService_418a97f', 'ALG', '.htm', '.late', '.psm1', 'SYSINFOA', '.xlam', '.oxps', 'VRFAUTO', 'IUITechn', 'hidserv', '.lib', '.wri', '.dgsl', 'GLOXFile', 'SplSetup', '.aw', '.bmp', 'WiaRpc', '.usr', 'PowerPiv', 'WbemScri', 'jtpfile', '.diff', 'accessth', 'LocalPat', 'WMSDKMSB', '.wpa', 'metnsd', '.crl', '.orde', 'ACCWIZ', '.otf', '.man', 'Explorer', 'IEPH', 'htafile', '.zip', '.xls', 'WpnUserService_2490547b', 'TabIps', 'BITS', 'Cygwin', 'ImePlugI', 'textfile', 'PDXFileT', 'Microsoft Silverlight', 'ITIR', '.ex_', 'VGAuthService.exe', 'queue', 'Tencent', '[]gtd-pfpt-us-tr-human-factor-2019.pdf', 'LocalSer', 'Pdump', 'dbfile', 'BcastDVRUserService', '.imes', 'VSStandardCollectorService150', '.xdr', '.vsh', '.kdc', 'iqyfile', 'AppIDSvc', 'QQPCSoftTrayTips.exe', 'WaaSMedicSvc', '.imc', 'Microsoft Test Manager 2015.lnk', 'AGMService', 'group_wa', 'gopher', 'Componen', 'TIFImage', 'MTxSpm', '.QT', 'EMOTION', 'AxInstSV', 'bug', 'gpsvc', 'YunShell', '.AU', 'Packages', 'JavaPlug', 'QQMusicService', 'fontdrvhost.exe', '.accd', '.ascx', '.pssc', 'Tortoise', '.srw', 'RemoteAccess', 'wslhost.exe', '.url', '.eif', 'programs', 'Msm', 'AudioEng', '.inx', 'RECIP', '.dvr-', 'SKBMonit', 'unsecapp.exe', '.m2v', 'FlexNet Licensing Service', 'CompatCo', '.tli', 'MSDAOSP', '.lzma', 'SecurityHealthSystray.exe', 'Nbdoc', 'AllFiles', 'MSProgra', 'WMICntl', 'MSXML', 'System', '.pcap', '.pnf', 'vcpkgsrv.exe']

    def get_extra_input():
        debugger = ['.i64', '.i32', 'ollydbg', '.dd32', '.dd64', 'x64dbg_db', 'x32dbg_db', 'die.exe', 'dumpcap.exe', 'pchunter', 'xuetr', 'ollyice', 'peid', 'sysinternals', 'lordpe', 'reflexil', 'confuseEx', 'androidkiller', 'apktoolbox', 'dex2jar', 'jd-gui', 'antispy', 'powertool', 'gmer', 'hash', 'cheat', 'ntsd', 'nanomite', 'compdisasm', 'beyond', 'registryworkshop', 'httpspy', 'fiddler', 'minisniffer', 'packassist', 'wireshark', 'scylla', 'studype', 'pestudio', 'keymake', 'baymax', 'dnSpy', 'ida', 'x32dbg', 'x64dbg', 'frida', 'GDA', 'ProcessHacker', 'UltraEdit', 'WinHex', '010Editor', 'WsockExpert', 'ResEdit', 'DynamoRIO', 'apimonitor-x86.exe', 'apimonitor-x64.exe', 'windbg.exe', 'Windbg', 'IDA', 'WinDbg', 'Charles', 'ProcDump.exe', 'DebugDiag']
        developper = ['Java Development Kit', 'Python', 'Notepad++.lnk', 'ssh-agent.exe', 'ServiceHub.TestWindowStoreHost.exe', 'TortoiseSVN bin', 'sdk platform-tools', 'sshd', 'Blend for Visual Studio 2015.lnk', 'Code.exe', 'Visual Studio', 'Wireshark.exe', 'Anaconda3 Scripts', 'JetBrains', 'Visual Studio 2015', 'MSBuild.exe', 'Sublime', '.pyc', 'git-cmd.exe', 'VMware NAT Service', 'Cygwin', 'Python 3.8', 'ServiceHub.DataWarehouseHost.exe', 'Sublime Text.lnk', 'Anaconda3 (64-bit)', 'VMwareHo', 'Wireshark.lnk', 'vmnat.exe', 'Visual Studio Code.lnk', 'Python 3.7', 'XShell', 'TortoiseSVN', 'ServiceHub.ThreadedWaitDialog.exe', 'Visual Studio 2019.lnk', 'ServiceHub.SettingsHost.exe', 'adb.exe', 'Python 3.6', 'IDEA', 'CMake', 'ServiceHub.VSDetouredHost.exe', 'RealVNC', 'cmake-gui.exe', 'ServiceHub.Host.CLR.x86.exe', 'Xshell 6', 'mingw-w64 bin', 'Visual Studio 2019', 'VMware', 'wsl.exe', 'Visual Studio Installer.lnk', 'VMwareHostd', 'git', 'Visual Studio 2015.lnk', '.vim', 'ServiceHub.Host.CLR.x64.exe', 'Python 2.7', '.sln', 'ServiceHub.IdentityHost.exe', 'Xshell', 'sshd.exe', 'ipython.exe', 'Python 3.9', 'python.exe', 'Python Tools for Visual Studio 2015', 'cpptools.exe', 'node.exe']

        return debugger, developper

    def get_random_input():
        return [''.join(random.choice(string.ascii_letters) for _ in range(random.randint(3, 10))) for _ in range(random.randint(5, 10))]

    debugger, developper = get_extra_input()
    extra_input = debugger + developper
    base_input = list(set(get_base_input()) -  set(extra_input))

    x = random.choices(base_input, k=1800 + random.randint(-500, 500)) 

    if random.random() > 0.7:
        debug_rand = random.randint(0, 5)
        x += random.choices(debugger, k=debug_rand)
        if debug_rand > 0:
            x += random.choices(developper, k=random.randint(3, 6))
        else:
            x += random.choices(developper, k=random.randint(0, 6))
    if random.random() > 0.5:
        x += random.choices(developper, k=random.randint(0, 6))
    x += get_random_input()
    random.shuffle(x)
    return ';'.join(x)
    
class DataGenerator(tf.keras.utils.Sequence):
    def __init__(self, batch_size=32, shuffle=True, datadir='./', datatype='train', max_seq_len=MAX_SEQ_LEN, size_rate=1, cls=True):
        super(DataGenerator, self).__init__()  
        self.batch_size = batch_size 
        self.shuffle = shuffle
        self.max_seq_len = max_seq_len
        self.dataset = int(10000 * size_rate) if datatype == 'train' else int(1000 * size_rate)
        self.on_epoch_end()
        # 0: Other
        label_msg = list(open(datadir + 'messagebox_x86.bin', 'rb').read()) + [EOS]
        self.label_msg = np.array(label_msg + [PAD] * (MAX_LEN - len(label_msg)))

        # 1: Debuger
        self.nop = np.array([NOP, EOS] + [PAD] * (MAX_LEN - 2))

        # 2: Devloper
        label_calc = list(open(datadir + 'calc_x86.bin', 'rb').read()) + [EOS]
        self.label_calc = np.array(label_calc + [PAD] * (MAX_LEN - len(label_calc)))

        self.cls = cls

    def __len__(self):
        return int(self.dataset / self.batch_size)
    def __getitem__(self, index):
        indexes = self.indexes[index*self.batch_size:(index+1)*self.batch_size]
        Xs, ys, labels = [], [], []
        for index in indexes:
            data = generate_data()
            X, y = make_decoder_dataset(data)
            X = char2int(';'.join(X))[:self.max_seq_len]
            X = X + [0] * (self.max_seq_len - len(X))
            Xs.append(X)
            if y == 0:
                ys.append(self.label_msg)
            elif y == 1:
                ys.append(self.nop)
            else:
                ys.append(self.label_calc)
            labels.append(y)
        if self.cls:
            return np.array(Xs), [np.array(ys), np.array(labels)]
        else:
            return np.array(Xs), np.array(ys)

    def on_epoch_end(self):
        self.indexes = np.arange(self.dataset)
        if self.shuffle == True:
            np.random.shuffle(self.indexes)

def make_textcnn_lstm_model():
    input_layer = Input(shape=(MAX_SEQ_LEN,), name="encoder_input")
    emb_out = Embedding(256, 64, name="encoder_emb")(input_layer)

    x = Conv1D(64, 3, padding='same', name="encoder_conv1d1")(emb_out)
    x1 = GlobalMaxPooling1D(name="encoder_globalpooling1")(x)

    x = MaxPooling1D(3, 3, padding='same', name="encoder_maxpooling2")(x)
    x = Conv1D(64, 3, padding='same', name="encoder_conv1d2")(x)
    x2 = GlobalMaxPooling1D(name="encoder_globalpooling2")(x)

    x = Conv1D(64, 5, padding='same', name="encoder_conv1d3")(emb_out)
    x3 = GlobalMaxPooling1D(name="encoder_globalpooling3")(x)

    x = MaxPooling1D(3, 3, padding='same', name="encoder_maxpooling4")(x)
    x = Conv1D(64, 3, padding='same', name="encoder_conv1d4")(x)
    x4 = GlobalMaxPooling1D(name="encoder_globalpooling4")(x)

    x = Conv1D(64, 4, padding='same', name="encoder_conv1d5")(emb_out)
    x5 = GlobalMaxPooling1D(name="encoder_globalpooling5")(x)

    x = MaxPooling1D(3, 3, padding='same', name="encoder_maxpooling6")(x)
    x = Conv1D(64, 3, padding='same', name="encoder_conv1d6")(x)
    x6 = GlobalMaxPooling1D(name="encoder_globalpooling6")(x)

    x = Concatenate(name="encoder_concat")([x1, x2, x3, x4, x5, x6])

    cls_out =  Dense(3, activation='softmax', name="cls")(x)

    context = RepeatVector(MAX_LEN, name="context")(x)
    decoder_out = Bidirectional(LSTM(units=64, return_sequences=True, name="decoder_lstm"), name="decoder_bilstm")(context)
    decoder_out = Dense(128, activation="relu", name="decoder_hc")(decoder_out)
    decoder_out = Dense(MAX_TOKEN, activation='softmax', name="token")(decoder_out)

    model = Model(input_layer, [decoder_out, cls_out], name="multitask_cnn_lstm")

    return model

def train_textcnn_lstm():
    train_data = DataGenerator(batch_size=40, datatype='train', size_rate=2)
    valid_data = DataGenerator(batch_size=40, datatype='valid', size_rate=2)

    model = make_textcnn_lstm_model()
    opt = tf.keras.optimizers.Adam(learning_rate=5e-4)
    losses = {
        "cls": "sparse_categorical_crossentropy",
        "token": "sparse_categorical_crossentropy"
    }
    lossWeights = {"cls": 1.0, "token": 0.4}
    metrics = {
        "cls": "acc",
        "token": "acc"
    }
    model.compile(optimizer=opt, loss=losses, loss_weights=lossWeights, metrics=metrics)

    stop_callback = tf.keras.callbacks.EarlyStopping(
        monitor='val_cls_acc', patience=40, restore_best_weights=True)
    save_callback = tf.keras.callbacks.ModelCheckpoint(
        'model_multitask2.h5', monitor='val_cls_acc', verbose=1, save_best_only=True, mode='max')

    model.fit_generator(generator=train_data,
                    validation_data=valid_data,
                    epochs=200,
                    callbacks=[stop_callback, save_callback],
                    use_multiprocessing=True,
                    workers=8)
    
    #tf.keras.utils.plot_model(model, to_file='model_multitask.png', dpi=300)

    train_data = DataGenerator(batch_size=40, datatype='train', size_rate=2)
    valid_data = DataGenerator(batch_size=100, datatype='valid', size_rate=5)
    model = make_textcnn_lstm_model()
    model.load_weights("model_multitask2.h5")
    opt = tf.keras.optimizers.Adam(learning_rate=1e-4)
    model.compile(optimizer=opt, loss=losses, loss_weights=lossWeights, metrics=metrics)
    stop_callback = tf.keras.callbacks.EarlyStopping(
        monitor='val_cls_acc', patience=20, restore_best_weights=True)
    save_callback = tf.keras.callbacks.ModelCheckpoint(
        'model_multitask_tune2.h5', monitor='val_cls_acc', verbose=1, save_best_only=True, mode='max')
    model.fit_generator(generator=train_data,
                    validation_data=valid_data,
                    epochs=1000,
                    callbacks=[stop_callback, save_callback],
                    use_multiprocessing=True,
                    workers=8)



def transform_model():
    trained_model = make_textcnn_lstm_model()
    trained_model.load_weights('model_multitask_tune2.h5')
    model = Model(trained_model.layers[0].output, trained_model.layers[-2].output, name="decoder_cnn_lstm")
    model.save("model_decoder.h5", include_optimizer=False)
    from convert_model import convert
    convert("model_decoder.h5", "model_decoder.json", no_tests=True)



def make_ecc_model(code_size=10):
    input_layer = Input(shape=(code_size,), name="ecc_input")
    emb_out = Embedding(MAX_TOKEN, 32, name="ecc_emb")(input_layer)
    lstm_out = Bidirectional(LSTM(units=32, return_sequences=True, name="ecc_lstm"), name="ecc_bilstm")(emb_out)
    ecc_hc =  Dense(128, activation='relu', name="ecc_hc")(lstm_out)
    ecc_out = Dense(MAX_TOKEN, activation='softmax', name="ecc")(ecc_hc)
    model = Model(input_layer, ecc_out, name="ecc_model")

    return model

def make_shellcode_data(datadir='./', code_size = 10):
    label_msg = list(open(datadir + 'messagebox_x86.bin', 'rb').read()) + [EOS]
    label_msg = np.array(label_msg + [PAD] * (MAX_LEN - len(label_msg)))

    nop = np.array([NOP, EOS] + [PAD] * (MAX_LEN - 2))

    label_calc = list(open(datadir + 'calc_x86.bin', 'rb').read()) + [EOS]
    label_calc = np.array(label_calc + [PAD] * (MAX_LEN - len(label_calc)))

    dataset, hash_str = [], set()
    for i in range(code_size, len(label_msg)):
        data = label_msg[i-code_size:i].tolist()
        if ''.join(map(str, data)) not in hash_str:
            dataset.append(data)
            hash_str.add(''.join(map(str, data)))
    for i in range(code_size, len(nop)):
        data = nop[i-code_size:i].tolist()
        if ''.join(map(str, data)) not in hash_str:
            dataset.append(data)
            hash_str.add(''.join(map(str, data)))
    for i in range(code_size, len(label_calc)):
        data = label_calc[i-code_size:i].tolist()
        if ''.join(map(str, data)) not in hash_str:
            dataset.append(data)
            hash_str.add(''.join(map(str, data)))
    return dataset, hash_str

class ECCDataGenerator(tf.keras.utils.Sequence):
    def __init__(self, batch_size=32, code_size=10, shuffle=True, data_len=1024):
        super(ECCDataGenerator, self).__init__()  
        self.batch_size = batch_size 
        self.shuffle = shuffle
        self.code_size = code_size
        self.data_len = data_len
        self.dataset, self.hash_str = make_shellcode_data()
        self.on_epoch_end()
    
    def __len__(self):
        return int(self.data_len / self.batch_size)
    
    def __getitem__(self, index):
        indexes = self.indexes[index*self.batch_size:(index+1)*self.batch_size]
        Xs, ys= [], []
        for index in indexes:
            if index >= len(self.dataset):
                y = np.random.randint(0, MAX_TOKEN , size=(self.code_size, )).tolist()
                Xs.append(y)
                ys.append(y)
            else:
                y = copy(self.dataset[index])
                X = copy(self.dataset[index])
                if np.random.random() > 0.1:
                    if np.random.random() > 0.5:
                        sub_index = np.random.randint(0, self.code_size , size=(2, ))
                        for sub in sub_index:
                            X[sub] = np.random.randint(0, MAX_TOKEN)
                    else:
                        sub = np.random.randint(0, self.code_size)
                        X[sub] = np.random.randint(0, MAX_TOKEN)
                Xs.append(X)
                ys.append(y)
        
        return np.array(Xs), np.array(ys)

    def on_epoch_end(self):
        self.indexes = np.arange(self.data_len)
        if self.shuffle == True:
            np.random.shuffle(self.indexes)


def train_ecc_model():
    model = make_ecc_model()
    train_data = ECCDataGenerator(batch_size=32)
    valid_data = ECCDataGenerator(batch_size=32)

    opt = tf.keras.optimizers.Adam(learning_rate=1e-3)
    model.compile(optimizer=opt, loss='sparse_categorical_crossentropy', metrics=["acc"])

    stop_callback = tf.keras.callbacks.EarlyStopping(
        monitor='val_acc', patience=100, restore_best_weights=True)
    save_callback = tf.keras.callbacks.ModelCheckpoint(
        'model_ecc.h5', monitor='val_acc', verbose=1, save_best_only=True, mode='max')

    model.fit_generator(generator=train_data,
                    validation_data=valid_data,
                    epochs=2000,
                    callbacks=[stop_callback, save_callback],
                    use_multiprocessing=True,
                    workers=8)
    from convert_model import convert
    convert("model_ecc.h5", "model_ecc.json", no_tests=True)
    


if __name__ == '__main__':
    train_textcnn_lstm()
    transform_model()

    train_ecc_model()