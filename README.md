
```
 ######        #     #        #     #
#              #   #         #     #
#               # #          #     #
 #####           #           #######
      #         # #          #     #
      #        #   #         #     #
 ######       #     #        #     #
```

# SSH Remote Connection Tool

A simple Python GUI that connects to remote servers via SSH, executes commands, and shows the output in a clean interface. Built with Tkinter and Paramiko.

## Features

- Host, port, username, and password input
- Connection status indicators (Connected/Failed/Disconnected)
- Execute remote commands and view stdout/stderr
- Safe threading for non-blocking UI
- Disconnect button to close the session

## Prerequisites

- Python 3.8+
- Paramiko library

## Installation

1. Clone or download this repository.
2. Install dependencies:
   ```bash
   pip install paramiko

   (Optional) On macOS with Python from python.org, you may need:

```
python3 -m pip install --upgrade pip
```
Usage
Run the app:

bash
python ssh_gui_tool.py
Enter remote server details (host, port, username, password).

Click "Connect". Check status label for feedback.

Enter a command and click "Execute".

Click "Disconnect" to close the SSH session.

Notes
For better security, prefer key-based authentication. You can extend connect_ssh() to use pkey=paramiko.RSAKey.from_private_key_file("~/.ssh/id_rsa").

The app uses AutoAddPolicy to accept unknown host keys. In production, consider managing known hosts explicitly.

Command output is appended; clear the text area manually if needed.

Example
Connect to a Linux host and run:

bash
uname -a
whoami
ls -la
Screenshot
Add a screenshot named screenshot.png in the project root and reference it here:
[Looks like the result wasn't safe to show. Let's switch things up and try something else!]

License
MIT
