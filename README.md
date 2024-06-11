# CT Scan Superimposition Tool

A simple tool written in Python to visualise a large number of co-registered CT scans simultaneously to identify and
inspect inaccurate registrations and anomalous scans.

[//]: # (<style>)

[//]: # (table th:first-of-type {)

[//]: # (    width: 32.6%;)

[//]: # (})

[//]: # (table th:nth-of-type&#40;2&#41; {)

[//]: # (    width: 33.8%;)

[//]: # (})

[//]: # (table th:nth-of-type&#40;3&#41; {)

[//]: # (    width: 33.8%;)

[//]: # (})

[//]: # (</style>)

[//]: # (Superimpose             |     Binary mask overlay      |   Original co-registered scan            )

[//]: # (:-------------------------:|:----------------------------:|:-------------------------:)

[//]: # (![]&#40;/images/000_superimpose.png&#41;  | ![]&#40;/images/000_overlay.png&#41; |  ![]&#40;/images/000_registered_source_scan.png&#41;)

## Installation

Clone the repository:

```git clone https://github.com/bjin96/superimposition-tool.git```

Install the dependencies:

```pip install -r requirements.txt```

Make sure to install Qt5 by following the instructions in the <a href="https://doc.qt.io/qt-5/gettingstarted.html" target="_blank">Qt documentation</a>.

## Run

Set the variables in the `config.json`:

| Variable             | Description                                                                                                     |
|----------------------|-----------------------------------------------------------------------------------------------------------------|
| batch_size           | Number of scans that are superimposed at a time.                                                                |
| template_path        | Path to the template in NIfTI format (`.nii.gz`) to which all scans were co-registered.                         |
| blacklist_path       | Path to a file JSON file where the blacklisted paths are stored. The file will be created if it does not exist. |
| input_file_list_path | Path to a JSON file containing paths to the CT scans to be analysed.                                            |

The blacklist will have the format of:

```json
[
    {
        "file": "/path/to/the/blacklisted/file1.nii.gz",
        "reason": "First comment"
    },
    {
        "file": "/path/to/the/blacklisted/file2.nii.gz",
        "reason": "Second comment"
    },
    ...
]
```

The input file list must have the following format:

```json
[
  "/path/to/the/blacklisted/file1.nii.gz",
  "/path/to/the/blacklisted/file2.nii.gz",
  ...
]
```

Start the tool with
```
python run.py
```
