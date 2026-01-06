import tkinter as tk
from tkinter import messagebox, scrolledtext
import paramiko
import threading

class SSHClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SSH Remote Connection Tool")
        self.root.geometry("720x480")

        # Host
        tk.Label(root, text="Host:").grid(row=0, column=0, sticky="e", padx=8, pady=6)
        self.host_entry = tk.Entry(root, width=32)
        self.host_entry.grid(row=0, column=1, padx=5, pady=6)

        # Port
        tk.Label(root, text="Port:").grid(row=1, column=0, sticky="e", padx=8, pady=6)
        self.port_entry = tk.Entry(root, width=32)
        self.port_entry.insert(0, "22")
        self.port_entry.grid(row=1, column=1, padx=5, pady=6)

        # Username
        tk.Label(root, text="Username:").grid(row=2, column=0, sticky="e", padx=8, pady=6)
        self.username_entry = tk.Entry(root, width=32)
        self.username_entry.grid(row=2, column=1, padx=5, pady=6)

        # Password
        tk.Label(root, text="Password:").grid(row=3, column=0, sticky="e", padx=8, pady=6)
        self.password_entry = tk.Entry(root, show="*", width=32)
        self.password_entry.grid(row=3, column=1, padx=5, pady=6)

        # Connect Button + Status
        self.connect_button = tk.Button(root, text="Connect", command=self.connect_ssh)
        self.connect_button.grid(row=4, column=1, pady=8, sticky="w")
        self.status_label = tk.Label(root, text="Status: Disconnected", fg="gray")
        self.status_label.grid(row=4, column=1, pady=8, sticky="e")

        # Command Entry
        tk.Label(root, text="Command:").grid(row=5, column=0, sticky="e", padx=8, pady=6)
        self.command_entry = tk.Entry(root, width=50)
        self.command_entry.grid(row=5, column=1, padx=5, pady=6, sticky="w")

        # Execute + Disconnect Buttons
        self.exec_button = tk.Button(root, text="Execute", command=self.execute_command)
        self.exec_button.grid(row=6, column=1, pady=6, sticky="w")
        self.disconnect_button = tk.Button(root, text="Disconnect", command=self.disconnect)
        self.disconnect_button.grid(row=6, column=1, pady=6, sticky="e")

        # Output Area
        self.output_area = scrolledtext.ScrolledText(root, width=80, height=16)
        self.output_area.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

        self.ssh_client = None

    def set_status(self, text, color="gray"):
        self.status_label.config(text=f"Status: {text}", fg=color)

    def connect_ssh(self):
        host = self.host_entry.get().strip()
        port = self.port_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not host or not port or not username:
            messagebox.showwarning("Missing Info", "Please fill in host, port, and username.")
            return

        try:
            port = int(port)
        except ValueError:
            messagebox.showerror("Invalid Port", "Port must be an integer.")
            return

        self.set_status("Connecting...", "orange")
        self.connect_button.config(state="disabled")

        def do_connect():
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                client.connect(hostname=host, port=port, username=username, password=password, timeout=10)
                self.ssh_client = client
                self.set_status("Connected", "green")
                messagebox.showinfo("Connection", "SSH connection successful.")
            except Exception as e:
                self.ssh_client = None
                self.set_status("Failed", "red")
                messagebox.showerror("Connection Failed", str(e))
            finally:
                self.connect_button.config(state="normal")

        threading.Thread(target=do_connect, daemon=True).start()

    def execute_command(self):
        if self.ssh_client is None:
            messagebox.showwarning("Not Connected", "Please connect to a server first.")
            return

        command = self.command_entry.get().strip()
        if not command:
            messagebox.showwarning("Empty Command", "Please enter a command to execute.")
            return

        self.output_area.insert(tk.END, f"$ {command}\n")
        self.exec_button.config(state="disabled")
        self.set_status("Running command...", "orange")

        def do_exec():
            try:
                stdin, stdout, stderr = self.ssh_client.exec_command(command)
                output = stdout.read().decode(errors="ignore")
                error = stderr.read().decode(errors="ignore")
                if output:
                    self.output_area.insert(tk.END, output + "\n")
                if error:
                    self.output_area.insert(tk.END, "[stderr] " + error + "\n")
            except Exception as e:
                self.output_area.insert(tk.END, f"Error executing command: {str(e)}\n")
            finally:
                self.exec_button.config(state="normal")
                self.set_status("Connected", "green")

        threading.Thread(target=do_exec, daemon=True).start()

    def disconnect(self):
        if self.ssh_client:
            try:
                self.ssh_client.close()
            except Exception:
                pass
            finally:
                self.ssh_client = None
        self.set_status("Disconnected", "gray")
        self.output_area.insert(tk.END, "Disconnected from server.\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = SSHClientGUI(root)
    root.mainloop()
