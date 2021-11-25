#include "pch.h"


struct ProcessInfo
{
	DWORD PID;
	std::string PName;
	std::string PPath;
	ProcessInfo(DWORD PID, std::string PNmae, std::string PPath) : PID(PID), PName(PNmae), PPath(PPath) {}

	bool operator < (const ProcessInfo& rhs) const {
		return (PID < rhs.PID);
	}
};

std::vector<ProcessInfo> GetProcessInfo();
std::set<std::string> get_process_name();
