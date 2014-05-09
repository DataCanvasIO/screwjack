
ScrewJack
=========

ScrewJack is a tiny command line tool for manipulating modules.

Installation
------------

Install directly by pip:

```sh
pip install -U screwjack
```

Or, you can use the latest version:

```sh
git clone http://github.com/DataCanvasIO/screwjack.git screwjack.git
cd screwjack.git
pip install -r requirements.txt
./bin/screwjack --help
```

Usage
-----

### Initialize a module

You can initialize a module interactively:

```
export DATACANVAS_USERNAME=your_username
screwjack init
```

Or, you can create a module in single command:

```
screwjack init --name=Your_Module_Name --description="Some nice description" --version=0.1 --cmd="/usr/bin/python main.py" --base-image=ubuntu
```

Then, you will get a directory of your module(in lower case):

```
cd your_module_name
screwjack --help
```

### Add/Remove a 'Env' parameter to 'spec.json'

Add a series of env parameters:

```
screwjack env_add your_env_parameter_name another_env_parameter
```

Remove a parameter:

```
screwjack env_del your_env_parameter_name
```

### Add/Remove a 'Input'/'Output' parameter to 'spec.json'

Add a series of 'Input'/'Output' parameters:

```
screwjack input_add your_env_parameter_name another_env_parameter
```

Remove a 'Input'/'Output' parameter:

```
screwjack input_del your_env_parameter_name
```

### Run module in local/docker mode

Run current module in local mode:

```
screwjack run local --PARAM1=1 --PARAM2=2
```

Alternative, you can run in docker:

```
screwjack run docker --PARAM1=1 --PARAM2=2
```

### Package and submit module

Package current module into a tar:

```
screwjack package
```

After that, you can submit your module to spec_server:

```
screwjack submit
```

About
-----

ScrewJack is licensed under BSD (3-Clause) License, see LICENSE file for detail. Comments and contribution are welcome.
