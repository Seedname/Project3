from collections import deque
adj={
	#adj needs to be replaced with actual data
    1:[[2,100],[2,200],[3,200],[4,300],[4,400],[5,300],[5,400]],
    2:[[1,100],[1,200],[3,200]],
    3:[[1,200],[2,200]],
    4:[[1,300],[1,400],[5,300],[5,400]],
    5:[[1,300],[1,400],[4,300],[4,400]],
	6:[[7,600]],
	7:[[6,600]]

}

def bfs(source, target):
	q=deque()
	q.append((source,[]))
	seen={source}
	#source is the current actor, 0 is the distance from source (not needed i think), [] contains the path taken
	while q:
		cur=q.popleft()
		for pair in adj[cur[0]]:
			actor=pair[0]
			movie=pair[1]
			if actor in seen:
				continue
			if actor==target:
				return cur[1] + [[actor, movie]]
			seen.add(actor)
			q.append((actor,cur[1]+[[actor,movie]]))
	return -1
			
print(bfs(5,3))
