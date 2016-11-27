import numpy as np
class markovmodel:
    def __int__(self, transmat = None, startprob = None):
        self.transmat = transmat
        self.startprob = startprob

    def fit(self, X):
        ns = max([max(items) for items in X]) + 1
        self.transmat = np.zeros([ns, ns])
        self.startprob = np.zeros([ns])
        for items in X:
            n = len(items)
            self.startprob[items[0]] += 1

            for i in range(n-1):
                self.transmat[items[i] , items[i+1]] += 1
                
        self.startprob = self.startprob / sum(self.startprob)

        n = self.transmat.shape[0]
        d = np.sum(self.transmat, axis = 1)
        for i in range(n):
            if d[i] == 0:
                self.transmat[i,:] = 1.0 / n
        d[d == 0] == 1
        self.transmat = self.transmat * \
                        np.transpose(np.outer(np.ones([ns,1]), 1./d))
'''
    def predict(self, obs, steps):
        pred = []
        n = len(obs)
        #determine whether we have specified the starting city
        if len(obs) > 0:
            s = obs[-1]
        else:
            s = np.argmax(np.random.multinomial(1,
                                                self.startprob.tolist(), size = 1))
        #random with the probability
        for i in range(steps):
            s1 = np.random.multinomial(1, self.transmat[s,:].tolist(),
                                       size = 1)
            #print s1
            pred.append(np.argmax(s1))
            print pred[-1]
            s = np.argmax(s1)
        return pred
'''
    #find the sequence of four cities that has the largest probability
    def find_sequence_four_cities(self):
        current_pred = []
        current_prob = 0
        prob = []
        pred = []

        for i in range(5):
            
            for j in range(5):
                
                for k in range(5):
                    
                    for z in range(5):
                        current_prob = self.startprob[i] * self.transmat[i][j] * self.transmat[j][k] * self.transmat[k][z]
                        current_pred = [i, j, k, z]
                        
                        prob.append(current_prob)
                        pred.append(current_pred)

                        current_prob = 0
                        current_pred = []

        print "The prob: "
        print prob
        print "The sequence: "
        print pred

        print "The max prob: ", max(prob)
        index = np.argmax(prob)
        return pred[index]
            


if __name__ == "__main__":
    label = {0: "Albany", 1: "Boston", 2: "Washington D.C.", 3: "Philadephia", 4: "New York City"}
    y = [[0, 2, 3, 1, 0],
         [0, 4, 2, 4, 0],
         [1, 0, 3, 1, 4],
         [0, 2, 1, 0, 2],
         [0, 3, 0, 2, 4],
         [0, 2, 0, 3, 1],
         [1, 0, 4, 3, 0],
         [1, 0, 2, 3, 1],
         [4, 3, 1, 3, 2],
         [3, 4, 0, 4, 3]
        ]
    for x in y:
        print [label[s] for s in x]
    mm = markovmodel()
    mm.fit(y)
    print mm.transmat
    print
    print mm.startprob
    pred = mm.find_sequence_four_cities()
    print [label[s] for s in pred]
