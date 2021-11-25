#include "pch.h"
#include "regedit.h"

std::string filter_rule(std::string key) {
    if (key[0] == '.') {
        if (key[1] == '_')
            return "*";
        return key.substr(0, 5);
    }
    else if (key[0] == '{') {
        return "*";
    }
    size_t pos = key.find_first_of(".- /");
    key = key.substr(0, min(pos, 8));
	return key;
}

std::set<std::string> query_regedit(HKEY hKey, LPCWSTR lpSubKey) {
    std::set<std::string> items;
    HKEY hTestKey;

    if (RegOpenKeyEx(hKey,
        lpSubKey,
        0,
        KEY_READ,
        &hTestKey) == ERROR_SUCCESS
        )
    {
        TCHAR    achKey[MAX_KEY_LENGTH];   // buffer for subkey name
        DWORD    cbName;                   // size of name string 
        TCHAR    achClass[MAX_PATH] = TEXT("");  // buffer for class name 
        DWORD    cchClassName = MAX_PATH;  // size of class string 
        DWORD    cSubKeys = 0;               // number of subkeys 
        DWORD    cbMaxSubKey;              // longest subkey size 
        DWORD    cchMaxClass;              // longest class string 
        DWORD    cValues;              // number of values for key 
        DWORD    cchMaxValue;          // longest value name 
        DWORD    cbMaxValueData;       // longest value data 
        DWORD    cbSecurityDescriptor; // size of security descriptor 
        FILETIME ftLastWriteTime;      // last write time 

        DWORD i, retCode;

        // Get the class name and the value count. 
        retCode = RegQueryInfoKey(
            hTestKey,                    // key handle 
            achClass,                // buffer for class name 
            &cchClassName,           // size of class string 
            NULL,                    // reserved 
            &cSubKeys,               // number of subkeys 
            &cbMaxSubKey,            // longest subkey size 
            &cchMaxClass,            // longest class string 
            &cValues,                // number of values for this key 
            &cchMaxValue,            // longest value name 
            &cbMaxValueData,         // longest value data 
            &cbSecurityDescriptor,   // security descriptor 
            &ftLastWriteTime);       // last write time 

        // Enumerate the subkeys, until RegEnumKeyEx fails.

        if (cSubKeys)
        {
            for (i = 0; i < cSubKeys; i++)
            {
                cbName = MAX_KEY_LENGTH;
                retCode = RegEnumKeyEx(hTestKey, i,
                    achKey,
                    &cbName,
                    NULL,
                    NULL,
                    NULL,
                    &ftLastWriteTime);
                if (retCode == ERROR_SUCCESS)
                {
                    std::string key = filter_rule(WCHAR2String(achKey));
                    items.insert(key);
                }
            }
        }

    }

    RegCloseKey(hTestKey);

    return items;
}