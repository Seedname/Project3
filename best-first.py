# note: currently does not work
# todo: implement movie popularity lookup, avg popularity of actor lookup

import heapq
adj = {
    # adj needs to be replaced with actual data
    1: [[2, 100], [2, 200], [3, 200], [4, 300], [4, 400], [5, 300], [5, 400]],
    2: [[1, 100], [1, 200], [3, 200]],
    3: [[1, 200], [2, 200]],
    4: [[1, 300], [1, 400], [5, 300], [5, 400]],
    5: [[1, 300], [1, 400], [4, 300], [4, 400]],
    6: [[7, 600]],
    7: [[6, 600]]

}


def best_first_search(source, target):
    pq = []
    heapq.heappush(pq, (0, source, []))
    seen = {source}
    # 0 is the popularity score, source is the current actor, [] contains the path taken
    while pq:
        cur = heapq.heappop(pq)
        for pair in adj[cur[1]]:
            actor = pair[0]
            movie = pair[1]
            if actor in seen:
                continue
            if actor == target:
                return cur[2] + [[actor, movie]]
            seen.add(actor)
            # replace 0 with abs(target avg popularity - movie popularity)
            heapq.heappush(pq, (0, actor, cur[2]+[[actor, movie]]))
    return -1


print(best_first_search(5, 3))
