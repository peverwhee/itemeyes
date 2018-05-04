# decision calculator!

def main():
	print("Hi! Please input your weights for each criterion. The weights are decimals that sum to 1.")
	print("For example, giving Request Latency a weight of 1 means you care about nothing but minimizing latency.")
	while(True):
		latency=input("REQUEST LATENCY: ")
		cost=input("COST: ")
		portability=input("PORTABILITY: ")
		scalability=input("SCALABILITY: ")
		difficulty=input("DEPLOYMENT DIFFICULTY: ")
		size=input("SIZE FLEXIBILITY: ")
		total = latency + cost + portability + scalability + difficulty+size
		if (total !=1):
			print("entered values don't sum to 1!");
		else:
			break;
	# [app engine, kubernetes, f1-micro, g1-small]
	# 4 is highest score, 1 is lowest
	latencyScores=[4, 3, 1, 2]
	costScores=[2, 1, 4, 3]
	portabilityScores=[3, 2, 4, 4]
	scalabilityScores=[4, 3, 1, 2]
	difficultyScores=[3, 2, 4, 4]
	sizeScores=[4,4,2,3]

	AEScore=latencyScores[0]*latency+costScores[0]*cost+portabilityScores[0]*portability+scalabilityScores[0]*scalability+difficultyScores[0]*difficulty+sizeScores[0]*size
	KScore=latencyScores[1]*latency+costScores[1]*cost+portabilityScores[1]*portability+scalabilityScores[1]*scalability+difficultyScores[1]*difficulty+sizeScores[1]*size
	fScore=latencyScores[2]*latency+costScores[2]*cost+portabilityScores[2]*portability+scalabilityScores[2]*scalability+difficultyScores[2]*difficulty+sizeScores[2]*size
	gScore=latencyScores[3]*latency+costScores[3]*cost+portabilityScores[3]*portability+scalabilityScores[3]*scalability+difficultyScores[3]*difficulty+sizeScores[3]*size
	print("\n")
	print("App Engine: {}").format(AEScore)
	print("Kubernetes Engine: {}").format(KScore)
	print("Compute Engine (f1-micro): {}").format(fScore)
	print("Compute Engine (g1-small): {}").format(gScore)



if __name__ == '__main__':
	main()