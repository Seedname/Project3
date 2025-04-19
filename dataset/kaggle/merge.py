import pathlib
import json
from text_unidecode import unidecode
from tqdm import tqdm
import pandas

if __name__ == "__main__":
    path = pathlib.Path(__file__).parent
    outputs_folder = path.joinpath("movies")

    
    total_length = 0
    output_ids = []

    for file_path in tqdm(outputs_folder.glob("*.txt"), total=len([*outputs_folder.glob("*.txt")])):
        with open(file_path, 'r') as file:
            for line in file:
                if line == "\n": continue
                # id = str(list(json.loads(line).values())[0][0]["id"])
                # output_ids.append(id)

                total_length += 1

    df = pandas.DataFrame(output_ids, columns=["nproc"])

    df.to_csv(path.joinpath("ids.csv"), index=False)
    print("Unique data points:", total_length)