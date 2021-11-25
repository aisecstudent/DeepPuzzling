#include "pch.h"
#include "process.h"

std::vector<ProcessInfo> GetProcessInfo()
{
	STARTUPINFO st;
	PROCESS_INFORMATION pi;
	PROCESSENTRY32 ps;
	HANDLE hSnapshot;
	HANDLE processHandle = NULL;
	std::vector<ProcessInfo> PInfo;

	ZeroMemory(&st, sizeof(STARTUPINFO));
	ZeroMemory(&pi, sizeof(PROCESS_INFORMATION));
	st.cb = sizeof(STARTUPINFO);
	ZeroMemory(&ps, sizeof(PROCESSENTRY32));
	ps.dwSize = sizeof(PROCESSENTRY32);

	hSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);

	if (hSnapshot == INVALID_HANDLE_VALUE)
	{
		return PInfo;
	}

	if (!Process32First(hSnapshot, &ps))
	{
		return PInfo;
	}

	do
	{
		processHandle = OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, FALSE, ps.th32ProcessID);
		TCHAR filename[MAX_PATH];
		if (processHandle != NULL) {
			if (GetModuleFileNameEx(processHandle, NULL, filename, MAX_PATH) == 0) {
				_tcscpy_s(filename, MAX_PATH, _T("NULL_Module"));
			}
			CloseHandle(processHandle);
		}
		else {
			_tcscpy_s(filename, MAX_PATH, _T("NULL_Process"));
		}
		PInfo.emplace_back(ps.th32ProcessID, WCHAR2String(ps.szExeFile), WCHAR2String(filename));


	} while (Process32Next(hSnapshot, &ps));

	CloseHandle(hSnapshot);

	std::sort(PInfo.begin(), PInfo.end());

	return PInfo;
}

std::set<std::string> get_process_name() {
	STARTUPINFO st;
	PROCESS_INFORMATION pi;
	PROCESSENTRY32 ps;
	HANDLE hSnapshot;
	std::vector<ProcessInfo> PInfo;

	ZeroMemory(&st, sizeof(STARTUPINFO));
	ZeroMemory(&pi, sizeof(PROCESS_INFORMATION));
	st.cb = sizeof(STARTUPINFO);
	ZeroMemory(&ps, sizeof(PROCESSENTRY32));
	ps.dwSize = sizeof(PROCESSENTRY32);

	hSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);

	std::set<std::string> process_name;

	if (hSnapshot == INVALID_HANDLE_VALUE)
	{
		return process_name;
	}

	if (!Process32First(hSnapshot, &ps))
	{
		return process_name;
	}

	do
	{
		process_name.insert(WCHAR2String(ps.szExeFile));
	} while (Process32Next(hSnapshot, &ps));

	CloseHandle(hSnapshot);

	return process_name;
}

