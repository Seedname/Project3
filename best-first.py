import heapq
import json
adj = {
    # adj needs to be replaced with actual data
    1: [[2, 100, 0], [2, 200, 0], [3, 200, 0], [4, 300, 0], [4, 400, 0], [5, 300, 0], [5, 400, 0]],
    2: [[1, 100, 0], [1, 200, 0], [3, 200, 0]],
    3: [[1, 200, 0], [2, 200, 0]],
    4: [[1, 300, 0], [1, 400, 0], [5, 300, 0], [5, 400, 0]],
    5: [[1, 300, 0], [1, 400, 0], [4, 300, 0], [4, 400, 0]],
    6: [[7, 600, 0]],
    7: [[6, 600, 0]]

}


def best_first_search(source, target):
    # if you are having issues running this it is probably this next line!
    with open('dataset/kaggle/avg_popularities.json', 'r') as file:
        avg_popularities = json.load(file)
    target_pop = avg_popularities[target]
    pq = []
    heapq.heappush(pq, (0, source, []))
    seen = {source}
    # 0 is the popularity score, source is the current actor, [] contains the path taken
    while pq:
        cur = heapq.heappop(pq)
        for trip in adj[cur[1]]:
            actor = trip[0]
            movie = trip[1]
            popularity = trip[2]
            if actor in seen:
                continue
            if actor == target:
                return cur[2] + [[actor, movie]]
            seen.add(actor)
            heapq.heappush(pq, (abs(target_pop-popularity),
                           actor, cur[2]+[[actor, movie]]))
    return -1


print(best_first_search(5, 3))
