# Jamazon - Event Manager 📅🚀

**Jamazon** (also known as *Dynamic Events*) is a desktop application developed in Python for the efficient management of events and resources. It uses a modern graphical interface and advanced data structures to handle scheduling and avoid resource conflicts.

## 🌟 Key Features

* **Task Management:** Easily create and delete tasks.
* **Event Definition:** Schedule events with specific date and time ranges.
* **Resource Management:** Add resources and handle dependencies between them.
* **Conflict Detection:** Intelligent system that checks if necessary resources are available and do not conflict with other rules.
* **Modern Interface:** Dark and friendly GUI based on `customtkinter`.

## 🛠️ Installation and Execution

Follow these steps to run the application in your local environment:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/VIRUSGAMING64/Jamazon.git
   cd Jamazon
   ```

2. **Install dependencies:**
   Make sure you have Python installed. Then, install the necessary libraries:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**

   ```bash
   python main.py
   ```

## 📖 Usage Guide

Upon starting the application, you will see a control panel with the following options:

* **Create new task:** Opens a form to register a new task in the system.
* **Remove existing task:** Allows deleting tasks that are no longer needed.
* **Add Resource:** Adds new resources (e.g., rooms, equipment) that can be assigned to events.
* **Define new event:** Creates complex events that require resources and have a specific duration. The system will automatically validate if resources are available and if there are dependency conflicts.

## 🧠 Technical Details and Modules

The project is built with a modular approach. The main components are detailed below:

### 1. Core (`modules/`)

* **`app` (in `main.py`)**:
  * It is the main window of the application.
  * Configures the interface, loads images, and manages navigation to other tools.

* **`Calendar` (in `modules/calendar.py`)**:
  * Manages the list of active events and used resources.
  * Handles saving and loading the application state.
  * Coordinates task availability.

* **`event` (in `modules/events.py`)**:
  * Represents an individual event with date, time, and necessary resources.
  * **Validation:** Checks dependencies and resource collisions upon initialization. If there is a conflict, it prevents the event creation.

### 2. Graphical Interface (`modules/gui_core/`)

* **`EventCreator` (in `EventDefiner.py`)**: Window to enter details for new events.
* **`TaskCreator`**: Interface to register new tasks in the system.
* **`TaskRemover`**: Interface to delete existing tasks.
* **`ResAdder`**: Allows adding new resources to the database (`resources.json`).

## 📂 Project Structure

```text
Jamazon/
├── changelog           # Project change log
├── clean.py            # Script to clean temporary files
├── logs.txt            # Error and event log file
├── main.py             # 🏁 Main entry point of the application
├── README.md           # Project documentation
├── requirements.txt    # List of Python dependencies
├── test.py             # Script for quick tests
├── modules/            # 🧠 Logical core of the system
│   ├── __init__.py
│   ├── calendar.py     # Calendar logic and availability
│   ├── events.py       # Event class definition and validations
│   ├── gvar.py         # Global variables
│   ├── iohandler.py    # Base handlers and utilities
│   ├── SegTree.py      # Segment Tree implementation
│   ├── utils.py        # General utility functions
│   └── gui_core/       # 🎨 Graphical Interface Components
│       ├── __init__.py
│       ├── EventDefiner.py   # Window to define new events
│       ├── Showers.py        # Event viewer
│       ├── ResAdder.py       # Window to add resources
│       ├── TaskCreator.py    # Window to create tasks
│       └── TaskRemover.py    # Window to delete tasks
├── saved/              # Folder for saved data
├── templates/          # 📄 Templates and static data
│   ├── resources.json  # Database of available resources
│   └── tasks.json      # Database of saved tasks
└── tests/              # 🧪 Unit tests
```

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=VIRUSGAMING64/Jamazon&type=date&legend=top-left)](https://www.star-history.com/#VIRUSGAMING64/Jamazon&type=date&legend=top-left)

---
Developed by [VIRUSGAMING64](https://github.com/VIRUSGAMING64)
