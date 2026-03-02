# CT Scan Superimposition Tool

A simple tool written in Python to visualise a large number of co-registered CT scans simultaneously to identify and
inspect inaccurate registrations and anomalous scans. The tool is part of a larger pre-processing and quality control
pipeline described in [Jin et al.](https://link.springer.com/chapter/10.1007/978-3-031-73748-0_8), which is available
in the [ct-processing repository](https://github.com/bjin96/ct-processing).

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
  "/path/to/the/file1.nii.gz",
  "/path/to/the/file2.nii.gz",
  ...
]
```

Start the tool with
```
python run.py
```

# Acknowledgment and Citation

The work was funded by the UK Medical Research Council's Doctoral Training Programme in Precision Medicine [MR/W006804/1].

```
Jin, B., Valdés Hernández, M.D.C., Fontanella, A., Li, W., Platt, E., Armitage, P., Storkey, A., Wardlaw, J.M., Mair, G., 2025. Pre-processing and Quality Control of Large Clinical CT Head Datasets for Intracranial Arterial Calcification Segmentation, in: Bhattarai, B., Ali, S., Rau, A., Caramalau, R., Nguyen, A., Gyawali, P., Namburete, A., Stoyanov, D. (Eds.), Data Engineering in Medical Imaging, Lecture Notes in Computer Science. Springer Nature Switzerland, Cham, pp. 73–83. https://doi.org/10.1007/978-3-031-73748-0_8
```
