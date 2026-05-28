import json
import urllib.request
import threading
from distutils.version import LooseVersion

VERSION_URL = "https://raw.githubusercontent.com/matheusfreitasrangel97-ops/GeoKit/main/version.json"

def check_for_updates(current_version: str, callback):
    """
    Checks for updates in a background thread.
    If a new version is available, calls the callback with (new_version, url, notes) in the main thread.
    """
    def thread_target():
        try:
            req = urllib.request.Request(
                VERSION_URL, 
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) GeoKitUpdater'}
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode('utf-8'))
                remote_version = data.get("version")
                update_url = data.get("url", "https://github.com/matheusfreitasrangel97-ops/GeoKit")
                notes = data.get("notes", "")

                if remote_version:
                    # Compares version strings
                    try:
                        # Use LooseVersion or simple tuple comparison
                        is_newer = LooseVersion(remote_version) > LooseVersion(current_version)
                    except Exception:
                        # Fallback simple split comparison
                        is_newer = tuple(map(int, remote_version.split('.'))) > tuple(map(int, current_version.split('.')))

                    if is_newer:
                        callback(remote_version, update_url, notes)
        except Exception:
            # Silently ignore errors (e.g. offline, DNS failure, 404)
            pass

    thread = threading.Thread(target=thread_target, daemon=True)
    thread.start()
