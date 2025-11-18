import socket
import sys

class SmtpClient:
    def __init__(self, server_ip, port=25, timeout=10):
        self.server_ip = server_ip
        self.port = port
        self.timeout = timeout
        self.socket = None

    def _connect_socket(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(self.timeout)
            print(f"[*] Connecting to {self.server_ip}:{self.port}...")
            self.socket.connect((self.server_ip, self.port))
            response = self._get_response()
            if not response.startswith('220'):
                raise ConnectionError(f"Server did not send 220 greeting. Received: {response.strip()}")
            print(f"[+] Connected. Server says: {response.strip()}")
        except socket.timeout:
            raise ConnectionError(f"Connection to {self.server_ip}:{self.port} timed out.")
        except socket.error as e:
            raise ConnectionError(f"Could not connect to {self.server_ip}:{self.port}. Error: {e}")

    def _send_command(self, command):
        print(f"[Client] -> {command.strip()}")
        self.socket.sendall(command.encode('utf-8'))
        return self._get_response()

    def _get_response(self):
        try:
            response = self.socket.recv(4096).decode('utf-8')
            print(f"[Server] <- {response.strip()}")
            return response
        except socket.timeout:
            raise TimeoutError("Server did not respond in time.")

    def send_email(self, ehlo_domain, from_address, to_address, subject, body, is_html=False):
        try:
            self._connect_socket()

            response = self._send_command(f'EHLO {ehlo_domain}\r\n')
            if not response.startswith('250'):
                raise RuntimeError(f"EHLO failed. Server responded: {response.strip()}")
            
            response = self._send_command(f'MAIL FROM:<{from_address}>\r\n')
            if not response.startswith('250'):
                raise RuntimeError(f"MAIL FROM failed. Server responded: {response.strip()}")

            response = self._send_command(f'RCPT TO:<{to_address}>\r\n')
            if not response.startswith('250'):
                raise RuntimeError(f"RCPT TO failed. Server responded: {response.strip()}")

            response = self._send_command('DATA\r\n')
            if not response.startswith('354'):
                raise RuntimeError(f"DATA command failed. Server responded: {response.strip()}")

            headers = [
                f"From: {from_address}",
                f"To: {to_address}",
                f"Subject: {subject}",
                "MIME-Version: 1.0"
            ]

            if is_html:
                headers.append('Content-Type: text/html; charset="utf-8"')
            else:
                headers.append('Content-Type: text/plain; charset="utf-8"')
            
            email_message = "\r\n".join(headers) + f"\r\n\r\n{body}\r\n.\r\n"
            
            print("[Client] -> [Message Data with Headers]")
            self.socket.sendall(email_message.encode('utf-8'))
            
            response = self._get_response()
            if not response.startswith('250'):
                raise RuntimeError(f"Message data not accepted. Server responded: {response.strip()}")
            print("[+] Message accepted for delivery.")

            response = self._send_command('QUIT\r\n')
            if not response.startswith('221'):
                raise RuntimeError(f"QUIT failed. Server responded: {response.strip()}")
            print("[+] Session closed.")

        except (ConnectionError, TimeoutError, RuntimeError) as e:
            print(f"\n[ERROR] {e}", file=sys.stderr)
        finally:
            self.close()

    def close(self):
        if self.socket:
            print("[*] Closing socket.")
            self.socket.close()
            self.socket = None


if __name__ == "__main__":
    print("--- Simple Manual SMTP Client (HTML Support) ---")
    
    try:
        server_ip = input("Enter SMTP server IP: ")
        ehlo_domain = input("Enter EHLO domain (e.g., example.com): ")
        mail_from = input("Enter MAIL FROM address: ")
        rcpt_to = input("Enter RCPT TO address: ")
        subject = input("Enter email subject: ")
        
        is_html_input = input("Send as HTML? (y/n): ").lower()
        is_html = (is_html_input == 'y')

        if is_html:
            body = input("Enter email body (HTML format):\n")
        else:
            body = input("Enter email body (plain text):\n")

        client = SmtpClient(server_ip)
        client.send_email(
            ehlo_domain=ehlo_domain,
            from_address=mail_from,
            to_address=rcpt_to,
            subject=subject,
            body=body,
            is_html=is_html
        )

    except KeyboardInterrupt:
        print("\n[INFO] Process cancelled by user.")
    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred: {e}", file=sys.stderr)