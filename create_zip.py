import os
import zipfile
import re

def zip_addon_folder():
    # Get the current user's AppData\Roaming folder
    appdata_roaming = os.path.join(os.environ['APPDATA'])
    folder_path = os.path.join(appdata_roaming, 'Kodi', 'addons', 'plugin.video.fenlight')
    addon_xml_path = os.path.join(folder_path, 'addon.xml')

    # Read the version number from addon.xml
    with open(addon_xml_path, 'r', encoding='utf-8') as file:
        first_line = file.readline().strip()
        version_match = re.search(r'version="([\d\.]+)"', first_line)
        if not version_match:
            raise ValueError("Version number not found in addon.xml")
        version_number = version_match.group(1)

    # Define the output directory and ensure it exists
    output_dir = os.path.join(os.getcwd(), 'packages')
    os.makedirs(output_dir, exist_ok=True)

    # Define the zip file name
    zip_name = os.path.join(output_dir, f'plugin.video.fenlight-{version_number}.zip')

    # Create the zip file
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            # Skip .git folder
            if '.git' in dirs:
                dirs.remove('.git')

            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)

    print(f"Zip file created: {zip_name}")

    # Update the fen_light_version file
    version_file_path = os.path.join(output_dir, 'fen_light_version')
    with open(version_file_path, 'w', encoding='utf-8') as version_file:
        version_file.write(version_number)

    # Update the index.html file in the packages folder
    index_file_path = os.path.join(output_dir, 'index.html')
    with open(index_file_path, 'w', encoding='utf-8') as index_file:
        index_file.write(f'<!DOCTYPE html>\n<a href="{os.path.basename(zip_name)}">{os.path.basename(zip_name)}</a>')

    # Update the fen_light_changes file
    changelog_path = os.path.join(folder_path, 'resources', 'text', 'changelog.txt')
    changes_file_path = os.path.join(output_dir, 'fen_light_changes')
    with open(changelog_path, 'r', encoding='utf-8') as changelog_file:
        changelog_lines = changelog_file.readlines()
        latest_changes = []
        for line in changelog_lines:
            if line.strip() == "":
                break
            latest_changes.append(line.strip())
    with open(changes_file_path, 'w', encoding='utf-8') as changes_file:
        changes_file.write("\n".join(latest_changes))

    # Update the index.html file in the script's folder
    script_index_file_path = os.path.join(os.getcwd(), 'index.html')
    with open(script_index_file_path, 'w', encoding='utf-8') as script_index_file:
        script_index_file.write(f'<!DOCTYPE html>\n<a href="packages/{os.path.basename(zip_name)}">{os.path.basename(zip_name)}</a>')

if __name__ == "__main__":
    zip_addon_folder()
