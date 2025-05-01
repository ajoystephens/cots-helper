import pickle
import shutil

from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.resolve()
SESSION_PATH = ROOT_DIR / 'data' / 'sessions'

def get_saved_sessions():
    dir_path = SESSION_PATH

    if not dir_path.exists():
        return []

    return [entry.name for entry in dir_path.iterdir() if entry.is_dir()]

def save_state(key,creatures,log):
    dir_path = SESSION_PATH / key
    dir_path.mkdir(parents=True, exist_ok=True)

    creatures_filename = "creatures.pkl"
    creatures_filepath = dir_path / creatures_filename
    with open(creatures_filepath, "wb") as file:
        pickle.dump(creatures, file)


    # session_log_filepath = ROOT_DIR / 'tmp' / 'log.txt'
    saved_log_filepath =  dir_path / 'log.pkl'
    with open(saved_log_filepath, "wb") as file:
        pickle.dump(log, file)
    # if session_log_filepath.is_file():
    #     shutil.copy2(session_log_filepath, saved_log_filepath)

def load_state(key):
    dir_path = SESSION_PATH / key

    creatures_filename = "creatures.pkl"
    creatures_filepath = dir_path / creatures_filename
    # with open(creatures_filepath, "wb") as file:
    #     pickle.dump(creatures, file)
    creatures = []
    if creatures_filepath.is_file():
        with open(creatures_filepath, 'rb') as file:
            creatures = pickle.load(file)

    logs = []
    saved_log_filepath =  dir_path / 'log.pkl'
    if saved_log_filepath.is_file():
        with open(saved_log_filepath, 'rb') as file:
            logs = pickle.load(file)
    # session_log_filepath = ROOT_DIR / 'tmp' / 'log.txt'
    # saved_log_filepath =  dir_path / 'log.txt'
    # if saved_log_filepath.is_file():
    #     shutil.copy2(saved_log_filepath, session_log_filepath)

    return(creatures,logs)