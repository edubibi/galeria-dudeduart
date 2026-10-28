import tarfile
import os

def create_tar(output_filename, paths):
    print(f"Creating {output_filename}...")
    with tarfile.open(output_filename, "w:gz") as tar:
        for path in paths:
            if os.path.exists(path):
                # arcname makes sure we use forward slashes and relative paths
                tar.add(path, arcname=path.replace('\\', '/'))
            else:
                print(f"Warning: {path} not found")

desktop = os.path.join(os.path.expanduser("~"), "Desktop")

# Part 1: Core
create_tar(os.path.join(desktop, "SUBIR_1_CODIGO_Y_PROMOS.tar.gz"), [
    "index.html", "main.css", "js", "cuadroteca", "visor", "bg", "promos"
])

# Part 2: Posters
create_tar(os.path.join(desktop, "SUBIR_2_POSTERS.tar.gz"), ["assets_poster"])

# Part 3: Assets Mitad 1
assets_1 = [f"assets/{f}" for f in os.listdir("assets") if f[0].lower() in "0123abcdefghijklm"]
create_tar(os.path.join(desktop, "SUBIR_3_OBRAS_MITAD_1.tar.gz"), assets_1)

# Part 4: Assets Mitad 2
assets_2 = [f"assets/{f}" for f in os.listdir("assets") if f[0].lower() in "nopqrstuvwxyz" or f.startswith("SAGA") or f.startswith("PORTADILLAS") or f in ["branding", "music", "quantum-samples", "vortex-samples"]]
create_tar(os.path.join(desktop, "SUBIR_4_OBRAS_MITAD_2.tar.gz"), assets_2)

print("Done!")
