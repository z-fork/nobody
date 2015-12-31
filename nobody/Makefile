VENV = venv

PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

PIP_MIRROR = https://pypi.mirrors.ustc.edu.cn/simple

# `w` stands for `wipe`
#PIP_INSTALL = $(PIP) install --quiet --exists-action=w
PIP_INSTALL = $(PIP) install

deps:
	@$(PIP_INSTALL) -i $(PIP_MIRROR) -r requirements.txt

venv:
	@virtualenv $(VENV) --prompt '<venv:nobody>'
	@$(PIP_INSTALL) -i $(PIP_MIRROR) -U pip setuptools

