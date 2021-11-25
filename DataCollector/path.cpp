#include "pch.h"
#include "path.h"

std::string path2file(std::string dir) {
	std::size_t found = dir.find_last_of("/\\");
	return dir.substr(found + 1);
}

std::vector<std::string> path2files(std::string dir) {
	std::vector<std::string> files;
	for (const auto& entry : std::experimental::filesystem::directory_iterator(dir))
		files.push_back(path2file(entry.path().string()));
	return files;
}

std::string get_desktop_dir() {
	WCHAR w_desktop_path[MAX_PATH + 1] = { 0 };
	std::string desktop_path;
	if (SHGetFolderPath(NULL, CSIDL_DESKTOP, NULL, 0, w_desktop_path) != S_OK) {
		desktop_path = "NULL_Desktop";
	}
	else {
		desktop_path = WCHAR2String(w_desktop_path);
	}

	return desktop_path;
}

std::string get_startmenu_dir() {
	WCHAR w_start_menu_path[MAX_PATH + 1] = { 0 };
	std::string start_menu_path;
	if (SHGetFolderPath(NULL, CSIDL_COMMON_PROGRAMS, NULL, 0, w_start_menu_path) != S_OK) {
		start_menu_path = "NULL_StartMenu";
	}
	else {
		start_menu_path = WCHAR2String(w_start_menu_path);
	}

	return start_menu_path;
}