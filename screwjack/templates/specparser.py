#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2014, Zetyun
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are
# permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of
#    conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list
#    of conditions and the following disclaimer in the documentation and/or other
#    materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors may be
#    used to endorse or promote products derived from this software without specific
#   prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
# SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
# DAMAGE.

"""
A minimum spec.json parser.
"""

import json
from collections import namedtuple

def input_output_builder(spec_input, spec_output):
    import sys
    params = dict(arg.split("=") for arg in sys.argv[1:])
    if not all(k in params for k in spec_input.keys()):
        raise ValueError("Missing input parameters")
    if not all(k in params for k in spec_output.keys()):
        raise ValueError("Missing output parameters")

    InputSettings = namedtuple('InputSettings', spec_input.keys())
    in_params = {k:params[k] for k,v in spec_input.items()}
    input_settings = InputSettings(**in_params)

    OutputSettings = namedtuple('OutputSettings', spec_output.keys())
    out_params = {k:params[k] for k,v in spec_output.items()}
    output_settings = OutputSettings(**out_params)

    return input_settings, output_settings

def env_builder(spec_env):
    import os
    env = dict(os.environ)
    EnvSettings = namedtuple('EnvSettings', spec_env.keys())
    # TODO : underscore-fy name of environment variable
    param_dict = {k:env.get("ZETENV_%s" % k, v['default']) for k,v in spec_env.items()}
    env_settings = EnvSettings(**param_dict)
    return env_settings

def get_settings(spec_json_dict):
    ret = spec_json_dict
    moderate_keys = ['Name', 'Env', 'Input', 'Output', 'Cmd', 'Description']
    if not all(k in ret for k in moderate_keys):
        raise ValueError("One of param from %s may not exist in 'spec.json'" % str(moderate_keys))

    ModuleSetting = namedtuple('ModuleSetting', moderate_keys)

    env = env_builder(ret['Env'])
    input, output = input_output_builder(ret['Input'], ret['Output'])
    settings = ModuleSetting(Name=ret['Name'], Description=ret['Description'], Env=env, Input=input, Output=output, Cmd=ret['Cmd'])
    return settings

def get_settings_from_file(filename):
    with open(filename, "r") as f:
        return get_settings(json.load(f))

def get_settings_from_string(spec_json_str):
    print(json.loads(spec_json_str))
    return get_settings(json.loads(spec_json_str))

if __name__ == "__main__":
    settings = get_settings_from_file("spec.json")
    print(settings)
    print(settings.Input)
    print(settings.Output)
    print("-----------------")

