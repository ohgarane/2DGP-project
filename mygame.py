import platform
import pico2d
import os
import game_framework
import start_state

game_framework.run(start_state)

if platform.architecture()[0] == '32bit':
    os.environ["PYSDL2_DLL_PATH"] = "./SDL2/X86"
else:
    os.environ["PYSDL2_DLL_PATH"] = "./SDL2/X64"

