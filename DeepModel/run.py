# -*- coding: utf-8 -*-

import struct, json, os, hashlib, keras
import numpy as np

project_path = os.path.dirname(os.path.realpath(__file__))
models_path = os.path.join(project_path, '../lib/model')
loader_path = os.path.join(project_path, '../IntentHiding')

def dump_hex2header(model_hexes, ecc_hexes, key=123, max_feature_len=18432):
    template = '''#ifndef _RESOURCE_MODEL_H_\n#define _RESOURCE_MODEL_H_\n\nconst int key = %d;\nconst int max_feature_len = %d;\nconst int decoder_seq_len = 300;\nconst int ecc_seq_len = 10;\nconst int emb_dim = 260;\nconst unsigned char model[] = {%s};\nconst unsigned char ecc[] = {%s};\n\n#endif''' % (key, max_feature_len, ','.join(map(str, model_hexes)), ','.join(map(str, ecc_hexes)))
    with open(os.path.join(loader_path, 'resource_model.h'), 'w') as file_out:
        file_out.write(template)

def dump_model_file(key=123, model_name='model_decoder', ecc_name='model_ecc'):
    model_str = open(os.path.join(models_path, '{}.json'.format(model_name))).read()
    model_chars = [hex(ord(char) ^ key) for char in model_str]
    ecc_str = open(os.path.join(models_path, '{}.json'.format(ecc_name))).read()
    ecc_chars = [hex(ord(char) ^ key) for char in ecc_str]
    dump_hex2header(model_chars, ecc_chars, key=key)

if __name__ == '__main__':
    dump_model_file()