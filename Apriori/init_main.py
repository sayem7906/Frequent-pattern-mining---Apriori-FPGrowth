import os,errno
from Apriori import Apriori 

def ffopen(fileLocation, mode, title=None):
    # if not os.path.exists(os.path.dirname(fileLocation)):
    if not os.path.exists(fileLocation):
        try:
            os.makedirs(os.path.dirname(fileLocation))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
        f = open(fileLocation, mode)
        if title is None:
            title = input('Creating New File, Enter Title: ')
        f.write(title)
        f.close()

    f = open(fileLocation, mode)
    return f

if __name__ == '__main__':
    datasets = ['mushroom.txt', 'chess.txt', 'retail.txt', 'kosarak.txt', 'accidents.txt']
    #datasets = ['retail.txt']
    minSupPerT = [[35.0,30.0,25.0,20.0],[90.0,85.0,80.0,75.0],[1.5,1.25,1.0,.75],[2.0,1.5,1.0,0.5],[90.0,85.0,80.0,75.0]]
    #minSupPerT = [[1.0]]
    open('../Files/result_apriori_53.csv','w').close()
    open("../Files/patterns_apriori_53.csv", 'w').close()
    ct = 0
    for idx,dataset in enumerate(datasets):
        
        print(dataset)
        for minSupPer in minSupPerT[idx]:
            #minSupPer = float(input('Enter min_sup in %: '))
            #if minSupPer<=0.0:
             #   break
            inputFile = '../Files/'+dataset
            
            print(inputFile)
            print("minsup : ",minSupPer)
            #algo = Apriori(minSupPer,inputFile)
            algo = Apriori(minSupPer,inputFile)
            tot_pat,time,memory = algo.algorithm()
            
            #save output
            output_file = '../Files/result_apriori_53.csv'
            title = 'dataset,min_sup %,Total Patterns,Apriori time,Apriori memory\n'
            outf = open(output_file,'a')
            if ct == 0:
                ct += 1
                outf.write(title)
            buffer_s = dataset.replace('.txt','') + ',' + str(minSupPer) + ',' + str(tot_pat) +','+ str(time) +','+ str(memory) + '\n'
            print('writing into file...')
            outf.write(buffer_s)
            outf.close()
        
        
        #chess,mushroom dense
        # 