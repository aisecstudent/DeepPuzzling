#pragma once
#include "pch.h"

#define MAX_KEY_LENGTH 255
#define MAX_VALUE_NAME 16383

std::set<std::string> query_regedit(HKEY hKey, LPCWSTR lpSubKey);
