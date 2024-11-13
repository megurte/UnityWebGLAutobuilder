# Unity WebGL Auto-Build and Upload Script
This Python script automates the process of building a Unity WebGL project, archiving it, and uploading it to an [itch.io](https://itch.io/) channel using [Butler](https://github.com/itchio/butler).

The script monitors a Git repository and triggers a new build whenever a new commit with a specific tag is detected.

## Requirements
- **Unity Editor** Installed and available on your system. Update the `UNITY_PATH` in the script to the location of your Unity Editor.
- **Git** Installed and configured to pull the latest changes from your repository.
- **Butler** Installed and added to your system's PATH. Butler is used to upload the build to itch.io. See official documentation how to install [butler](https://itch.io/docs/butler/).
- **Python** This script is written in Python and requires Python 3+.

## Configuration
Before using the script, make sure to configure the following settings:

- `UNITY_PATH` The path to the Unity Editor executable (Unity.exe).
- `PROJECT_PATH` The path to your Unity project.
- `BUILD_PATH` The folder where the WebGL build will be stored.
- `ZIP_PATH` The path for the zipped archive of the WebGL build.
- `ITCH_IO_CHANNEL` The [itch.io](https://itch.io/) channel where the build will be uploaded. Format should be username/game:web.
- `BUTLER_PATH` If Butler is in your system PATH, use "butler". Otherwise, specify the full path.
- `CHECK_INTERVAL` The interval (in seconds) between checks for new commits.

## Usage
Configure the script as described in the Configuration section.

Run the script using Python: `python autobuilder.py`

The script will continuously check the Git repository for new commits. If a new commit contains the tag `[build]` in its message, the following steps will occur:

1. **Pull Latest Changes** The script pulls the latest changes from the Git repository.
2. **Build the Project** Unity will run a WebGL build using the specified method (`Editor.WebGLBuilder.PerformWebGLBuild` by default). You may need to create or modify this method in your Unity project. Unity builder starts in package mode without interface.
3. **Archive the Build** The WebGL build folder is compressed into a .zip file.
4. **Upload to itch.io** The .zip file is uploaded to the specified itch.io channel using Butler.

[Here an example](https://github.com/megurte/ItchAutobuilder/blob/main/WebGLBuilder.cs) of external method in C# to call from the script.
