import time
import datetime
import threading


class Debugger:
    thread = None

    def __init__(self):
        self.error_log = 'error_log'
        self.debug_log = 'debug_log'
        self.error_file = None
        self.debug_file = None
        self.files_closing = False
        self.flush_thread = None

    def run(self):
        self.error_file = open(self.error_log, 'a+')
        self.debug_file = open(self.debug_log, 'a+')
        self.flush_thread = threading.Thread(target=self.output_flush, args=(10,), daemon=True)

    def output_flush(self, interval):
        time.sleep(interval)
        self.files_closing = True
        time.sleep(0.1)
        self.error_file.close()
        self.debug_file.close()
        self.error_file = open(self.error_log, 'a+')
        self.debug_file = open(self.debug_log, 'a+')
        self.files_closing = False

    def write(self, content, code):
        x = threading.Thread(target=self.safe_write, args=(content, code))
        x.start()

    def safe_write(self, content, code):
        start_time = datetime.datetime.now()
        while self.files_closing:
            time.sleep(0.1)
            if (datetime.datetime.now() - start_time).seconds >= 5:
                with open('debugger_timeout') as f:
                    f.write(f'Timeout at {start_time}, Log [' + ('LOG' if code == 0 else 'ERROR') + '] entry:\n'\
                            + content)
                    return
        if code == self.DebugCode.LOG:
            self.debug_file.write(content + '\n')
        elif code == self.DebugCode.ERROR:
            self.error_file.write(content + '\n')
        return

    class DebugCode:
        LOG = 0
        ERROR = 1
