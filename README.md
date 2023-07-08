Natürlich! Hier ist der gesamte Code in Markdown-Syntax:

```markdown
## User Button Control

This script (`d_usr_button_ctrl.py`) provides control for a user button and display using the power LED on the Raspberry Pi.

### Prerequisites

- Raspberry Pi
- Python 3.x
- RPi.GPIO library

### Installation

1. Clone the repository:

   ```
   git clone <repository_url>
   ```

2. Navigate to the project directory:

   ```
   cd <project_directory>
   ```

3. Install the required dependencies:

   ```
   pip install RPi.GPIO
   ```

### Usage

Run the script using the following command:

```
python d_usr_button_ctrl.py [-h] [-i INPUT] [-t TIMES] [-b BLINK_PERIODS] [-c COMMANDS]
```

#### Arguments

- `-h`, `--help`: Show the help message and exit.
- `-i INPUT`, `--input INPUT`: Raspberry Pi input channel (default: 22).
- `-t TIMES`, `--times TIMES`: Time within the action shall occur (default: [5, 10, 15]).
- `-b BLINK_PERIODS`, `--blink_periods BLINK_PERIODS`: Blink time periods in milliseconds. The blink time means the time for ON plus the same time for OFF (default: [500, 250, 50]).
- `-c COMMANDS`, `--commands COMMANDS`: Actions to be executed if the button is released within the given time (default: ['echo No action 1', 'echo No action 2', 'sudo poweroff']).

**Example:**

```
python d_usr_button_ctrl.py -i 22 -t [5, 10, 15] -b [500, 250, 50] -c ['echo No action 1', 'echo No action 2', 'sudo poweroff']
```

**CAUTION:** The count of `blink_periods` must be the same as `times` and `commands`.

### License

This project is licensed under the MIT License.
```