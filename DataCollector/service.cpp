#include "pch.h"
#include "service.h"
#include "data_collector.h"


std::vector<std::string> get_service_name() {
	std::vector<std::string> service_names;
	SC_HANDLE scHandle = OpenSCManager(NULL, NULL, SC_MANAGER_ENUMERATE_SERVICE);
	if (scHandle == NULL) {
		service_names.push_back("NULL_Service");
	}
	else {
		SC_ENUM_TYPE infoLevel = SC_ENUM_PROCESS_INFO;
		DWORD dwServiceType = SERVICE_WIN32;
		DWORD dwServiceState = SERVICE_STATE_ALL;
		LPBYTE lpServices = NULL;
		DWORD cbBufSize = 0;
		DWORD pcbBytesNeeded;
		DWORD servicesReturned;
		LPDWORD lpResumeHandle = NULL;
		LPCWSTR pszGroupName = NULL;

		BOOL ret = EnumServicesStatusEx(scHandle, infoLevel, dwServiceType, dwServiceState, lpServices, cbBufSize, &pcbBytesNeeded, &servicesReturned, lpResumeHandle, pszGroupName);

		cbBufSize = pcbBytesNeeded;
		lpServices = new BYTE[cbBufSize];
		if (NULL == lpServices)
		{
			service_names.push_back("NULL_Service");
		}
		else {
			ret = EnumServicesStatusEx(scHandle, infoLevel, dwServiceType, dwServiceState, lpServices, cbBufSize, &pcbBytesNeeded, &servicesReturned, lpResumeHandle, pszGroupName);
			LPENUM_SERVICE_STATUS_PROCESS lpServiceStatusProcess = (LPENUM_SERVICE_STATUS_PROCESS)lpServices;
			for (DWORD i = 0; i < servicesReturned; i++) {
				service_names.push_back(WCHAR2String(lpServiceStatusProcess[i].lpServiceName));
			}
			delete[] lpServices;
		}
		CloseServiceHandle(scHandle);
	}

	return service_names;
}

