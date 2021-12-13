# Otakube MSE Converter

This is a tool to convert  Otakube design sheets into a [Macig Set Editor](https://magicseteditor.boards.net/) format

This project includes a version of MSE that is both used to generate the set file, and it contains some customisations like liquid mana already in place.

## Installation

Requires python 3

Recomend using python virtual env for installation

```bash
python -m  venv ./venv
./venv/Scripts/activate
pip install -r ./requirements.txt
```

## Usage

Download the sheet from google spreasheets as csv and place it in the folder. Then run the following command (where csv)

```
python  ./mse_generate.py --csv_file path_to_downloaded.csv
```

It will generate a mse-set file containing the set named otakube.mse-set, invidual card pictures under export_otakube and sheets ready for table top simulator in 7x11 grid under sheets  folder.

To print the set you can use the included  MSE. With MSE, open the generated otakube.mse-set file. You can print the set from File -> Print

It can be a good idea to first print to a pdf file to generate it, and check that everything looks okay.

## Parameters
```
-P  (WIP) generate a 3x3 A4 printable file (work in progress)
-T (WIP) Generate a token sheet, currently does not work with csv
-U upload generated print sheets, usefull for uploading to a remote server to be used with TTS, it will run a upload.py file in the root of the project which you have to create
```

## License
[MIT](https://choosealicense.com/licenses/mit/)