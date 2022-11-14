# ASEBAtranscription

This is a script and library for transcribing ASEBA (CBCL/YSR) data that has been entered in to REDcap or another tabular format in to a JSON file that can be imported into the ASEBA scoring software for scoring. To be clear, this will not score the instruments for you, it simply allows you to avoid manually transcribing the data in to ASEBA from another source.

This product is not endorsed in any way by Thomas Achenbach, the Research Center for Children, Youth, & Families, or the University of Vermont. It is provided for non-commercial use and at your own risk, with no guarantees as to the quality of the resulting data.

# Usage

python3 TranscribeAseba.py (mapping) (cbcl) (ysr)

* mapping: specify the CSV file with the study variable mappings.
* cbcl: Specify the CSV with the CBCL school age (6-18) form data.
* ysr: Specify the CSV with the YSR school age (6-18) form data.

Output json will be written to the 'output/' folder.

# Dependencies:

The following packages are required:

* json
* csv
* argparse
* pprint
* warnings
* time
* numpy




