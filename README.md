# Movie Recommendation System using Content-Based
I used Content-Based Method for creating a Movies Recommender System. This is a web application that can recommend various kinds of similar movies

## Dataset has been used:

* [Dataset link](https://www.kaggle.com/tmdb/tmdb-movie-metadata?select=tmdb_5000_movies.csv)

## Demo:
<img src="images/0.png" alt="workflow" width="70%">

<img src="images/1.png" alt="workflow" width="70%">

<img src="images/2.png" alt="workflow" width="70%">

<img src="images/3.png" alt="workflow" width="70%">

## How to run the app
### STEPS:

Clone the repository

```bash
git clone https://github.com/VuBacktracking/Movie-Content-based-RecSys.git
```
### STEP 01- Create a conda environment after opening the repository

```bash
# you can use the other version of python but at least 3.7.10
conda create -n movie python=3.7.10 -y
```

```bash
conda activate movie
```


### STEP 02- install the requirements
```bash
pip install -r requirements.txt
```


```bash
#run this file to generate the models

Movie RecSys.ipynb
```

Now run,
```bash
streamlit run app.py
```# Movie-Recommeder-System
