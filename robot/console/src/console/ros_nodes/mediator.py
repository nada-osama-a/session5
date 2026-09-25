from PySide6.QtCore import Signal, QObject, Property
from console.ros_nodes.worker import WorkerThread

class Mediator(QObject):
    telemetry_updated = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.telemetry_exists = False

        self._x = 0.0
        self._y = 0.0
        self._angle = 0.0
        
        self._battery = 0.0
        self._vel = 0.0
        self._ang_vel = 0.0

        self._worker = WorkerThread()
        self._worker.signals.telemetry_signal.connect(self.handle_telemetry)
        self._worker.start()

    @Property(float, notify=telemetry_updated)
    def x(self):return self._x

    @Property(float, notify=telemetry_updated)
    def y(self):return self._y

    @Property(float, notify=telemetry_updated)
    def angle(self):return self._angle

    @Property(float, notify=telemetry_updated)
    def battery(self):return self._battery

    @Property(float, notify=telemetry_updated)
    def vel(self):return self._vel

    @Property(float, notify=telemetry_updated)
    def ang_vel(self):return self._ang_vel


    def handle_telemetry(self, telemetry: dict) -> None:
        self._x = telemetry.get("x", self._x)
        self._y = telemetry.get("y", self._y)
        self._angle = telemetry.get("angle", self._angle)
        self._battery = telemetry.get("battery", self._battery)
        self._vel = telemetry.get("vel", self._vel)
        self._ang_vel = telemetry.get("ang_vel", self._ang_vel)

        self.telemetry_exists = True
        self.telemetry_updated.emit()