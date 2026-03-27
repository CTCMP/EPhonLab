"""Define EPhonLab version."""

# Copyright (C) 2026 Xianyong Ding
# All rights reserved.
#
# This file is part of EPhonLab.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in
#   the documentation and/or other materials provided with the
#   distribution.
#
# * Neither the name of the phonopy project nor the names of its
#   contributors may be used to endorse or promote products derived
#   from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

# import tomllib  # Python 3.11+
import os, sys
import os.path as osp
from pathlib import Path

config_path = osp.join(os.getcwd(), "ephonlab", "install_ephonlab.toml")

# 自动适配 Python 版本
if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomli as tomllib
    except ImportError:
        raise ImportError("please intall tomli: pip install tomli")

class Config:
    def __init__(self, config_file="~/.ephonlab.toml"):
        self.config_file = Path(config_file)
        self.data = self._load()
    
    def _load(self):
        """Loading TOML configure file"""
        if not self.config_file.exists():
            raise FileNotFoundError(f"file not exist: {self.config_file}")
        
        with open(self.config_file, 'rb') as f:  
            return tomllib.load(f)
    
    def get_submit_script(self, **kwargs):
        """生成提交脚本"""
        params = {
            'job_name': os.getcwd().split('/')[-1],
            'num_process': self.data['calculation']['total_cores'],
            'cal_nodes': self.data['calculation']['cal_nodes'],
            **kwargs
        }
        
        script = self.data['submit_scripts']['template']
        
        for key, value in params.items():
            script = script.replace(f'{{{key}}}', str(value))
        
        return script
    
    def save_script(self, filename="submit.pbs", **kwargs):
        """保存脚本到文件"""
        script = self.get_submit_script(**kwargs)
        
        with open(filename, 'w') as f:
            f.write(script)
        
        os.chmod(filename, 0o755)
        print(f"脚本已保存: {filename}")
        
        return script

# 使用
config = Config(config_path)
config.save_script("submit.sh")
