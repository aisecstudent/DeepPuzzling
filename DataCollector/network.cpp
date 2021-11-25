#include "pch.h"
#include "network.h"

std::string get_domain() {
	std::string domain;
	DSROLE_PRIMARY_DOMAIN_INFO_BASIC* info;
	DWORD dw = DsRoleGetPrimaryDomainInformation(NULL,
		DsRolePrimaryDomainInfoBasic,
		(PBYTE*)&info);
	if (dw != ERROR_SUCCESS)
	{
		domain = "NULL_Domain";
	}

	if (info->DomainNameDns == NULL)
	{
		domain = "NULL_Domain";
	}
	else
	{
		domain = WString2String(info->DomainNameDns);
	}
	return domain;
}

std::vector<NetCard> get_netcard() {
	std::vector<NetCard> netcard;

	PIP_ADAPTER_INFO pIpAdapterInfo = new IP_ADAPTER_INFO();
	unsigned long stSize = sizeof(IP_ADAPTER_INFO);
	int nRel = GetAdaptersInfo(pIpAdapterInfo, &stSize);

	if (ERROR_BUFFER_OVERFLOW == nRel)
	{
		delete pIpAdapterInfo;
		pIpAdapterInfo = (PIP_ADAPTER_INFO)new BYTE[stSize];
		nRel = GetAdaptersInfo(pIpAdapterInfo, &stSize);
	}

	if (ERROR_SUCCESS == nRel)
	{
		while (pIpAdapterInfo)
		{
			IP_ADDR_STRING* pIpAddrString = &(pIpAdapterInfo->IpAddressList);
			do
			{
				netcard.emplace_back(pIpAdapterInfo->Description, pIpAddrString->IpAddress.String, pIpAdapterInfo->GatewayList.IpAddress.String);
				pIpAddrString = pIpAddrString->Next;
			} while (pIpAddrString);
			pIpAdapterInfo = pIpAdapterInfo->Next;
		}

	}

	if (pIpAdapterInfo)
	{
		delete pIpAdapterInfo;
	}
	return netcard;
}

std::vector<std::string> list_netcard() {
	std::vector<std::string> netcard;

	PIP_ADAPTER_INFO pIpAdapterInfo = new IP_ADAPTER_INFO();
	unsigned long stSize = sizeof(IP_ADAPTER_INFO);
	int nRel = GetAdaptersInfo(pIpAdapterInfo, &stSize);

	if (ERROR_BUFFER_OVERFLOW == nRel)
	{
		delete pIpAdapterInfo;
		pIpAdapterInfo = (PIP_ADAPTER_INFO)new BYTE[stSize];
		nRel = GetAdaptersInfo(pIpAdapterInfo, &stSize);
	}

	if (ERROR_SUCCESS == nRel)
	{
		while (pIpAdapterInfo)
		{
			IP_ADDR_STRING* pIpAddrString = &(pIpAdapterInfo->IpAddressList);
			do
			{	
				netcard.push_back(pIpAdapterInfo->Description);
				pIpAddrString = pIpAddrString->Next;
			} while (pIpAddrString);
			pIpAdapterInfo = pIpAdapterInfo->Next;
		}

	}
	if (pIpAdapterInfo)
	{
		delete pIpAdapterInfo;
	}
	return netcard;
}