import os
import zipfile
import re

def zip_addon_folder(addon_name, version_file_name):
    # Get the current user's AppData\Roaming folder
    appdata_roaming = os.path.join(os.environ['APPDATA'])
    folder_path = os.path.join(appdata_roaming, 'Kodi', 'addons', addon_name)
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
    zip_name = os.path.join(output_dir, f'{addon_name}-{version_number}.zip')

    # Create the zip file
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            # Skip .git folder
            if '.git' in dirs:
                dirs.remove('.git')

            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.join(addon_name, os.path.relpath(file_path, folder_path))
                zipf.write(file_path, arcname)

    print(f"Zip file created: {zip_name}")

    # Update the version file
    version_file_path = os.path.join(output_dir, version_file_name)
    with open(version_file_path, 'w', encoding='utf-8') as version_file:
        version_file.write(version_number)

    return zip_name

def update_index_files(latest_fenlight_zip, latest_fen_zip):
    # Update the index.html file in the packages folder
    index_file_path = os.path.join(os.getcwd(), 'packages', 'index.html')
    with open(index_file_path, 'w', encoding='utf-8') as index_file:
        if latest_fenlight_zip:
            index_file.write(f'<!DOCTYPE html>\n<a href="{os.path.basename(latest_fenlight_zip)}">{os.path.basename(latest_fenlight_zip)}</a>\n')
        if latest_fen_zip:
            index_file.write(f'<a href="{os.path.basename(latest_fen_zip)}">{os.path.basename(latest_fen_zip)}</a>\n')

    # Update the index.html file in the script's folder
    script_index_file_path = os.path.join(os.getcwd(), 'index.html')
    with open(script_index_file_path, 'w', encoding='utf-8') as script_index_file:
        if latest_fenlight_zip:
            script_index_file.write(f'<!DOCTYPE html>\n<a href="packages/{os.path.basename(latest_fenlight_zip)}">{os.path.basename(latest_fenlight_zip)}</a>\n')
        if latest_fen_zip:
            script_index_file.write(f'<a href="packages/{os.path.basename(latest_fen_zip)}">{os.path.basename(latest_fen_zip)}</a>\n')

def get_latest_zip_from_version_file(version_file_name, addon_name):
    version_file_path = os.path.join(os.getcwd(), 'packages', version_file_name)
    if os.path.exists(version_file_path):
        with open(version_file_path, 'r', encoding='utf-8') as version_file:
            version_number = version_file.read().strip()
            return os.path.join(os.getcwd(), 'packages', f'{addon_name}-{version_number}.zip')
    return None

def main():
    latest_fenlight_zip = None
    latest_fen_zip = None

    # Check if plugin.video.fenlight folder exists
    fenlight_folder_path = os.path.join(os.environ['APPDATA'], 'Kodi', 'addons', 'plugin.video.fenlight')
    if os.path.exists(fenlight_folder_path):
        latest_fenlight_zip = zip_addon_folder('plugin.video.fenlight', 'fen_light_version')
    else:
        latest_fenlight_zip = get_latest_zip_from_version_file('fen_light_version', 'plugin.video.fenlight')

    # Check if plugin.video.fen folder exists
    fen_folder_path = os.path.join(os.environ['APPDATA'], 'Kodi', 'addons', 'plugin.video.fen')
    if os.path.exists(fen_folder_path):
        latest_fen_zip = zip_addon_folder('plugin.video.fen', 'fen_version')
    else:
        latest_fen_zip = get_latest_zip_from_version_file('fen_version', 'plugin.video.fen')

    # Update the index.html files
    update_index_files(latest_fenlight_zip, latest_fen_zip)

if __name__ == "__main__":
    main()