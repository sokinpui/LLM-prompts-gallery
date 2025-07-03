# update_neovim.py
import os
import re
import sys

import pynvim

# --- Configuration ---
SOURCE_FILE = "tmp.txt"

# --- Regex patterns ---
FILE_BLOCK_REGEX = re.compile(
    r"```[a-z]*\n(?P<content_with_header>(?:#|//|/\*)\s*.*?\n.*?)\n```", re.DOTALL
)
PATH_EXTRACT_REGEX = re.compile(r"^(?:#|//|/\*)\s*(?P<path>.*?)\s*(?:\*/)?$")


def get_nvim_instance(socket_path):
    """Connects to the Neovim instance via its socket."""
    try:
        return pynvim.attach("socket", path=socket_path)
    except Exception as e:
        print(
            f"Error connecting to Neovim socket at '{socket_path}': {e}",
            file=sys.stderr,
        )
        print(
            "Hint: Is Neovim running with `nvim --listen /tmp/nvim.sock`?",
            file=sys.stderr,
        )
        return None


def find_or_open_buffer(nvim, file_path):
    """Finds the buffer for the given file_path, opening it if it necessary."""
    abs_file_path = os.path.abspath(file_path)
    for buf in nvim.api.list_bufs():
        buf_name = nvim.api.buf_get_name(buf)
        if buf_name == abs_file_path:
            return buf
    print(f"  -> File not open. Creating new buffer for '{file_path}'...")
    escaped_path = nvim.api.call_function("fnameescape", [abs_file_path])
    nvim.command(f"edit {escaped_path}")
    return nvim.api.get_current_buf()


def update_neovim_buffers(nvim, should_save=False):
    """
    Reads a source file, parses it for file blocks, and updates the corresponding
    buffers inside the running Neovim instance.
    """
    print(f"--- Starting Neovim buffer update from '{SOURCE_FILE}' ---")
    try:
        with open(SOURCE_FILE, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: Source file '{SOURCE_FILE}' not found.", file=sys.stderr)
        return

    matches = FILE_BLOCK_REGEX.finditer(content)
    updated_count = 0
    for match in matches:
        file_content_with_header = match.group("content_with_header")
        first_line = file_content_with_header.split("\n", 1)[0].strip()
        path_match = PATH_EXTRACT_REGEX.search(first_line)
        if not path_match:
            continue
        file_path = path_match.group("path").strip()
        print(f"Processing: {file_path}")
        target_buffer = find_or_open_buffer(nvim, file_path)
        if not target_buffer:
            print(
                f"  -> Error: Could not find or create a buffer for this file.",
                file=sys.stderr,
            )
            continue
        content_lines = file_content_with_header.split("\n")
        try:
            nvim.api.buf_set_lines(target_buffer, 0, -1, True, content_lines)
            print(f"  -> Successfully updated buffer {target_buffer.handle}.")
            updated_count += 1
        except pynvim.NvimError as e:
            print(f"  -> Neovim API Error updating buffer: {e}", file=sys.stderr)

    print(f"\n--- Buffer update complete ---")
    print(f"Successfully updated {updated_count} buffer(s) in Neovim.")

    if should_save and updated_count > 0:
        try:
            print("\nSaving all modified buffers (without running autocommands)...")
            nvim.command("noa wa!")
            print("Save complete.")
        except pynvim.NvimError as e:
            print(f"  -> Neovim API Error saving buffers: {e}", file=sys.stderr)


if __name__ == "__main__":
    # This script was previously named 'insert_to_file.py' in the screenshot,
    # but the logic remains the same.
    args = sys.argv[1:]
    socket = None
    save_flag = "--save" in args

    for arg in args:
        if arg != "--save":
            socket = arg
            break

    if not socket:
        socket = os.environ.get("NVIM_LISTEN_ADDRESS")

    if not socket:
        print(
            "Usage: python update_neovim.py <neovim_socket_path> [--save]",
            file=sys.stderr,
        )
        print("Or set the NVIM_LISTEN_ADDRESS environment variable.", file=sys.stderr)
        sys.exit(1)

    nvim_instance = get_nvim_instance(socket)
    if nvim_instance:
        update_neovim_buffers(nvim_instance, should_save=save_flag)
