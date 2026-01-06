#!/usr/bin/env python3
"""
Simple API Testing Tool
- Stores token persistently
- Tests any API endpoint
- Displays results nicely formatted
"""

import json
import os
import sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode

TOKEN_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".api_token")

# Colors for terminal output
class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    END = "\033[0m"


def load_token():
    """Load saved token from file."""
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            return f.read().strip()
    return None


def save_token(token):
    """Save token to file."""
    with open(TOKEN_FILE, "w") as f:
        f.write(token)
    print(f"{Colors.GREEN}✓ Token saved!{Colors.END}")


def clear_token():
    """Clear saved token."""
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)
        print(f"{Colors.GREEN}✓ Token cleared!{Colors.END}")
    else:
        print(f"{Colors.YELLOW}No token to clear.{Colors.END}")


def format_json(data):
    """Pretty format JSON with colors."""
    formatted = json.dumps(data, indent=2, sort_keys=False)
    return formatted


def format_headers(headers):
    """Format response headers nicely."""
    lines = []
    for key, value in headers.items():
        lines.append(f"  {Colors.CYAN}{key}{Colors.END}: {value}")
    return "\n".join(lines)


def make_request(url, method="GET", token=None, data=None, headers=None):
    """Make an HTTP request and return the response."""
    req_headers = {"Content-Type": "application/json"}

    if token:
        req_headers["Authorization"] = f"Bearer {token}"

    if headers:
        req_headers.update(headers)

    body = None
    if data:
        body = json.dumps(data).encode("utf-8")

    req = Request(url, data=body, headers=req_headers, method=method)

    try:
        with urlopen(req, timeout=30) as response:
            status = response.status
            resp_headers = dict(response.headers)
            content = response.read().decode("utf-8")
            return status, resp_headers, content, None
    except HTTPError as e:
        content = e.read().decode("utf-8") if e.fp else ""
        return e.code, dict(e.headers) if e.headers else {}, content, str(e)
    except URLError as e:
        return None, {}, "", str(e.reason)
    except Exception as e:
        return None, {}, "", str(e)


def display_response(status, headers, content, error):
    """Display the API response nicely."""
    print()
    print(f"{Colors.BOLD}{'='*60}{Colors.END}")

    # Status
    if status:
        if 200 <= status < 300:
            color = Colors.GREEN
        elif 300 <= status < 400:
            color = Colors.YELLOW
        else:
            color = Colors.RED
        print(f"{Colors.BOLD}Status:{Colors.END} {color}{status}{Colors.END}")
    else:
        print(f"{Colors.BOLD}Status:{Colors.END} {Colors.RED}Failed - {error}{Colors.END}")

    print(f"{Colors.BOLD}{'='*60}{Colors.END}")

    # Headers
    if headers:
        print(f"\n{Colors.BOLD}Response Headers:{Colors.END}")
        print(format_headers(headers))

    # Body
    print(f"\n{Colors.BOLD}Response Body:{Colors.END}")
    if content:
        try:
            parsed = json.loads(content)
            print(format_json(parsed))
        except json.JSONDecodeError:
            print(content[:2000] if len(content) > 2000 else content)
    else:
        print(f"{Colors.YELLOW}(empty response){Colors.END}")

    print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")


