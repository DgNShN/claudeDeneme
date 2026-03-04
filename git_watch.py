import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

IGNORED = {'messages.db', '__pycache__', '.git', 'git_watch.py'}

class AutoGitHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_push = 0

    def should_ignore(self, path):
        for ig in IGNORED:
            if ig in path:
                return True
        return False

    def on_modified(self, event):
        if event.is_directory or self.should_ignore(event.src_path):
            return
        now = time.time()
        if now - self.last_push < 3:
            return
        self.last_push = now
        self.push(event.src_path)

    def push(self, path):
        print(f"\nDeğişiklik algılandı: {path}")
        try:
            subprocess.run(['git', 'add', '-A'], check=True)
            result = subprocess.run(['git', 'diff', '--cached', '--quiet'])
            if result.returncode == 0:
                print("Değişiklik yok, push atlanıyor.")
                return
            subprocess.run(['git', 'commit', '-m', f'Auto-commit: {path.split("/")[-1]} güncellendi'], check=True)
            subprocess.run(['git', 'push', 'origin', 'claude/priceless-margulis:main'], check=True)
            print("GitHub'a push edildi!")
        except subprocess.CalledProcessError as e:
            print(f"Hata: {e}")

if __name__ == '__main__':
    print("Git izleyici başlatıldı. Dosya değişikliklerini izliyor...")
    print("Durdurmak için Ctrl+C\n")
    handler = AutoGitHandler()
    observer = Observer()
    observer.schedule(handler, path='.', recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
