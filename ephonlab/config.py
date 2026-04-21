"""configure submit script."""

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

import os, sys
from pathlib import Path

# python version
if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomli as tomllib
    except ImportError:
        raise ImportError("Please install tomli: pip install tomli")

def load_config():
        """Loading TOML configure file"""
        config_file = Path("~/.ephonlab.toml").expanduser()
        if not config_file.exists():
            raise FileNotFoundError(f"file not exist: {config_file}")
        
        with open(config_file, 'rb') as f:  
            return tomllib.load(f)

class Config:
    def __init__(self, 
                 job_name: str = 'elphonlab',
                 num_cores: int = 40,
                 cal_node: str = 'node01',
                 ):
        self._job_name = job_name
        self._num_cores = num_cores
        self._cal_node = cal_node
        self.config_file = Path("~/.ephonlab.toml").expanduser()
        self.data = self._load()
        self.params = {'job_name': self._job_name, 
                      'num_cores': self._num_cores, 
                      'cal_nodes': self._cal_node}
        self.softpath = self.data['software_paths']
        self.pseudo = self.data['pseudo_paths']
        self.cal_order = self.data['calculations']['cal_order']
        self._soft = []
        self._order = []

    # get job_name
    @property
    def job_name(self):
        # get the defined job name
        return self._job_name
    @job_name.setter
    def job_name(self, job_name):
        self._job_name = job_name

    # get total cores
    @property
    def num_cores(self):
        # get the defined total core number
        return self._num_cores
    @num_cores.setter
    def num_cores(self, num_cores):
        self._num_cores = num_cores

    # get the calculation nodes
    @property
    def cal_node(self):
        # get the defined total core number
        return self._cal_node
    @cal_node.setter
    def cal_node(self, cal_node):
        self._cal_node = cal_node      

    # get software
    @property
    def soft(self):
        # get the defined job name
        return self._soft
    @soft.setter
    def soft(self, val):
        if isinstance(val, (list, tuple)):
            self._soft.extend(val)
        else:
            self._soft.append(val)

    # get submit orders
    @property
    def order(self):
        # get the defined job name
        return self._order
    @order.setter
    def order(self, val):
        if isinstance(val, (list, tuple)):
            self._order.extend(val)
        else:
            self._order.append(val)

    def _load(self):
        """Loading TOML configure file"""
        if not self.config_file.exists():
            raise FileNotFoundError(f"file not exist: {self.config_file}")
        
        with open(self.config_file, 'rb') as f:  
            return tomllib.load(f)
    
    def get_sub_prefix(self):
        """generate configure file"""

        script = self.data['submit_scripts']['template']
        
        for key, value in self.params.items():
            script = script.replace(f'{{{key}}}', str(value))
        
        return script
    
    def save(self, filename="submit.sh"):
        """save submit file"""
        script = self.get_sub_prefix()
        split_str ="#######################################################"
        for i in range(len(self.soft)):
            script= script + f"export PATH={self.soft[i]}:$PATH" + '\n'
            # script[f'soft{i}'] = "Test"
        script = script + '\n\necho -n "start time  " > time \ndate >> time'
        script = script + f'\n{split_str}\n'
        for j in range(len(self.order)):
            script= script + self.order[j] + '\n'
        script = script + f'{split_str}\n'
        # save to file
        with open(filename, 'w') as f:
            f.write(script)
            f.write('echo -n "End time  " >> time\ndate >> time')
        os.chmod(filename, 0o755)
        print(f"Submit script saved to : {filename}")

# if __name__ == '__main__':
#     config = Config()
#     data = load_config()
#     softs = [data['software_paths']['QE'], data['software_paths']['third_order']]
#     orders = [f"{config.cal_order} {40} {config.softpath['QE']}/pw.x < scf.in > scf.log", 
#              f"{config.cal_order} {40} {config.softpath['QE']}/pw.x < nscf.in > nscf.log"]
#     # soft1
#     config.soft = softs
#     config.order = orders

#     config.save(Path.cwd() / 'submit.sh')
