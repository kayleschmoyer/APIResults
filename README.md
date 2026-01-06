# API Testing Tool

A simple, no-dependencies Python tool for testing APIs from the command line.

## Features

- **Token persistence** - Set your Bearer token once, it remembers it
- **Any HTTP method** - GET, POST, PUT, DELETE, PATCH
- **Pretty JSON output** - Formatted and colored responses
- **No external dependencies** - Uses only Python standard library

## Usage

### Interactive Mode (Recommended)

```bash
python api_tester.py
```

This opens an interactive shell where you can:

```
api> token sk-your-api-token-here     # Set your token (saved to file)
api> GET https://api.example.com/users   # Make a GET request
api> POST https://api.example.com/users  # Make POST (prompts for JSON body)
api> headers                             # Toggle header display
api> quit                                # Exit
```

### Quick Commands

```bash
# Quick GET request
python api_tester.py https://api.example.com/endpoint

# Set token from command line
python api_tester.py --set-token your-token-here

# Clear saved token
python api_tester.py --clear-token
```

## Commands

| Command | Description |
|---------|-------------|
| `token <value>` | Set and save Bearer token |
| `token` | Show current token (masked) |
| `clear` | Clear saved token |
| `GET <url>` | Make GET request |
| `POST <url>` | Make POST request (prompts for body) |
| `PUT <url>` | Make PUT request (prompts for body) |
| `DELETE <url>` | Make DELETE request |
| `PATCH <url>` | Make PATCH request (prompts for body) |
| `headers` | Toggle response headers display |
| `help` | Show help |
| `quit` | Exit |

## Example Session

```
$ python api_tester.py

╔══════════════════════════════════════╗
║       API Testing Tool v1.0          ║
╚══════════════════════════════════════╝

No token set. Use 'token <your-token>' to set one.

api> token myapikey123456789

✓ Token saved!

api> GET https://jsonplaceholder.typicode.com/posts/1

→ GET https://jsonplaceholder.typicode.com/posts/1

============================================================
Status: 200
============================================================

Response Body:
{
  "userId": 1,
  "id": 1,
  "title": "example post",
  "body": "example body content"
}

============================================================
```

## Token Storage

Your token is saved to `.api_token` in the same directory as the script. Add this file to `.gitignore` if you're version controlling the directory.
