

class Startup_Tasks():
    endpoints = ["/api/startup_tasks"]
    endpoint_name = "api_startup_tasks"
    endpoint_methods = ["GET", "POST"]

    def __init__(self, ascanner):
        self.ascanner = ascanner

        self.watchdog_start_url = "/api/watchdog?method=start"

    def __call__(self, *args):
        return self.get(*args)

    def get(self, *args):

        self.ascanner.logger.info("Running Startup Tasks.")

        # Start watchdog thread
        self.ascanner.api.threadget(self.watchdog_start_url)

        self.ascanner.logger.info("Startup Tasks Complete.")

        return "Success"
