# SEI-ENERGY - Commercial-Energy

In this repository we provide all the code used to reproduce the results from the paper "Machine Learning Approaches for Estimating Commercial Building Energy Consumption" (in submission at Applied Energy), and to apply the trained models to new locations. We also provide instructions for downloading and organizing the free data sources included in our study.

The code is organized as follows:

`CBECSLib.py` - Contains several methods that are used by other files.

IPython notebooks:
- `Create CBECS datasets.ipynb`
     - Test
- `Feature importances.ipynb`
    - Generates 
- `Generate MFBTU distributions per PBA.ipynb`
- `Run experiments.ipynb`
- `Train models on CBECS.ipynb`
- `Variable tables.ipynb`
- `Generate dummy data.ipynb`
     - Generates dummy locations in Atlanta, GA for each row in CBECS.
     - The `Apply model.ipynb` notebook will use the dummy data to demonstrate how to apply our model to specific city data.
- `Apply model.ipynb`
- `NYC - Data centroids.ipynb`
- `NYC - Run experiments.ipynb`
- `NYC - Validation.ipynb`
- `NYC - Write joined PLUTO-LL84 dataset.ipynb`
     - Generates the joined PLUTO/LL84 dataset with HDD and CDD information from climate raster.
     - Because we cannot distribute


## Organizing External Data

We use the 2012 CBECS microdata, downloadable from [here](https://www.eia.gov/consumption/commercial/data/2012/index.php?view=microdata). We have included the `2012_public_use_data_aug2016.csv` file in `data/cbecs/`. If there is a more recent version of the data released, then our file should be replaced with it, and the appropriate filename references in `Create CBECS datasets.ipynb` should be updated.

Because of the large sizes of the PLUTO and LL84 datasets we do not include them in this repository. You must download and add them to the `data/nyc/` directory as follows:

- Goto [http://www.nyc.gov/html/gbee/html/plan/ll84_scores.shtml](http://www.nyc.gov/html/gbee/html/plan/ll84_scores.shtml) and download the "2016 Energy and Water Data Disclosure (Data for Calendar Year 2015)" spreadsheet. Export the downloaded file, "nyc_benchmarking_disclosure_data_reported_in_2016.xlsx", as a csv file with "|" delimiters to `data/nyc/nyc_benchmarking_disclosure_data_reported_in_2016.csv`.
- Goto [https://www1.nyc.gov/site/planning/data-maps/open-data/dwn-pluto-mappluto.page](https://www1.nyc.gov/site/planning/data-maps/open-data/dwn-pluto-mappluto.page)
    - Download "nyc_pluto_16v2.zip" (this is the PLUTO (.csv format) download) and unzip to `data/nyc/BORO_zip_files_csv/`. This directory should contain: "BK.csv", "BX.csv", "MN.csv", "QN.csv", and "SI.csv"
    - Download all of the individual borough shapefiles to `data/nyc/shapefiles/`. There should be 5 subdirectories in `data/nyc/shapefiles`: "bk_mappluto_16v2", "bx_mappluto_16v2", "mn_mappluto_16v2", "qn_mappluto_16v2", and "si_mappluto_16v2".

## Reproducing paper results

Use these steps to reproduce the experiments performed in the 