def interactive_mode():
    """Run in interactive mode."""
    token = load_token()

    print(f"\n{Colors.BOLD}{Colors.BLUE}╔══════════════════════════════════════╗{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}║       API Testing Tool v1.0          ║{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}╚══════════════════════════════════════╝{Colors.END}\n")

    if token:
        masked = token[:8] + "..." + token[-4:] if len(token) > 12 else "****"
        print(f"{Colors.GREEN}✓ Token loaded:{Colors.END} {masked}")
    else:
        print(f"{Colors.YELLOW}No token set. Use 'token <your-token>' to set one.{Colors.END}")

    print(f"""
{Colors.BOLD}Commands:{Colors.END}
  {Colors.CYAN}token <value>{Colors.END}    - Set Bearer token
  {Colors.CYAN}token{Colors.END}            - Show current token
  {Colors.CYAN}clear{Colors.END}            - Clear saved token
  {Colors.CYAN}GET <url>{Colors.END}        - Make GET request
  {Colors.CYAN}POST <url>{Colors.END}       - Make POST request (will prompt for body)
  {Colors.CYAN}PUT <url>{Colors.END}        - Make PUT request (will prompt for body)
  {Colors.CYAN}DELETE <url>{Colors.END}     - Make DELETE request
  {Colors.CYAN}PATCH <url>{Colors.END}      - Make PATCH request (will prompt for body)
  {Colors.CYAN}headers{Colors.END}          - Toggle showing response headers
  {Colors.CYAN}help{Colors.END}             - Show this help
  {Colors.CYAN}quit{Colors.END}             - Exit
""")

    show_headers = True

    while True:
        try:
            cmd = input(f"\n{Colors.BOLD}api>{Colors.END} ").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{Colors.YELLOW}Goodbye!{Colors.END}")
            break

        if not cmd:
            continue

        parts = cmd.split(maxsplit=1)
        action = parts[0].upper()

        if action == "QUIT" or action == "EXIT" or action == "Q":
            print(f"{Colors.YELLOW}Goodbye!{Colors.END}")
            break

        elif action == "HELP" or action == "H" or action == "?":
            print(f"""
{Colors.BOLD}Commands:{Colors.END}
  {Colors.CYAN}token <value>{Colors.END}    - Set Bearer token
  {Colors.CYAN}token{Colors.END}            - Show current token
  {Colors.CYAN}clear{Colors.END}            - Clear saved token
  {Colors.CYAN}GET <url>{Colors.END}        - Make GET request
  {Colors.CYAN}POST <url>{Colors.END}       - Make POST request
  {Colors.CYAN}PUT <url>{Colors.END}        - Make PUT request
  {Colors.CYAN}DELETE <url>{Colors.END}     - Make DELETE request
  {Colors.CYAN}PATCH <url>{Colors.END}      - Make PATCH request
  {Colors.CYAN}headers{Colors.END}          - Toggle showing response headers
  {Colors.CYAN}quit{Colors.END}             - Exit
""")

        elif action == "TOKEN":
            if len(parts) > 1:
                token = parts[1]
                save_token(token)
            else:
                if token:
                    masked = token[:8] + "..." + token[-4:] if len(token) > 12 else token
                    print(f"{Colors.GREEN}Current token:{Colors.END} {masked}")
                else:
                    print(f"{Colors.YELLOW}No token set.{Colors.END}")

        elif action == "CLEAR":
            clear_token()
            token = None

        elif action == "HEADERS":
            show_headers = not show_headers
            state = "ON" if show_headers else "OFF"
            print(f"{Colors.GREEN}Headers display: {state}{Colors.END}")

        elif action in ["GET", "POST", "PUT", "DELETE", "PATCH"]:
            if len(parts) < 2:
                print(f"{Colors.RED}Please provide a URL{Colors.END}")
                continue

            url = parts[1]

            # Ensure URL has protocol
            if not url.startswith("http://") and not url.startswith("https://"):
                url = "https://" + url

            data = None
            if action in ["POST", "PUT", "PATCH"]:
                print(f"{Colors.CYAN}Enter JSON body (or press Enter for empty):{Colors.END}")
                body_input = input().strip()
                if body_input:
                    try:
                        data = json.loads(body_input)
                    except json.JSONDecodeError as e:
                        print(f"{Colors.RED}Invalid JSON: {e}{Colors.END}")
                        continue

            print(f"\n{Colors.BLUE}→ {action} {url}{Colors.END}")

            status, headers, content, error = make_request(url, action, token, data)

            if not show_headers:
                headers = {}

            display_response(status, headers, content, error)

        else:
            # Try to treat as a URL (default GET)
            url = cmd
            if url.startswith("http://") or url.startswith("https://") or "." in url:
                if not url.startswith("http"):
                    url = "https://" + url
                print(f"\n{Colors.BLUE}→ GET {url}{Colors.END}")
                status, headers, content, error = make_request(url, "GET", token)
                if not show_headers:
                    headers = {}
                display_response(status, headers, content, error)
            else:
                print(f"{Colors.RED}Unknown command. Type 'help' for available commands.{Colors.END}")


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        # Command line mode
        if sys.argv[1] == "--help" or sys.argv[1] == "-h":
            print("""
API Testing Tool

Usage:
  python api_tester.py                    # Interactive mode
  python api_tester.py <url>              # Quick GET request
  python api_tester.py --set-token <tok>  # Set token
  python api_tester.py --clear-token      # Clear token

Interactive mode provides full functionality.
""")
            return

        if sys.argv[1] == "--set-token" and len(sys.argv) > 2:
            save_token(sys.argv[2])
            return

        if sys.argv[1] == "--clear-token":
            clear_token()
            return

        # Quick GET request
        url = sys.argv[1]
        if not url.startswith("http"):
            url = "https://" + url

        token = load_token()
        print(f"{Colors.BLUE}→ GET {url}{Colors.END}")
        status, headers, content, error = make_request(url, "GET", token)
        display_response(status, headers, content, error)
    else:
        interactive_mode()


if __name__ == "__main__":
    main()
