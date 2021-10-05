from watchdog.events import PatternMatchingEventHandler


class MediaHandler(PatternMatchingEventHandler):
    patterns = [
                "*.webm",
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

    def process(self, event):
        """"
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """

        self.ascanner.logger.info("Detected a %s change to %s" % (event.event_type, event.src_path))
        for plugin_name in list(self.ascanner.targets.keys()):
            if self.ascanner.plugins.plugins[plugin_name].manifest["type"] in ["target"]:
                self.ascanner.targets[plugin_name].dispatch(event)

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)

    def on_deleted(self, event):
        self.process(event)

    def on_moved(self, event):
        self.process(event)
