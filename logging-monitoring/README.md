# Application Insights
*for Logging & Monitoring of Databricks*

```
from applicationinsights import TelemetryClient
.....

__author__ = "Vinay Narayana"
__version__ = "1.0.0"
__github__ = "https://github.com/Vinay26k"
.......



class AppInsightsLogger:
    def __init__(self, props={}, measures={}) -> None:
        # telemetry config
        self.tc = TelemetryClient(os.getenv("APPINSIGHTS_INSTRUMENTATIONKEY"))
        self.send_log(props={**STATIC_PROPS, **{"LoggerMessage": "Logger has been initialized"}}, measures={**STATIC_MEASURES, **{"RunTime": time.time() - self.start_time}})
        
    def add_config(self, props, measures) -> None:
        ....

    def start(self):
        ....
        
    def end(self):
        ....

    def add_log(self, logType, props, measures) -> None:
        self.send_log(props={**STATIC_PROPS, **props}, measures={**STATIC_MEASURES, **measures})

    def send_log(self, eventName="NotebookLogger", props={}, measures={}) -> None:
        self.tc.track_event(eventName, props, measures)
        self.tc.flush()

    def send_exception(self, eventName="Exception", props={}, measures={}) -> None:
        error_tb = traceback.format_exc()
        self.tc.track_exception(properties={**STATIC_PROPS, **props, **{"ErrorTraceback": error_tb}}, measurements={**STATIC_MEASURES, **{"RunTime": time.time() - self.start_time}, **measures})
        self.tc.flush()

log = AppInsightsLogger()
```

Code Link: [AppInsightsLogger.py](https://github.com/Vinay26k/azure/blob/main/logging-monitoring/AppInsightsLogger.py)