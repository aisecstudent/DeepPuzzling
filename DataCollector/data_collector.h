#ifndef _DATA_COLLECTOR_H_
#define _DATA_COLLECTOR_H_
#include "pch.h"

#include "path.h"
#include "network.h"
#include "process.h"
#include "service.h"
#include "env.h"
#include "regedit.h"

void tokenize(std::string& str, std::string delim, std::vector<std::string>& out);
std::vector<std::string> split(std::string s, std::string delimiter);
bool invalidChar(char c);
void stripUnicode(std::string& str);
std::string make_features();

#endif
