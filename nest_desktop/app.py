# encoding: utf8
import http.server
import os
import socketserver
import sys
from subprocess import check_output

import psutil
import rich_click as click
from rich.console import Console
from rich.table import Table

NEST_DESKTOP_HOST = os.environ.get("NEST_DESKTOP_HOST", "127.0.0.1")
NEST_DESKTOP_PORT = os.environ.get("NEST_DESKTOP_PORT", 54286)
console = Console()


def pid() -> int:
    "Return nest_desktop.app process identifier (PID)."
    return int(check_output('pgrep -f "python3 -m nest_desktop.app ${HOST} ${PORT}"', shell=True, encoding="utf8"))


@click.group()
def cli():
    "Manage NEST Desktop processes."


@cli.command("version")
def version():
    from . import __version__

    print(__version__)


@cli.command("pid")
def print_pid():
    print(pid())


@cli.command("serve")
@click.argument("host")
@click.argument("port")
def serve(host: str = NEST_DESKTOP_HOST, port: int = NEST_DESKTOP_PORT):
    "Start a simple http server to hand out the app."
    web_dir = os.path.join(os.path.dirname(__file__), "app")
    os.chdir(web_dir)

    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer((host, port), Handler) as httpd:
        httpd.serve_forever()


@cli.command("start")
def start():
    "Start a new server instance for NEST Desktop"
    # Starts NEST Desktop (if no instance is already running).
    # Formerly:
    #   if pid > /dev/null; then
    #     echo "NEST Desktop is already running at http://${HOST}:${PORT}."
    #   else
    #     echo "NEST Desktop is now running at http://${HOST}:${PORT}."
    #     echo "Use CTRL + C to stop this service."
    #     python3 -m nest_desktop.app ${HOST} ${PORT}
    #   fi


@cli.command("status")
def status():
    "Display the status of NEST Desktop"
    # Returns the status of NEST Desktop instances started with the Python webserver
    # by giving the IP addresses and ports.
    # Formerly:
    #  PS_AUX="$(ps aux | grep "[p]ython3 -m nest_desktop.app")"
    #  PS_CMD="$(echo ${PS_AUX} | awk '{ for(i=1;i<=NF;i++) {if ( i >= 11 ) printf $i" "}; printf "\n" }')"
    #  printf "HTTP-SOCKETS (PYTHON)\n---------------------\n"
    #  if [ -z "${PS_CMD}" ]; then
    #    echo "[no running instance found]"
    #  else
    #    echo "${PS_CMD}" | awk '{ for(i=1;i<=NF;i++) {if ( i == 4 || i == 5 ) printf $i" "}; printf "\n" }'
    #  fi;
    fields = ["pid", "username", "name", "cmdline"]

    table = Table(*fields, title="Processes")
    for proc in psutil.process_iter(fields):
        if proc.status() == "zombie":
            continue
        table.add_row(str(proc.pid), str(proc.username()), str(proc.name()), " ".join(proc.cmdline()))
    console.print(table)


@cli.command("stop")
def stop():
    "Stop a server instance running on <HOST>:<PORT>"
    # Tries to stop a running NEST Desktop instance.
    # Formerly:
    #  if pid > /dev/null; then
    #    kill "$(pid)"
    #    echo "NEST Desktop running at http://${HOST}:${PORT} has just stopped."
    #  else
    #    echo "NEST Desktop is not running at http://${HOST}:${PORT}."
    #    false
    #  fi


@cli.command("restart")
def restart():
    "Restart (i.e. stop and start) a server on <HOST>:<PORT>"


@cli.command("launch-all")
def launch_all():
    "Start all backends, and servers."
    # Formerly:
    #   export NESTML_MODULES_PATH="${NESTML_MODULES_PATH:-/tmp/nestmlmodules}"
    #   export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${NESTML_MODULES_PATH}

    #   export NEST_SERVER_DISABLE_AUTH=1
    #   export NEST_SERVER_DISABLE_RESTRICTION=1
    #   export NEST_SERVER_ENABLE_EXEC_CALL=1
    #   export NEST_SERVER_MODULES="import nest; import numpy; import numpy as np"

    #   # Start NEST Server as daemon
    #   export NEST_SERVER_DAEMON=1
    #   nest-server start

    #   if ! command -v nestml-server 2>&1 >/dev/null
    #   then
    #       # Start NESTML Server as daemon
    #       export NESTML_SERVER_DAEMON=1
    #       nestml-server start
    #   fi

    #   # Start NEST Desktop
    #   nest-desktop --no-sandbox

    #   # Stop NEST Server
    #   nest-server stop

    #   if ! command -v nestml-server 2>&1 >/dev/null
    #   then
    #       # Stop NESTML Server
    #       nestml-server stop
    #   fi
