import time

from AScanner.tools import humanized_time

from watchdog.observers import polling

from .whandler import WHandler


class ASWatchdog():

    @property
    def scan_directories(self):
        scan_dirs = self.ascanner.config.dict["watchdog"]["scan_dirs"]
        if not scan_dirs:
            return []
        if not isinstance(scan_dirs, list):
            scan_dirs = [scan_dirs]
        return scan_dirs

    def __init__(self, ascanner):
        self.ascanner = ascanner

        self.observer = polling.PollingObserver()

        self.directories = {}

        for directory in self.scan_directories:

            curr_dict = self.defaults

            if directory.lower() in list(self.ascanner.config.dict.keys()):
                for dir_setting in list(curr_dict.keys()):
                    if dir_setting in list(self.ascanner.config.dict[directory.lower()].keys()):
                        curr_dict[dir_setting] = self.ascanner.config.dict[directory.lower()][dir_setting]

            if curr_dict["patterns"] == "media":
                curr_dict["patterns"] = self.media_patterns

            curr_dict["handler"] = WHandler(patterns=curr_dict["patterns"])
            curr_dict["handler"].ascanner = self.ascanner

            self.directories[directory] = curr_dict

        for directory in list(self.directories.keys()):

            self.directories[directory]["watchOBJ"] = self.observer.schedule(
                event_handler=self.directories[directory]["handler"],
                path=directory,
                recursive=self.directories[directory]["recursive"])

    def scan_interval(self):
        return self.ascanner.config.dict["watchdog"]["polling_interval"]

    def start(self):

        self.ascanner.logger.info("Preparing to observe %s directories:" % len(list(self.directories.keys())))
        for directory in list(self.directories.keys()):
            self.ascanner.logger.info("* %s, recursive=%s" % (directory, self.directories[directory]["recursive"]))

        scan_start_time = time.time()

        self.observer.start()

        self.ascanner.logger.info("Observing %s directories" % len(list(self.directories.keys())))

        # monitor
        try:
            while True:
                scan_end_time = time.time()
                sleeptime = self.scan_interval
                self.ascanner.logger.info("Performed a scan of %s directories. Process took %s. Sleeping for %s" % (
                    len(list(self.directories.keys())), humanized_time(scan_end_time - scan_start_time), humanized_time(sleeptime)))
                time.sleep(sleeptime)
                scan_start_time = time.time()
        except KeyboardInterrupt:
            self.observer.unschedule_all()
            self.observer.stop()

    def stop(self):
        self.observer.unschedule_all()
        self.observer.stop()

    @property
    def status(self):
        return self.observer.is_alive()

    @property
    def defaults(self):
        return {
                "recursive": False,
                "patterns": None
                }

    @property
    def media_patterns(self):
        return ["*.webm",
                "*.mkv",
                "*.flv",
                "*.vob",
                "*.ogv",
                "*.ogg",
                "*.drc",
                "*.gif",
                "*.gifv",
                "*.mng",
                "*.avi",
                "*.mov",
                "*.qt",
                "*.wmv",
                "*.yuv",
                "*.rm",
                "*.rmvb",
                "*.asf",
                "*.amv",
                "*.mp4",
                "*.m4p",
                "*.m4v",
                "*.mpg",
                "*.mp2",
                "*.mpeg",
                "*.mpe",
                "*.mpv",
                "*.m2v",
                "*.m4v",
                "*.svi",
                "*.3gp",
                "*.3g2",
                "*.mxf",
                "*.roq",
                "*.nsv",
                "*.f4v",
                "*.f4p",
                "*.f4a",
                "*.f4b",
                "*.mp3",
                "*.flac",
                "*.ts"
                ]
