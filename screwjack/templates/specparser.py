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
__version__ = "0.1.0"
__author__ = "xiaolin"

import json
from collections import namedtuple
import types
import os
import itertools

def gettype(name):
    type_map = {
        "string" : "str",
        "integer" : "int",
        "float" : "float",
        "enum" : "str",
        "file" : "str"
    }
    if name not in type_map:
        raise ValueError(name)
    t = __builtins__.get(type_map[name], types.StringType)
    if isinstance(t, type):
        return t
    raise ValueError(name)

def read_whole_file(filename):
    with open(filename, "r") as f:
        return f.read()

class Input(object):
    def __init__(self, x):
        self.x = x

    def __repr__(self):
        return self.x

    def as_first_line(self):
        with open(self.x, "r") as f:
            return f.readline().rstrip()

    def as_whole(self):
        with open(self.x, "r") as f:
            return f.read()

    def as_file(self, mode="r"):
        return open(self.x, mode)

    @property
    def val(self):
        return self.as_first_line()

class Output(object):
    def __init__(self, x):
        self.x = x

    def __repr__(self):
        return self.x

    def as_first_line(self):
        with open(self.x, "r") as f:
            return f.readline().rstrip()

    def as_whole(self):
        with open(self.x, "r") as f:
            return f.read()

    def as_file(self, mode="r"):
        return open(self.x, mode)

    @property
    def val(self):
        return self.as_first_line()

    @val.setter
    def val(self, value):
        with open(self.x, "w+") as f:
            f.write(value)

    def as_file(self, mode="w+"):
        return open(self.x, mode)

class Param(object):
    def __init__(self, x, typeinfo):
        self._x = x
        self._typeinfo = typeinfo

    def __repr__(self):
        return self._x

    @property
    def val(self):
        type_handler = {
            "string" : lambda x : x,
            "float" : lambda x : float(x),
            "integer" : lambda x : int(x),
            "enum" : lambda x : x,
            "file" : read_whole_file
        }
        param_type = self._typeinfo['Type']
        if param_type in type_handler:
            return type_handler[param_type](self._x)
        else:
            return self._x

def input_output_builder(spec_input, spec_output):
    import sys
    params = dict(arg.split("=") for arg in sys.argv[1:])
    if not all(k in params for k in spec_input.keys()):
        raise ValueError("Missing input parameters")
    if not all(k in params for k in spec_output.keys()):
        raise ValueError("Missing output parameters")

    InputSettings = namedtuple('InputSettings', spec_input.keys())
    in_params = {k:Input(params[k]) for k,v in spec_input.items()}
    input_settings = InputSettings(**in_params)

    OutputSettings = namedtuple('OutputSettings', spec_output.keys())
    out_params = {k:Output(params[k]) for k,v in spec_output.items()}
    output_settings = OutputSettings(**out_params)

    return input_settings, output_settings

def param_builder(spec_param, param_json):
    def get_param(k):
        if k in param_json:
            return param_json[k]['Val']
        else:
            return spec_param[k]['Default']

    ParamSettings = namedtuple('ParamSettings', spec_param.keys())
    param_dict = {k:Param(get_param(k), v) for k,v in spec_param.items()}
    env_settings = ParamSettings(**param_dict)
    return env_settings

def global_param_builder(param_json):
    return {k:v['Val'] for k,v in param_json.items()}

def get_settings(spec_json):
    moderate_keys = ['Name', 'Param', 'Input', 'Output', 'Cmd', 'Description']
    if not all(k in spec_json for k in moderate_keys):
        raise ValueError("One of param from %s may not exist in 'spec.json'" % str(moderate_keys))

    # TODO: condition for appending 'GlobalParam'
    moderate_keys.append('GlobalParam')
    ModuleSetting = namedtuple('ModuleSetting', moderate_keys)

    # Load parameters
    param_json = get_json_file(os.getenv("ZETRT"))

    param = param_builder(spec_json['Param'], param_json['PARAM'])
    json_input, json_output = input_output_builder(spec_json['Input'], spec_json['Output'])

    # TODO:
    global_param = global_param_builder(param_json['GLOBAL_PARAM'])
    settings = ModuleSetting(Name=spec_json['Name'], Description=spec_json['Description'], Param=param, Input=json_input, Output=json_output, Cmd=spec_json['Cmd'], GlobalParam=global_param)
    return settings

def get_json_file(filename):
    with open(filename, "r") as f:
        return json.load(f)

def get_settings_from_file(filename):
    with open(filename, "r") as f:
        return get_settings(json.load(f))

def get_settings_from_string(spec_json_str):
    print(json.loads(spec_json_str))
    return get_settings(json.loads(spec_json_str))

# Various Runtime: Hive, Hadoop, Pig
class ZetRuntime(object):
    def __init__(self, spec_filename="spec.json"):
        self.settings = get_settings_from_file(spec_filename)

    def __repr__(self):
        return str(self.settings)

