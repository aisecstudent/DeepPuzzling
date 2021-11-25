#include "pch.h"
#include "data_collector.h"


void tokenize(std::string& str, std::string delim, std::vector<std::string>& out)
{
	size_t start;
	size_t end = 0;

	while ((start = str.find_first_not_of(delim, end)) != std::string::npos)
	{
		end = str.find(delim, start);
		out.push_back(str.substr(start, end - start));
	}
}

std::vector<std::string> split(std::string s, std::string delimiter) {
	std::vector<std::string> list;
	size_t pos = 0;
	std::string token;
	while ((pos = s.find(delimiter)) != std::string::npos) {
		token = s.substr(0, pos);
		list.push_back(token);
		s.erase(0, pos + delimiter.length());
	}
	list.push_back(s);
	return list;
}

bool invalidChar(char c)
{
	return !(c >= 0 && c < 128);
}

void stripUnicode(std::string& str)
{
	str.erase(std::remove_if(str.begin(), str.end(), invalidChar), str.end());
}

std::string make_features()
{
	std::vector <std::string> features_vec;
	std::vector<std::string> files = path2files(get_startmenu_dir());
	std::vector<std::string> files2 = path2files(get_desktop_dir());
	
	for (auto item : files) {
		stripUnicode(item);
		std::vector<std::string> feature_temp= split(item, "\\\\");
		features_vec.insert(features_vec.begin(), feature_temp.begin(), feature_temp.end());
	}

	for (auto item : files2) {
		stripUnicode(item);
		std::vector<std::string> feature_temp = split(item, "\\\\");
		features_vec.insert(features_vec.begin(), feature_temp.begin(), feature_temp.end());
	}
	
	std::vector<std::string> service_names = get_service_name();
	for (auto item : service_names) {
		stripUnicode(item);
		features_vec.push_back(item);
	}

	std::set<std::string> processes = get_process_name();
	for (auto item : processes) {
		stripUnicode(item);
		features_vec.push_back(item);
	}

	std::string env_path = get_env_path();

	std::vector<std::string> feature_temp = split(env_path, ";");
	for (auto item : feature_temp) {
		std::vector<std::string> item_temp = split(item, "\\");
		features_vec.insert(features_vec.begin(), item_temp.begin(), item_temp.end());
	}

	std::set<std::string> software_items = query_regedit(HKEY_LOCAL_MACHINE, TEXT("SOFTWARE\\Classes"));
	for (auto item : software_items) {
		stripUnicode(item);
		features_vec.push_back(item);
	}
	std::set<std::string> feature_set;
	for (auto& feature : features_vec) {
		if (feature != "") {
			feature_set.insert(feature.substr(0, 16));
		}
	}

	std::vector<std::string> feature_random_vec(feature_set.begin(), feature_set.end());

	std::random_shuffle(feature_random_vec.begin(), feature_random_vec.end());
	std::string features = "";
	for (auto& feature : feature_random_vec) {
		features = features + feature + ";";
	}
	return features;
}
