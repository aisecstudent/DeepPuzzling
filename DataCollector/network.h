#pragma once
#include "pch.h"

struct NetCard {
	std::string desc;
	std::string ip;
	std::string gateway;
	NetCard(std::string desc, std::string ip, std::string gateway) : desc(desc), ip(ip), gateway(gateway) {}
};

std::string get_domain();
std::vector<NetCard> get_netcard();
std::vector<std::string> list_netcard();
