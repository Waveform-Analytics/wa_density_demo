# Exploring Animal Density Data

The data used in this project are from [MGEL Density Models: US East Coast](https://seamap.env.duke.edu/models/Duke/EC/). If you'd like to replicate this work, you can either download the full zip file containing all of the data, or you can download individual density files. The data in the data folder are all .gitignore'd because they're large. But the folders are organized as follows:

    |--data
        |-- density
            |-- Atlantic_spotted_dolphin_v9.1
            |-- Atlantic_white_sided_dolphin_v4.1
            |-- etc...

To provide examples of how you can extract relevant statistics, we're using shapefiles from [BOEM's Renewable Energy GIS Data site](https://www.boem.gov/renewable-energy/mapping-and-data/renewable-energy-gis-data)

## References for Data Sources
Roberts JJ, Best BD, Mannocci L, Fujioka E, Halpin PN, Palka DL, Garrison LP,
Mullin KD, Cole TVN, Khan CB, McLellan WM, Pabst DA, Lockhart GG (2016)
Habitat-based cetacean density models for the U.S. Atlantic and Gulf of
Mexico. Scientific Reports 6: 22615. doi: 10.1038/srep22615

Roberts JJ, Yack TM, Halpin PN (2023) Marine mammal density models for the
U.S. Navy Atlantic Fleet Training and Testing (AFTT) study area for the Phase
IV Navy Marine Species Density Database (NMSDD). Document version 1.3. Report
prepared for Naval Facilities Engineering Systems Command, Atlantic by the
Duke University Marine Geospatial Ecology Lab, Durham, NC
