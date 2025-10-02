import os
import subprocess
import time
import zipfile

# Configuration
UNITY_PATH = ".../Editor/Unity.exe"  # Path to unity editor .exe
PROJECT_PATH = ".../ProjectRepo"  # Path to unity project
BUILD_PATH = os.path.join(PROJECT_PATH, "Build/WebGL")  # Path to web build folder 
ZIP_PATH = os.path.join(PROJECT_PATH, "Build/WebGL.zip")  # Path to archive
ITCH_IO_CHANNEL = "name/gamelink:web"  # Itch's user name and game's link name username/game:web
BUTLER_PATH = "butler"  # If butler in PATH - use just 'butler'
CHECK_INTERVAL = 60  # Inverval how ofter stript checks new commits
BUILD_TAG = "[build]" # You can change tag here

def get_latest_commit_message():
    try:
        commit_message = subprocess.check_output(["git", "log", "-1", "--pretty=%B"]).strip().decode("utf-8")
        return commit_message
    except subprocess.CalledProcessError as e:
        print(f"Error when get commit: {e}")
        return None

def get_latest_commit_hash():
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"]).strip().decode("utf-8")
    except subprocess.CalledProcessError as e:
        print(f"Error getting commit hash: {e}")
        return None

def pull_latest_changes():
    try:
        subprocess.check_call(["git", "pull"])
        print("Pulled changes")
    except subprocess.CalledProcessError as e:
        print(f"Error git pull: {e}")

def build_webgl():
    try:
        subprocess.check_call([
            UNITY_PATH,
            "-quit", "-batchmode",
            "-projectPath", PROJECT_PATH,
            "-executeMethod", "Editor.WebGLBuilder.PerformWebGLBuild",  # Here you can modify method as you want
            "-buildTarget", "WebGL",
            "-logFile", "unity_build.log"
        ])
        print("Build WebGL succesful")
    except subprocess.CalledProcessError as e:
        print(f"Build Error: {e}")
        return False
    return True

def zip_build_folder():
    if os.path.exists(ZIP_PATH):
        os.remove(ZIP_PATH)
    with zipfile.ZipFile(ZIP_PATH, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(BUILD_PATH):
            for file in files:
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, BUILD_PATH)
                zipf.write(full_path, relative_path)
    print("Archive finished.")

def upload_to_itch():
    try:
        subprocess.check_call([BUTLER_PATH, "push", ZIP_PATH, ITCH_IO_CHANNEL])
        print("Upload to itch.io finished.")
    except subprocess.CalledProcessError as e:
        print(f"Error during upload to itch.io: {e}")

def main():
    last_commit_message = ""
    last_commit_hash = ""
    
    while True:
        pull_latest_changes()
        
        commit_message = get_latest_commit_message()
        commit_hash = get_latest_commit_hash()

        if last_commit_hash != commit_hash:
        	if commit_message and BUILD_TAG.lower() in commit_message.lower(): 
        	    print("Tag found, starting build...")
        	    last_commit_hash = commit_hash

        	    if build_webgl():
        	        zip_build_folder()
        	        upload_to_itch()
        	    else:
        	        print("Build failed")
        	else:
        	    print("Last commint doesn't contain [build] tag. Skip build.")
        else:
        	print("Same commit. Skip build")
        
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()

