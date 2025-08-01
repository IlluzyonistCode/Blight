import socket
import threading
import subprocess
import psutil
import pyscreenshot
import shlex
import signal
import io
import os
import sys
import platform
import time
import base64
import tabulate
import Xlib
from datetime import datetime

try:
    from pynput.keyboard import Listener

    HAVE_X = True
except Xlib.error.DisplayNameError:
    HAVE_X = False
