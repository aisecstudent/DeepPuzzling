#pragma once
#include "pch.h"

struct ServiceInfo
{
	SERVICE_STATUS ServiceStatus;
	std::string lpDisplayName;
	std::string lpServiceName;
	ServiceInfo(SERVICE_STATUS ServiceStatus, std::string lpDisplayName, std::string lpServiceName) : ServiceStatus(ServiceStatus), lpDisplayName(lpDisplayName), lpServiceName(lpServiceName) {}
};

std::vector<std::string> get_service_name();
