# -*- coding: utf-8 -*-
import os

from maya import cmds

from . import info, core, prompts, openai_utils, voice, exec_code, settings
from importlib import reload
reload(info)
reload(core)
reload(prompts)
reload(openai_utils)
reload(voice)
reload(exec_code)
reload(settings)

def run():
    try:
        os.environ['OPENAI_API_KEY']
    except KeyError:
        cmds.error('The environment variable "OPENAI_API_KEY" is not set.')
    else:
        core.showUI()