from watchdog.events import PatternMatchingEventHandler


class WHandler(PatternMatchingEventHandler):
    patterns = []

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
            self.ascanner.targets[plugin_name].dispatch(event)

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)

    def on_deleted(self, event):
        self.process(event)

    def on_moved(self, event):
        self.process(event)