class HiveRuntime(ZetRuntime):
    def get_hdfs_working_dir(self, path=""):
        ps = self.settings
        prj_vars = ps.GlobalParam
        return os.path.join(ps.Param.hdfs_root.val, 'tmp/zetjob', prj_vars['userName'], "job%s" % prj_vars['jobId'], "blk%s" % prj_vars['blockId'])

    def get_hive_namespace(self):
        ps = self.settings
        prj_vars = ps.GlobalParam
        return "zetjob_%s_job%s_blk%s" % (prj_vars['userName'], prj_vars['jobId'], prj_vars['blockId'])

    def hdfs_uploader(self, local_dir):
        hdfs_upload_dir = self.get_hdfs_working_dir(local_dir)
        ext_files = [f for f in sorted(os.listdir(local_dir)) if os.path.isfile(os.path.join(local_dir,f))]
        for f in ext_files:
            f_remote = os.path.join(hdfs_upload_dir, local_dir, f)
            f_remote_dir = os.path.dirname(f_remote)
            if os.system("hadoop fs -mkdir -p %s" % f_remote_dir) != 0:
                raise Exception("Failed to create dir %s" % f_remote_dir)
            print("HDFS Upload :: %s ====> %s" % (f, f_remote))
            print("hadoop fs -copyFromLocal %s %s" % (os.path.join(local_dir, f), os.path.join(f_remote_dir)))
            if os.system("hadoop fs -copyFromLocal %s %s" % (os.path.join(local_dir, f), f_remote_dir)) == 0:
                yield os.path.join(f_remote)
            else:
                raise Exception("Failed to upload file %s to %s" % (f, f_remote))

    def hive_output_builder(self, output_name):
        ps = self.settings
        prj_vars = ps.GlobalParam
        return "zetjob_%s_job%s_blk%s" % (prj_vars['userName'], prj_vars['jobId'], prj_vars['blockId'])

    def header_builder(self, hive_ns, uploaded_files, uploaded_jars):
        # Build Output Tables
        for output_name,output_obj in self.settings.Output._asdict().items():
            output_obj.val = self.hive_output_builder(output_name)

        return "\n".join(
                itertools.chain(
                    ["ADD FILE %s;" % f for f in uploaded_files],
                    ["ADD JAR %s;" % f for f in uploaded_jars],
                    ["set hivevar:MYNS = %s;" % hive_ns],
                    ["set hivevar:PARAM_%s = %s;" % (k,v) for k,v in self.settings.Param._asdict().items()],
                    ["set hivevar:INPUT_%s = %s;" % (k,v.val) for k,v in self.settings.Input._asdict().items()],
                    ["set hivevar:OUTPUT_%s = %s;" % (k,v.val) for k,v in self.settings.Output._asdict().items()]))

    def generate_script(self, hive_script, target_filename=None):
        hdfs_working_dir = self.get_hdfs_working_dir()
        if not clean_hdfs_path(hdfs_working_dir):
            # TODO : refactor to 'HiveException'
            raise Exception("Can not clean hdfs path : %s" % hdfs_working_dir)

        hive_ns = self.get_hive_namespace()

        # Upload files and UDF jars
        file_dir = self.settings.Param.FILE_DIR
        jar_dir = self.settings.Param.UDF_DIR

        uploaded_files = self.hdfs_uploader(file_dir.val)
        uploaded_jars = self.hdfs_uploader(jar_dir.val)

        # Build Input, Output and Param
        header = self.header_builder(hive_ns, uploaded_files, uploaded_jars)
        if target_filename == None:
            import tempfile
            tmp_file = tempfile.NamedTemporaryFile(prefix="hive_generated_", suffix=".hql", delete=False)
            tmp_file.close()
            target_filename = tmp_file.name

        with open(hive_script, "r") as f, open(target_filename, "w+") as out_f:
            out_f.write("--------------------------\n")
            out_f.write("-- Header\n")
            out_f.write("--------------------------\n")
            out_f.write(header)
            out_f.write("\n")
            out_f.write("--------------------------\n")
            out_f.write("-- Main\n")
            out_f.write("--------------------------\n")
            out_f.write("\n")
            out_f.write(f.read())

        return target_filename

    def execute(self, hive_script, generated_hive_script=None):
        generated_hive_script = self.generate_script(hive_script, generated_hive_script)

        if os.system("beeline -u jdbc:hive2://%s:%s -n hive -p tiger -d org.apache.hive.jdbc.HiveDriver -f '%s' --verbose=true "
                % (generated_hive_script, self.settings.Param.HiveServer2_Host, self.settings.Param.HiveServer2_Port)) == 0:
            raise Exception("Failed to execute hive script : %s" % generated_hive_script)

class PigRuntime(object):
    def __init__(self, spec_filename="spec.json"):
        self.settings = get_settings_from_file(spec_filename)

# Utility Functions
def clean_hdfs_path(p):
    if os.system("hadoop fs -rm -r -f %s && hadoop fs -mkdir -p %s" % (p, p)) == 0:
        return True
    else:
        return False

def cmd(cmd_str):
    print(cmd_str)
    return os.system(cmd_str)

if __name__ == "__main__":
    # settings = get_settings_from_file("spec.json")
    # print(settings)
    # print(settings.Input)
    # print(settings.Output)
    # print("-----------------")

    # i = Input("test.param")
    # print(i)
    # print(i.as_one_line())
    # print(i.as_all_line())

    # t = MyTest(4)
    # print(t.val)
    # t.val = 5
    # print(t.val)

    # o = Output("out.param")
    # print(o)
    # print(o.val)
    # o.val = "cacaca"
    # settings = get_settings_from_file("spec.json")
    hive_runtime = HiveRuntime()
    print(hive_runtime)

