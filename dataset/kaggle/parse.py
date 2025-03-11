import pandas
import pathlib

if __name__ == "__main__":
    path = pathlib.Path(__file__).parent
    print("Reading csv...")
    df = pandas.read_csv(path.joinpath("names.csv"))
    
    print("Getting random sample of 100,000 actors...")
    ids = df['nconst'].sample(n=100_000, random_state=42)

    print(ids)