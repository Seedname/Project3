import pandas
import pathlib
import json
from tqdm import tqdm
from multiprocessing import Pool
import pull as db

def get_actor_names(start_index: int, chunk_size: int, buffer_size: int) -> list:
    with open(pathlib.Path(__file__).parent.joinpath(f"actors/result_{start_index}.txt"), "w") as f:
        buffer = ""

        for i in range(start_index, min(start_index + chunk_size, len(df["nconst"].values))):
            id = str(df["nconst"].values[i])

            try:
                result = db.get_people_from_page(id)
                buffer += json.dumps(result) + "\n"
            except ValueError as e:
                # print(f"Something went wrong on the server: {e}")
                continue
            except LookupError as e:
                # print(str(e))
                continue


            if i % buffer_size == 0:
                f.write(buffer)
                f.flush()
                # print(start_index, i)
                buffer = ""

        f.write(buffer)
        f.flush()


def get_actor_names(start_index: int, chunk_size: int, buffer_size: int) -> list:
    with open(pathlib.Path(__file__).parent.joinpath(f"movies/result_{start_index}.txt"), "w") as f:
        buffer = ""

        for i in range(start_index, min(start_index + chunk_size, len(df["nconst"].values))):
            id = str(df["nconst"].values[i])

            try:
                result = db.get_movies_from_themoviedb_id(id)
                buffer += json.dumps(result) + "\n"
            except ValueError as e:
                # print(f"Something went wrong on the server: {e}")
                continue
            except LookupError as e:
                # print(str(e))
                continue


            if i % buffer_size == 0:
                f.write(buffer)
                f.flush()
                # print(start_index, i)
                buffer = ""

        f.write(buffer)
        f.flush()


def main() -> None:
    print("Querying themoviedb...")
    chunk_size = 1_000
    buffer_size = 10
    num_proc = 16
    
    entry_chunk = 0
    num_batches = 248
    for starting_chunk in tqdm(range(entry_chunk, entry_chunk + num_proc * chunk_size * num_batches, num_proc * chunk_size), desc="Processing chunks"):
        with Pool(processes=num_proc) as pool:
            pool.starmap(
                get_actor_names,
                [(starting_chunk + i * chunk_size, 
                chunk_size,
                buffer_size
                ) for i in range(num_proc)]
            )

    print("Done querying themoviedb.")


if __name__ == "__main__":
    path = pathlib.Path(__file__).parent.joinpath("data")
    print("Reading csv...")
    df = pandas.read_csv(path.joinpath("ids.csv"))

    main()