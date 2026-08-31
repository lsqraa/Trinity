# PyQt6 Core Best Practices & Widgets Catalog

Extended documentation based on Qt6 official patterns and community best practices.

---

## 1. Threading & Concurrency in PyQt6

> **CRITICAL RULE**: The GUI in Qt is NOT thread-safe. Never modify widgets or update UI properties directly from background threads (`QThread`, `threading.Thread`, `asyncio`). Always communicate via **`pyqtSignal`**.

### Recommended Pattern: Worker Object + QThread

```python
from PyQt6.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QMainWindow, QPushButton, QProgressBar, QVBoxLayout, QWidget, QMessageBox
import time

class HeavyTaskWorker(QObject):
    """
    Independent worker instance with signals for cross-thread delivery.
    """
    progress = pyqtSignal(int)
    result_ready = pyqtSignal(dict)
    error = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, data_list: list):
        super().__init__()
        self.data_list = data_list
        self._is_cancelled = False

    @pyqtSlot()
    def run(self):
        try:
            total = len(self.data_list)
            for i, item in enumerate(self.data_list):
                if self._is_cancelled:
                    return
                
                # Heavy operations (e.g. database, HTTP request, file I/O)
                time.sleep(0.1)
                
                percent = int(((i + 1) / total) * 100)
                self.progress.emit(percent)

            self.result_ready.emit({"status": "success", "count": total})
        except Exception as e:
            self.error.emit(str(e))
        finally:
            self.finished.emit()

    def cancel(self):
        self._is_cancelled = True


class MainWindowThreadExample(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 Clean Threading")
        self.resize(400, 200)

        self.btn_start = QPushButton("Iniciar Tarea Pesada")
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)

        layout = QVBoxLayout()
        layout.addWidget(self.btn_start)
        layout.addWidget(self.progress_bar)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.btn_start.clicked.connect(self.start_heavy_task)

    def start_heavy_task(self):
        self.btn_start.setEnabled(False)
        self.progress_bar.setValue(0)

        # 1. Instanciar thread y worker
        self.thread = QThread()
        self.worker = HeavyTaskWorker([f"item_{i}" for i in range(20)])
        self.worker.moveToThread(self.thread)

        # 2. Conectar señales
        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.result_ready.connect(self.on_task_success)
        self.worker.error.connect(self.on_task_error)
        
        # 3. Limpieza de memoria
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(lambda: self.btn_start.setEnabled(True))

        # 4. Iniciar
        self.thread.start()

    def on_task_success(self, res):
        QMessageBox.information(self, "Completado", f"Procesados {res['count']} elementos.")

    def on_task_error(self, err_msg):
        QMessageBox.critical(self, "Error", f"Fallo al procesar: {err_msg}")
```

---

## 2. Advanced Signals & Slots Techniques

### Types and Signatures in PyQt6
```python
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

class DataEmitter(QObject):
    # Signals declaration at class level
    int_signal = pyqtSignal(int)
    str_signal = pyqtSignal(str)
    multi_arg_signal = pyqtSignal(str, int, bool)
    dict_payload = pyqtSignal(dict)
    
    # Overloaded signal (can emit int or str)
    overloaded_signal = pyqtSignal([int], [str])

    def trigger(self):
        self.int_signal.emit(42)
        self.str_signal.emit("Hola")
        self.multi_arg_signal.emit("Evento", 1, True)
        self.dict_payload.emit({"user": "admin", "token": "xyz"})
```

### Clean Disconnect & Signal Blocking
```python
# Temporary block to avoid feedback loops (e.g. updating input from model without triggering on_change)
widget.blockSignals(True)
widget.setValue(100)
widget.blockSignals(False)

# Disconnect
widget.valueChanged.disconnect(self.my_slot)
```

---

## 3. Comprehensive Widgets Quick Reference (PyQt6 Specific)

| Widget | Key Methods & Properties | Primary Signals |
|---|---|---|
| **`QLineEdit`** | `setPlaceholderText()`, `setEchoMode()`, `setClearButtonEnabled(True)`, `setValidator()` | `textChanged`, `returnPressed`, `editingFinished` |
| **`QTextEdit` / `QPlainTextEdit`** | `setPlainText()`, `toPlainText()`, `append()`, `setReadOnly()` | `textChanged` |
| **`QComboBox`** | `addItems()`, `currentText()`, `currentIndex()`, `setEditable()` | `currentIndexChanged`, `currentTextChanged` |
| **`QSpinBox` / `QDoubleSpinBox`** | `setRange(min, max)`, `setValue()`, `setSingleStep()`, `setSuffix()` | `valueChanged` |
| **`QCheckBox`** | `setChecked()`, `isChecked()`, `setTristate()` | `stateChanged` |
| **`QSlider`** | `setOrientation()`, `setRange()`, `setValue()`, `setTickPosition()` | `valueChanged` |
| **`QProgressBar`** | `setRange(0, 100)`, `setValue()`, `setFormat("%p%")`, `setRange(0, 0)` (indeterminate) | `valueChanged` |
| **`QTableWidget`** | `setColumnCount()`, `setHorizontalHeaderLabels()`, `setItem()`, `setSelectionBehavior()` | `cellClicked`, `cellDoubleClicked`, `itemChanged` |
| **`QTreeWidget`** | `setHeaderLabels()`, `addTopLevelItem()`, `expandAll()` | `itemClicked`, `itemSelectionChanged` |
| **`QListWidget`** | `addItem()`, `currentItem()`, `currentRow()` | `itemClicked`, `currentItemChanged` |
| **`QTabWidget`** | `addTab(widget, label)`, `setCurrentIndex()`, `setTabsClosable(True)` | `currentChanged`, `tabCloseRequested` |
| **`QStackedWidget`** | `addWidget(page)`, `setCurrentIndex()`, `setCurrentWidget()` | `currentChanged` |
| **`QSplitter`** | `addWidget()`, `setOrientation()`, `setSizes([w1, w2])` | `splitterMoved` |

---

## 4. Anti-Patterns & Pitfalls to Avoid

1. **Garbage Collection of Windows/Dialogs**:
   - ❌ Creating a non-modal window in a local variable: `w = MyWindow(); w.show()` (it gets garbage collected immediately).
   - ✅ Always store a reference: `self.sub_window = MyWindow(); self.sub_window.show()`.
2. **Blocking `QApplication.exec()`**:
   - ❌ Never use `time.sleep()` in UI callbacks or event handlers.
   - ✅ Use `QTimer.singleShot(ms, callback)` or background workers (`QThread`).
3. **Hardcoding Geometry**:
   - ❌ Never use `setGeometry(x, y, w, h)` for internal child widgets.
   - ✅ Always use Layout Managers (`QVBoxLayout`, `QHBoxLayout`, `QGridLayout`, `QFormLayout`).
