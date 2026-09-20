import subprocess
import sys
import os

# Set UTF-8 for stdout to prevent crashes on non-ASCII characters in Windows CMD/PS
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def generate_pdf(typ_file):
    if not os.path.exists(typ_file):
        print(f"Error: File '{typ_file}' not found.")
        return

    # Find the tinymist binary dynamically in the extensions directory
    extensions_dir = os.path.expanduser(r"~\.antigravity\extensions")
    tinymist_path = "typst"  # fallback
    
    if os.path.exists(extensions_dir):
        # Look for folders starting with myriad-dreamin.tinymist
        tinymist_folders = [f for f in os.listdir(extensions_dir) if f.startswith("myriad-dreamin.tinymist")]
        if tinymist_folders:
            # Pick the latest version (lexicographically)
            latest_folder = sorted(tinymist_folders)[-1]
            executable = os.path.join(extensions_dir, latest_folder, "out", "tinymist.exe")
            print(f"Looking for tinymist in: {executable}")
            if os.path.exists(executable):
                tinymist_path = executable
                print(f"Found tinymist: {tinymist_path}")
            else:
                print(f"Warning: Found tinymist folder {latest_folder} but {executable} is missing.")
        else:
            print("Warning: No myriad-dreamin.tinymist extension folder found.")
    else:
        print(f"Warning: Extensions directory {extensions_dir} not found.")

    # If still using the default fallback, try to find typst.exe in winget packages
    if tinymist_path == "typst":
        winget_base = os.path.expanduser(r"~\AppData\Local\Microsoft\WinGet\Packages")
        if os.path.exists(winget_base):
            for pkg_dir in os.listdir(winget_base):
                if pkg_dir.lower().startswith("typst.typst"):
                    candidate = os.path.join(winget_base, pkg_dir)
                    for root, _, files in os.walk(candidate):
                        if "typst.exe" in files:
                            tinymist_path = os.path.join(root, "typst.exe")
                            print(f"Found typst via winget: {tinymist_path}")
                            break
                if tinymist_path != "typst":
                    break

    output_pdf = typ_file.replace(".typ", ".pdf")
    
    print(f"Compiling {typ_file} to {output_pdf}...")
    
    # Use shell=True for better character handling on Windows
    cmd = f'"{tinymist_path}" compile "{typ_file}" "{output_pdf}"'
    
    try:
        # Use encoding='utf-8' and replace errors for robustness
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8', errors='replace')
        
        if result.returncode == 0:
            print(f"Success! Generated: {output_pdf}")
        else:
            print("Error during compilation:")
            print(result.stderr)
            print(f"Exit code: {result.returncode}")
            sys.exit(1)
            
    except Exception as e:
        # Repr avoids encoding issues when printing the exception itself
        print(f"Failed to execute tinymist: {repr(e)}")
        print("Make sure Tinymist is installed or the path in this script is correct.")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generatePdf.py <filename.typ>")
    else:
        generate_pdf(sys.argv[1])
