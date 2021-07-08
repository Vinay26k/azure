from applicationinsights import TelemetryClient
import datetime as dt
import time
import os
import traceback

__author__ = "Vinay Narayana"
__version__ = "1.0.0"
__github__ = "https://github.com/Vinay26k"
__status__ = "Production"
__createdAt__ = "Feb 22, 2021"
__lastModified__ = "Feb 22, 2021"

## Global variables
global STATIC_PROPS, STATIC_MEASURES

STATIC_PROPS = {
    "NotebookName": "MyTestNotebook",
    "NotebookPath": "/path/to/my/notebook",
}
STATIC_MEASURES = {
    "DateKey": int(dt.datetime.now().strftime("%Y%m%d")),
    "TimeKey": int(dt.datetime.now().strftime("%H%M%S%f"))
}

class AppInsightsLogger:
    def __init__(self, props={}, measures={}) -> None:
        ## telemetry config
        self.tc = TelemetryClient(os.getenv("APPINSIGHTS_INSTRUMENTATIONKEY"))
        self.send_log(props={**STATIC_PROPS, **{"LoggerMessage": "Logger has been initialized"}}, measures={**STATIC_MEASURES, **{"RunTime": time.time() - self.start_time}})
        
    def add_config(self, props, measures) -> None:
        STATIC_PROPS.update(props)
        STATIC_MEASURES.update(measures)

    def start(self):
        self.add_log("START", {**STATIC_PROPS, **{"Transformation": "Notebook Execution Started", "LoggerMessage": "Notebook Execution Started"}}, {**STATIC_MEASURES})
        
    def end(self):
        self.add_log("END", {**STATIC_PROPS, **{"Transformation": "Notebook Execution Completed", "LoggerMessage": "Notebook Execution Completed"}}, {**STATIC_MEASURES})
          
    def add_log(self, logType="INFO", props={}, measures={}) -> None:
        self.send_log(props={**STATIC_PROPS, **props}, measures={**STATIC_MEASURES, **measures})

    def send_log(self, eventName="NotebookLogger", props={}, measures={}) -> None:
        self.tc.track_event(eventName, props, measures)
        self.tc.flush()

    def send_exception(self, eventName="Exception", props={}, measures={}) -> None:
        error_tb = traceback.format_exc()
        self.tc.track_exception(properties={**STATIC_PROPS, **props, **{"ErrorTraceback": error_tb}}, measurements={**STATIC_MEASURES, **{"RunTime": time.time() - self.start_time}, **measures})
        self.tc.flush()

log = AppInsightsLogger()
