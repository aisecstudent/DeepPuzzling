#include "pch.h"
#include "env.h"

using environment_t = std::unordered_map<std::wstring, std::wstring>;

environment_t get_env_data() {
	environment_t env;

	auto free = [](wchar_t* p) { FreeEnvironmentStrings(p); };
	auto env_block = std::unique_ptr<wchar_t, decltype(free)>{
		GetEnvironmentStrings(), free };

	for (const wchar_t* name = env_block.get(); *name != L'\0'; )
	{
		const wchar_t* equal = wcschr(name, L'=');
		std::wstring key(name, equal - name);

		const wchar_t* pValue = equal + 1;
		std::wstring value(pValue);

		env[key] = value;

		name = pValue + value.length() + 1;
	}

	return env;
}

std::string get_env_path() {
	auto free = [](wchar_t* p) { FreeEnvironmentStrings(p); };
	auto env_block = std::unique_ptr<wchar_t, decltype(free)>{
		GetEnvironmentStrings(), free };

	for (const wchar_t* name = env_block.get(); *name != L'\0'; )
	{
		const wchar_t* equal = wcschr(name, L'=');
		std::wstring key(name, equal - name);

		const wchar_t* pValue = equal + 1;
		std::wstring value(pValue);

		if (key == L"Path") {
			return WString2String(value);
		}

		name = pValue + value.length() + 1;
	}

	return "";
}