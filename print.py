import sys
import os
import subprocess
import glob

# Set UTF-8 for stdout
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def run_command(command):
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if result.returncode != 0:
        print(f"\n!!! ERROR during execution of: {command} !!!")
        if result.stdout:
            print(f"Standard Output:\n{result.stdout}")
        if result.stderr:
            print(f"Error Output:\n{result.stderr}")
        return False
    else:
        if result.stdout:
            print(result.stdout)
        return True

def main():
    print("--- Starting Full Book Generation Flow ---")

    # 1. Run Scribus generation
    print("\n[1/3] Generating Scribus files...")
    run_command(f'"{sys.executable}" scribus_gen.py')

    # 2. Run Typst generation (creates .typ files for A5 and B6)
    print("\n[2/3] Generating Typst source files...")
    run_command(f'"{sys.executable}" typst_gen.py')

    # 3. Generate PDFs
    print("\n[3/3] Compiling PDFs...")
    # These rely on generatePdf.py being present
    # Primary output: Slim format (110x180mm)
    if not run_command(f'"{sys.executable}" generatePdf.py Blok.typ'):
        print("\n[!] Stopping: Failed to generate Blok.typ")
        return

    # Secondary output: B6 format
    if not run_command(f'"{sys.executable}" generatePdf.py Blok_B6.typ'):
        print("\n[!] Stopping: Failed to generate Blok_B6.typ")
        return

    # Rename Blok.pdf to Blok_Slim.pdf for clarity
    if os.path.exists("Blok.pdf"):
        if os.path.exists("Blok_Slim.pdf"):
            os.remove("Blok_Slim.pdf")
        os.rename("Blok.pdf", "Blok_Slim.pdf")
        print("Renamed: Blok.pdf -> Blok_Slim.pdf")

    # CLEANUP
    print("\n--- Cleaning up temporary files ---")
    
    # Files to remove as requested
    to_delete = [
        "Blok.typ", "Blok_B6.typ", "Blok_A5.typ",
        "export_config_130x200.json", "export_config_110x180.json",
        "chaps.txt", "all_imgs.txt", "check_images.py", "test.py", "test2.py",
        "Blok_130x200.pdf", "Blok_110x180.pdf", "Blok_130x200.typ", "Blok_110x180.typ"
    ]
    
    for f in to_delete:
        if os.path.exists(f):
            try:
                os.remove(f)
                print(f"Deleted: {f}")
            except Exception as e:
                print(f"Could not delete {f}: {e}")

    # Remove any stray logs
    for log in glob.glob("*.log"):
        os.remove(log)
        print(f"Deleted log: {log}")

    print("\n--- DONE! Your print-ready PDFs are ready: Blok_Slim.pdf and Blok_B6.pdf ---")

if __name__ == "__main__":
    main()
