# StarChain

## Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/Seedname/StarChain
    cd StarChain
    ```

2. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```
    Required packages include:
    - `requests`
    - `python-dotenv`
    - `text-unidecode`
    - `tqdm`
    - `pandas`
    - `flask`
    - `scipy`
    - `matplotlib`

## Running the Application


### Generate the dataset

```sh
    cd dataset
    python combine_data.py # process the unbatched data
    python process_data.py # generate the adjacency list
    cp data/graph.data ../backend/ # Copy the adjacency list to the backend
    cp data/avg_popularities ../backend/ # Copy the average popularities of the movies the actors have been in to the backend
```


### Run the frontend

To run the frontend, we recommend using the "Live Server" extension on Visual Studio Code, and starting a server on index.html.

### Run the backend

The server runs on 127.0.0.1:8080. You may need to edit the CORS settings to allow the frontend to fetch this api. If using the Live Server extension, the port is :5500 by default, but you must modify it in server.js if the port is different.  

```sh
    cd backend
    python3 server.py
```


## Gathering data from themoviedb api

To collect data from themoviedb api when running `batch_query.py`, you must:
- Visit https://www.themoviedb.org/ 
- Request a API Token for your project
- Create a `.env` file in the `dataset/` directory with `READ_TOKEN={read_token}`
