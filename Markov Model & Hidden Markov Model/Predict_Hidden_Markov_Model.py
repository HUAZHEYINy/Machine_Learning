import numpy as np
from hmmlearn import hmm
import scipy.stats as stats

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
    #construct normal distribution for each city
    def prepare_dist(self, X, label):
        city_list = {key: [] for key in label.keys()}
        print city_list

        for s in X:
            for i in s:
                city_list.get(i[0]).append(i[1])
        for key in city_list.keys():
            print "City ",label[key],"  ", city_list.get(key)
        #print city_list
            
        #city_list is a dictionary
        # city  0 :[], city 1 :[]...
        keys = ['mean', 'std']
        nm_dist_list = [{'city' : i, 'mean': 0, 'std': 0} for i in range(5)]
        
        for i in range(5):
            nm_dist_list[i]['mean'] = np.mean(city_list[i])
            nm_dist_list[i]['std'] = np.std(city_list[i])
        
        print nm_dist_list
        
        #
        #list of dict
        #       [ {'mean': ?, 'std': ?, 'city_No: ?'}, {...}, {...}, {...}, {...} ]
        #
        return nm_dist_list
        
    #predict
    #   @parameter _X the spends
    #   @parameter nm_dist_list list of normal distribution distribution
        
    def predict(self, predict_x, nm_dist_list):
        current_pred = []   #store the current predicted sequence
        current_prob = 0    #store the current predicted probability 
        prob = []           #store all of the predicted brobability
        pred = []           #store all of the predicted sequence
        
        for i in range(5):
            
            for j in range(5):
                
                for k in range(5):
                    
                    for z in range(5):
                        current_prob = self.startprob[i] * stats.norm(nm_dist_list[i]['mean'], nm_dist_list[i]['std']).pdf(predict_x[0]) * \
                                        self.transmat[i][j] * stats.norm(nm_dist_list[j]['mean'], nm_dist_list[j]['std']).pdf(predict_x[1]) * \
                                        self.transmat[j][k] * stats.norm(nm_dist_list[k]['mean'], nm_dist_list[k]['std']).pdf(predict_x[2]) * \
                                        self.transmat[k][z] * stats.norm(nm_dist_list[z]['mean'], nm_dist_list[z]['std']).pdf(predict_x[3])
                        current_pred = [i , j, k, z]
                        
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

    X = [[[0, 60.44], [2, 159.67], [3, 231.84], [1, 346.4], [0, 18.82]],
         [[0, -200.04], [4, 52.7], [2, 537.1], [4, 109.82], [0, 142.08]],
         [[1, 79.09], [0, -195.59], [3, 177.49], [1, 620.13], [4, 100.25]],
         [[0,185.67], [2, 284.93], [1, 62.12], [0, 200.59], [2, 152.77]],
         [[0, 30.4], [3, 180.69], [0, -336.63], [2, 472.77], [4, 36.17]],
         [[0, 395.82], [2, 346.42], [0, 202.59], [3, 213.88], [1, 496.2]],
         [[1, 95.53], [0, 182.25], [4, 3.76], [3, 93.81], [0, 159.14]],
         [[1, 292.77], [0, 188.31], [2, -101.1], [3, 214.96], [1, -297.47]],
         [[4, 119.03], [3, 97.44], [1, 369.64], [3, 154.91], [2, 61.39]],
         [[3, 46.59], [4, -22.4], [0, -270.73], [4, 41.39], [3, 75.75]]
        ]
    for s in X:
        for i in s:
            print label[i[0]], " , ", i[1],"   ",
        print 
        
        
    mm = markovmodel()
    mm.fit(y)
    startprob = mm.startprob
    transmat = mm.transmat
    print startprob
    print transmat
    
    predict_x = [355, 339, 148, 50]
    nm_dist_list = mm.prepare_dist(X, label)
    sequence = mm.predict(predict_x, nm_dist_list)
    for x in predict_x:
        for i in nm_dist_list:
            print i['city'], " with ",x," pdf: ",stats.norm(i['mean'], i['std']).pdf(x)
    print  [label[i] for i in sequence]
    
