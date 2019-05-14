from threading import Thread
from concurrent.futures import ThreadPoolExecutor
import csv
import time
import asyncio

class Live:

    def __init__(self, path):
        self.file = open(path, 'r+')
        self.last_position = self.file.tell()
        self.running = False
        self.current_line = 1
        self._set_headers()
        self.start()
        self.pool = ThreadPoolExecutor(max_workers=3)
        self.futures = {}

    def _set_headers(self):
        headers = []
        for header in self.file.readline().split(';')[:-1]:
            if '(C)' in header:
                header = header.replace('(C)', '_c')
            elif '(P)' in header:
                header = header.replace('(P)', '_p')
            headers.append(header)
        for header in headers:
            setattr(self, header, [])
        self.headers = dict(enumerate(headers))

    def _proccess_line(self, line):
        values = line.split(';')[:-1]
        for idx, value in enumerate(values):
            current_header = self.headers[idx]
            getattr(self, current_header).append(value)

    def run(self):
        while self.running:
            self.last_position = self.file.tell()
            line = self.file.readline()
            if not line:
                time.sleep(1)
                self.file.seek(self.last_position)
            else:
                self.current_line += 1
                self._proccess_line(line)

    def stop(self):
        if self.running:
            self.running = False
        else:
            print('Not Running.')

    def start(self):
        self.thread = Thread(target=self.run)
        self.running = True
        self.thread.start()

    def _trigger(self, header, value):
        while not int(getattr(self, header)[-1]) > value:
            asyncio.sleep(1)
        return True

    def set_triggers(self, headers):
        for header, value in headers.items():
            self.futures[header] = self.pool.submit(self._trigger, header, value)

    def set_callback(self, future_name, callback):
        if future_name in self.futures.keys():
            self.futures[future_name].add_done_callback(callback)

class Stats(Live):

    def __init__(self, path, static=False):
        if static:
            self.file = open(path, 'r+')
            self.reader = csv.DictReader(self.file, delimiter=';')
            self.__friendly_headers()
        else:
            super().__init__(path)

    def __friendly_headers(self):
        headers = {
            'time': 'ElapsedTime(C)',
            'call_rate': 'CallRate(P)',
            'incoming': 'IncomingCall(P)',
            'outgoing': 'OutgoingCall(P)',
            'simcall': 'CurrentCall',
            'success': 'SuccessfulCall(P)',
            'failed': 'FailedCall(P)',
            'retrans': 'Retransmissions(P)'
        }
        for header, value in headers.items():
            data = self.fieldname_data(value)
            setattr(self, header, data)

    def fieldname_data(self, fieldname):
        fieldname_data = []
        for row in self.reader:
            fieldname_data.append(row[fieldname])
        self.file.seek(0)
        return fieldname_data
