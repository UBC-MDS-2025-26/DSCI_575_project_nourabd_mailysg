# Video Game Product Query Assistant

## Overview

This project builds a web app through which users can interact with a product query assistant that implements BM25 and semantic search to retrieve product recommendations.


## Dataset Description

The dataset that is being used in this project is the Video Games category from the Amazon Reviews dataset, collected in 2023 by [McAuley Lab](https://cseweb.ucsd.edu/~jmcauley/). This dataset contains 2.8M user reviews and 137.2k items.
It can be found and downloaded at the following address : [amazon-reviews-2023](https://amazon-reviews-2023.github.io)


## Data Preprocessing

The preprocessing implementation can be found in the [src/preprocess.py](src/preprocess.py) module.

The preprocessing steps are as follows :
- process the item meta data :
    - extract item type, ESRB rating and date first available from `details` field from the item meta data 
    - change the `price` field type to string 
    - drop unused columns 
    - rename title `column` to `item_title`
- process the user reviews :
    - keep only verified purchases (`verified_purchase==True`)
    - drop unused columns 
    - rename title `column` to `review_title`
    - group reviews by product
- merge the two datasets (user reviews and item meta data) 
- preprocess the data
    - transform text to lowercase
    - removes all elements that aren't lowercase letters, numbers or whitespace
    - if the given text is a list, transforms it into a string

More information about preprocessing can be found in the [Data exploration and preprocessing](notebooks/milestone1_exploration.ipynb) notebook.

The following fields were used in the product retrieval workflow:


- User reviews :
    - title
    - text
    - parent_asin
    - verified_purchase
- Item meta data:
    - title
    - average_rating
    - rating_number
    - features
    - description
    - price
    - store
    - categories
    - details
    - parent_asin

More information about field selection can be found in the [Data exploration and preprocessing](notebooks/milestone1_exploration.ipynb) notebook.

### Sample Size Selection
Due to storage and memory constraints, only the first 400k rows of the processed data were used in the following workflow.

To change the amount of data used, follow the instructions below :
1. Follow the link to the [src/preprocess.py](src/preprocess.py) module
2. At the bottom of the module, change the `sample_size` argument of the `merged` function to the desired size.

## Instructions

### Downloading the datasets
To download the data, follow the instructions below :
1. Clink on the link to navigate to the Video Games dataset website : [Video Games dataset](https://amazon-reviews-2023.github.io/#:~:text=review%2C%20meta-,Video_Games,-2.8M)

2. Download the files by clicking on `review` and `meta` (as pictured below)

    ![alt text](results/img/data_download.png)

You should now have 2 files downloaded : `Video_Games.jsonl` and `meta_Video_Games.jsonl`

Instructions for loading the dataset can be found here : [Loading instructions](https://amazon-reviews-2023.github.io/#quick-start)

### Setting up
To set up the workflow, follow the instructions below :

1. Clone the repository :

    ```bash
    git clone https://github.com/UBC-MDS/DSCI_575_project_nourabd_mailysg.git
    ```

2. Navigate to the project directory locally :

    ```bash
    cd DSCI_575_project_nourabd_mailysg
    ```

3. Install the required dependencies :

    ```bash
    conda env create -f environment.yml
    conda activate 575-proj
    ```

4. Put the files `Video_Games.jsonl` and `meta_Video_Games.jsonl` downloaded above in the `data/raw` folder 

### Running the workflow
To run the workflow, follow the instructions below :

1. Create the preprocessed corpus :

    ```{bash}
    python src/preprocess.py
    ```

2. Run the retrieval workflows :
    - BM25 search  :
    
    ```{bash}
    python -m src.bm25 
    ```
    - Semantic search  :
    
    ```{bash}
    python -m src.semantic 
    ```

The results of the workflows can be found in the [results](results) folder.

### Running the App
To run the web app, follow the instructions below :

1. To run the app locally :
    ```{bash}
    streamlit run app/app.py 
    ```
2. This should automatically open a new window with the web app in your browser.
3. To stop the app, press `ctrl` + `C` in the terminal. 

#### Memory constraints
In some cases (machines with low RAM) the web app crashes when loading both the BM25 and FAISS indices. If that situation occurs, here are 2 solutions :
- Re-run the workflow with a smaller sample size 
    - follow steps detailed in the [Sample Size Selection](#sample-size-selection) section
- Use a smaller sample size for the BM25 search
    - follow steps detailed in the [app](app/app.py) module