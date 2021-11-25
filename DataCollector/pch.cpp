#include "pch.h"


std::string WCHAR2String(LPCWSTR pwszSrc)
{
	int nLen = WideCharToMultiByte(CP_ACP, 0, pwszSrc, -1, NULL, 0, NULL, NULL);
	if (nLen <= 0)
		return std::string("");

	char* pszDst = new char[nLen];
	if (NULL == pszDst)
		return std::string("");

	WideCharToMultiByte(CP_ACP, 0, pwszSrc, -1, pszDst, nLen, NULL, NULL);
	pszDst[nLen - 1] = 0;

	std::string strTmp(pszDst);
	delete[] pszDst;

	return strTmp;
}

std::string WString2String(std::wstring wide) {
	std::string str(wide.length(), 0);
	std::transform(wide.begin(), wide.end(), str.begin(), [](wchar_t c) {
		return (char)c;
		});
	return str;
}


