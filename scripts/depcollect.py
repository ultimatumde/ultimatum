import yaml
import os
import subprocess

DEPMAP_FNAME = "UMDEPMAP.yaml"

DEPENDENCIES = {
    "arch": [],
    "nix": [],
    "debian": []
}

for root, dirs, files in os.walk("."):
    if DEPMAP_FNAME in files:
        with open(os.path.join(root, DEPMAP_FNAME), "r") as f:
            depmap = yaml.safe_load(f)
            if depmap is not None:
                print(f"{DEPMAP_FNAME}: {root}")
                for dep_type, deps in depmap.items():
                    if dep_type in DEPENDENCIES:
                        for dep in deps:
                            if dep not in DEPENDENCIES[dep_type]:
                                DEPENDENCIES[dep_type].append(dep)
                            else:
                                print(f"duplicate dependency '{dep}' in {DEPMAP_FNAME} at {root}")
                    else:
                        print(f"unknown dependency type '{dep_type}' in {DEPMAP_FNAME} at {root}")

os_name = "arch"
with open("/etc/os-release", "r") as f:
    os_release = f.read()
    os_name = list(filter(lambda x: x.split("=")[0] == "ID", os_release.split("\n"))).pop().split("=")[1].strip('"')

match os_name:
    case "arch":
        import os
        subprocess.run(["pacman", "-S", "--needed", "--noconfirm", *DEPENDENCIES["arch"]])
    case "nixos":
        import os
        cmds = [
            ["nix-env", "-iA"],
            ["nix", "profile", "install"]
        ]
        worked = False
        for cmd in cmds:
            try:
                print("Running " + " ".join(cmd))
                for dep in DEPENDENCIES["nix"]:
                    try:
                        print(f"{dep} t1/2 ...", end=" ")
                        r = subprocess.run(cmd + ["nixpkgs#" + dep], capture_output=False, check=True, text=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        print("installed", end=" ")
                    except Exception as e:
                        try:
                            print(f"{dep} t2/2 ...", end=" ")
                            r = subprocess.run(cmd + ["nixpkgs." + dep], capture_output=False, check=True, text=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                            print("installed", end=" ")
                        except Exception as e:
                            print(f"exists", end=" ")
            except Exception as e:
                print(f"command {cmd} failed: {e}")
        if not worked:
            print("\nseems i was unable to automatically install every dependency. here's how to add them manually:")
            print("\n".join(map(lambda x: " - pkgs." + x, DEPENDENCIES["nix"])))
            exit(1)
    case "debian":
        import os
        subprocess.run(["apt-get", "install", "-y", *DEPENDENCIES["debian"]])
    case _:
        print(f"unknown OS '{os_name}'")
        exit(1)