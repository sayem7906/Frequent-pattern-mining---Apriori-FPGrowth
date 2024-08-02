import copy
import time
import tracemalloc
class Apriori():
    minSupPer = 0.0
    inputFileName = ''
    dataset = []
    file = None
    first_candidate = dict()
    first_pat = []
    freq_pat_list = []
    next_level = 1
    root_node = None
    minSup = 0
    gen_pat = 0
    tot_pat = 0
    cand_count = 0
    ct = 0
    

    def loadTransections(self):
        file = open(self.inputFileName, 'r')
        for line in file:
            tns = line.strip().split()
            tmp_tns = []
            for itm in tns:
                tmp_tns.append(int(itm))
            tmp_tns.sort()
            # print(tmp_tns)
            self.dataset.append(tmp_tns)
            
            
    def __init__(self,minSupPer,inputFileName):
        self.minSupPer = minSupPer
        self.inputFileName = inputFileName
        self.dataset = []
        self.first_candidate = dict()
        self.first_pat = []
        self.freq_pat_list = []
        self.root_node = None
        pass
    
    def algorithm(self):
        
        self.loadTransections()
        self.minSup = round(self.minSupPer * len(self.dataset)/100)
        
        #print("init pat: ",self.tot_pat)
        #print("init data", len(self.dataset))
        
        t1 = time.time()
        tracemalloc.start()
        #1st candidate gen
        for itemset in self.dataset:
            for item in itemset:
                if item not in self.first_candidate:
                    self.first_candidate[item] = 1
                    #print(self.first_candidate[item])
                else:
                    self.first_candidate[item] += 1
                if(self.first_candidate[item] == self.minSup):
                    self.first_pat.append(item)
                    l = []
                    l.append(item)
                    self.freq_pat_list.append(l)
           
        self.first_pat.sort()
        
        self.tot_pat += len(self.first_pat)
        
        #build initial trie
        self.root_node = Node(None)        
        for label in self.first_pat:
            #etao thik ase
            self.add_child(self.root_node,label)
        print("Level : ",self.next_level)
        print("patterns: ",len(self.first_pat))
        print("candidates: ",len(self.first_pat))
        print("----------------------")
        #self.print_FS(self.root_node,[])
        self.next_level = 2
        
        #eta thik ase
        self.cand_count = 0
        self.gen_candidate(self.root_node,[],0)
        
        
        
        while True:
            #thik ase
            for transection in self.dataset:
                self.support_update(self.root_node, transection,0)
            #self.print_FS(self.root_node,[])
            
            self.gen_pat = 0
            self.gen_freq_pat(self.root_node,0)
            self.print_FS(self.root_node,[])
            
            print("Level : ",self.next_level)
            print("patterns: ",self.gen_pat)
            print("candidates: ",self.cand_count)
            print("----------------------")
            
            self.tot_pat += self.gen_pat
            
            if(self.gen_pat < self.next_level):
                break
            
            self.next_level += 1
            self.cand_count = 0
            self.gen_candidate(self.root_node, [], 0)
            #self.print_FS(self.root_node,[])
            print("--------------")
            
        t2 = time.time()
        print("total pattern : ",self.tot_pat)
        print("time : ",round(t2-t1,4))
        
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        
        print("Current memory : ",current/10**6)
        print("peak memory : ",peak/10**6)
        
        f = open("../Files/patterns_apriori_53.csv", 'a')
        f.write('-----------------\n')
        f.write(self.inputFileName)
        f.write('\n-----------------\n')
        f.write('minsup% : ')
        f.write(str(self.minSupPer))
        f.write('\n')
        f.write('patterns : ')
        f.write(str(len(self.freq_pat_list)))
        f.write('\n')
        for items in self.freq_pat_list:
            items.sort()
            f.write(str(items))
            f.write('\n')
        f.write('\nEND\n\n\n\n')
        f.close()
        
        
        
        return self.tot_pat, round(t2-t1,4), peak/10**6
    
    def gen_freq_pat(self, cur_node, cur_lvl):
        
        #cur_node.support = 0
        #cur_node.marker = False
        tmp_child = copy.deepcopy(cur_node.child)
        cur_node.child = dict()
        for child in tmp_child:
            #if(cur_lvl == self.next_level-1 and tmp_child[child].support < self.minSup):
             #   print("hoiseeee")
              #  del tmp_child[child]
            if (cur_lvl==self.next_level-1 and tmp_child[child].support >= self.minSup):
                cur_node.child[child] = tmp_child[child]
                #cur_node.child[child].support = 0
                self.gen_pat +=1
            if(cur_lvl < self.next_level-1):
                cur_node.child[child] = tmp_child[child]
                self.gen_freq_pat(tmp_child[child],cur_lvl+1)
                
            
            
    def support_update(self, cur_node, trn,cur_lvl):
        #cur_node.marker = False
        for child in cur_node.child:
            next_node = cur_node.child[child]
            if next_node.label in trn:
                if cur_lvl == self.next_level-1:
                    next_node.support += 1
                self.support_update(next_node, trn,cur_lvl+1)
    
    
    #porer duita function complexity beshi howar karone baad
    def update_sup(self):
        for transection in self.dataset:
            temp = copy.deepcopy(transection)
            
            self.update(self.root_node,temp,0)
            
                
                
    
    def update(self,cur_node,pat,pos):
        if pos == len(pat):
            return
        #
        
        
        if pat[pos] in cur_node.child:
            next_node = cur_node.child[pat[pos]]
            next_node.support += 1
            self.update(next_node, pat, pos+1)
                    
        self.update(cur_node,pat,pos+1)
        
    
    
    def gen_candidate(self,cur_node,prefix,cur_level):
        if cur_node.label is not None:
            prefix.append(cur_node.label)
        if(cur_level == self.next_level-2):
            labels = list(cur_node.child.keys())
            labels.sort()
            
            for i in range(len(labels)):
                for j in range(i+1,len(labels)):
                    candidate = copy.deepcopy(prefix)
                    candidate.append(labels[i])
                    candidate.append(labels[j])
                    #print(candidate)
                    self.pruning(candidate,cur_node)
                
            return
        
        for child in cur_node.child:
            temp = copy.deepcopy(prefix)
            self.gen_candidate(cur_node.child[child],temp,cur_level+1)
        




    def pruning(self,candidate,cur_node):
        for i in range(0, len(candidate)):
            tmp_cur = copy.deepcopy(candidate)
            del tmp_cur[i]
            ret = self.check_subpatterns(self.root_node, tmp_cur, 0)
            if ret is False:
                return
        
       # print("child added ",candidate[i-1]," ",candidate[i]) 
        self.cand_count += 1
        self.add_child(cur_node.child[candidate[i-1]],candidate[i])
    
    
    
    def check_subpatterns(self,cur_node,sub_pat,pos):
        if pos== len(sub_pat):
            return True
        if sub_pat[pos] not in cur_node.child:
            return False
        self.check_subpatterns(cur_node.child[sub_pat[pos]],sub_pat,pos+1)
    
    
    
    
    def add_child(self,cur_node,label):
        #cur_node.marker = False
        cur_node.child[label] = Node(label)
    
    def print_FS(self, cur_node, cur_set):
        if cur_node.label is not None:
            cur_set.append(cur_node.label)
            if len(cur_set) == self.next_level:
                #print(cur_set, " : ", cur_node.support)
                self.freq_pat_list.append(cur_set)
                return 1
        cnt = 0
        for child in cur_node.child:
            cnt += self.print_FS(cur_node.child[child], copy.deepcopy(cur_set))
        return cnt


class Node():

    def __init__(self,label):
        self.label = label
        self.support = 0
        self.child = dict()