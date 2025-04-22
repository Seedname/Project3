import pathlib, pickle, json, csv, time, heapq, random
from collections import deque
from tqdm import tqdm
import matplotlib.pyplot as plt
from multiprocessing import Pool



path = pathlib.Path(__file__).parent
with open(path / "graph.data", 'rb') as f:
    graph = pickle.load(f)

with open(path / 'avg_popularities.json', 'r') as f:
    avg_popularities = json.load(f)

with open(path.parent / "frontend" / "actor_names_sorted.json", 'r') as f:
    names_to_ids: dict = json.load(f)

print("Loaded data")

def bfs(source: int, target: int):
    q = deque()
    q.append((source, []))
    seen = {source}
    # source is the current actor, 0 is the distance from source (not needed i think), [] contains the path taken
    while q:
        cur = q.popleft()
        for pair in graph[cur[0]]:
            actor = pair[0]
            movie = pair[1]
            if actor in seen:
                continue
            if actor == target:
                path = cur[1] + [[actor, movie]]
                return len(path)
            seen.add(actor)
            q.append((actor, cur[1]+[[actor, movie]]))

    return -1


def best_first_search(source: int, target: int):

    # if you are having issues running this it is probably this next line!
    target_pop = avg_popularities.get(str(target), 0)
    pq = []
    heapq.heappush(pq, (0, 0, source, []))
    seen = {source}
    # args: distance, priority (based on popularity), source, path taken
    while pq:
        cur = heapq.heappop(pq)
        for trip in graph[cur[2]]:
            actor = trip[0]
            movie = trip[1]
            popularity = trip[2]
            if actor in seen:
                continue
            if actor == target:
                path = cur[3] + [[actor, movie]]
                return len(path)
            seen.add(actor)
            heapq.heappush(pq, (cur[0]+1, abs(target_pop-popularity),
                           actor, cur[3]+[[actor, movie]]))

    return -1



def process_chunk(start_idx: int):
    end_idx = min(start_idx + chunk_size, total)
    chunk_items = items[start_idx:end_idx]

    res_file = out_dir / f"results_{start_idx}.txt"
    miss_file = out_dir / f"missing_{start_idx}.txt"

    with res_file.open("w") as rf, miss_file.open("w") as mf:
        buf_count = 0
        for name, other_id in chunk_items:
            if other_id == bacon:
                continue

            # --- best_first_search timing ---
            t0 = time.perf_counter()
            best_len = best_first_search(bacon, other_id)
            t_best = time.perf_counter() - t0

            # --- bfs timing ---
            t0 = time.perf_counter()
            bfs_len = bfs(bacon, other_id)
            t_bfs = time.perf_counter() - t0

            # write one CSV‐style line
            rf.write(f"{name},{other_id},{best_len},{t_best:.6f},"
                     f"{bfs_len},{t_bfs:.6f}\n")

            if best_len == -1 or bfs_len == -1:
                mf.write(f"{name}\n")

            buf_count += 1
            if buf_count >= flush_every:
                rf.flush()
                mf.flush()
                buf_count = 0

        # final flush
        rf.flush()
        mf.flush()



if __name__ == "__main__":
    out_dir = pathlib.Path(__file__).parent / "bench_chunks"
    bacon = names_to_ids["kevin bacon"]
    num_proc = 8                 # number of worker processes
    chunk_size = 100            # how many (name,id) pairs per worker
    flush_every = 1             # flush to disk every N results
    total = 10_000

    out_dir.mkdir(exist_ok=True)

    items = list(random.sample(list(names_to_ids.items()), total))

    starts = list(range(0, total, chunk_size))

    with Pool(num_proc) as pool:
        for _ in tqdm(pool.imap_unordered(process_chunk, starts), total=len(starts)):
            pass
