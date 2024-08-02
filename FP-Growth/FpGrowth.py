import copy
import time
import tracemalloc

class FpGrowth():
    minSupPer = 0.0
    inputFileName = ''
    dataset = []
    trans_freq = []
    file = None
    freq_items = dict()
    first_pat = []
    freq_pat_list = []
    next_level = 1
    root_node = None
    minSup = 0
    gen_pat = 0
    tot_pat = 0
    count = 0
    

    def loadTransections(self):
        file = open(self.inputFileName, 'r')
        idx = 0
        for line in file:
            tns = line.strip().split()
            self.trans_freq.append(1)
            idx += 1
            tmp_tns = []
            for itm in tns:
                tmp_tns.append(int(itm))
            
            # print(tmp_tns)
            
            self.dataset.append(tmp_tns)
            
            
    def __init__(self,minSupPer,inputFileName):
        self.minSupPer = minSupPer
        self.inputFileName = inputFileName
        self.dataset = []
        self.trans_freq = []
        self.freq_items = dict()
        self.first_pat = []
        self.freq_pat_list = []
        self.root_node = None
        pass
    
    
    
    def algorithm(self):
        
        self.loadTransections()
        self.minSup = round(self.minSupPer * len(self.dataset)/100)
        #print(self.minSup)
        
        #print(self.dataset)
        #print("---------------")
        #print(self.trans_freq)
        
        
        t1 = time.time()
        tracemalloc.start()
        
        root_node,freq_items = self.build_trie(self.dataset,self.trans_freq)
        if(freq_items != None):
            #print(freq_items.keys())
            self.mining(freq_items,[])
        print("frequent patterns : ",len(self.freq_pat_list))
        
        t2 = time.time()
        print("time : ",round(t2-t1,4))
        print("-----------------------")
        print("-----------------------")
        
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        f = open("../Files/patterns_fpgrowth_53.csv", 'a')
        f.write('-----------------\n')
        f.write(self.inputFileName)
        f.write('\n-----------------\n')
        f.write('minsup% : ')
        f.write(str(self.minSupPer))
        f.write('\n')
        for items in self.freq_pat_list:
            items.sort()
            f.write(str(items))
            f.write('\n')
        f.write('\nEND\n\n\n\n')
        f.close()
            
        
        return len(self.freq_pat_list), round(t2-t1,4), peak/10**6
        #print("Current memory : ",current/10**6)
        #print("peak memory : ",peak/10**6)
        
        
    def gen_prefix(self,node,prefix):
        prefix.append(node.label)
        if node.parent.label != -1:
            #prefix.append(node.label)
            self.gen_prefix(node.parent, prefix)
        
        
    
    
    def gen_con_pat(self,item,freq_items):
        # First node in linked list
        node = freq_items[item][1] 
        condPats = []
        frequency = []
        while node != None:
            prefixPath = []
            # From leaf node all the way to root
            if(node.parent.label != -1):
                
                self.gen_prefix(node.parent, prefixPath)  
                # Storing the prefix path and it's corresponding count
                if(len(prefixPath)>0):
                    condPats.append(prefixPath)
                    frequency.append(node.support)
        
            # Go to next node
            node = node.next  
        return condPats, frequency
        
        
    
    
    def mining(self,freq_items, suffix):
        freq_items_head = dict(sorted(freq_items.items(), key=lambda item: item[1][0]))
        # if(len(suffix)==1):
        #     print(suffix[len(suffix)-1])
        #     print(freq_items.keys())
        #     print("------------")
        #print(self.count)
        #print(suffix)
        #self.count += 1
        
        for item in freq_items_head:
            
            
            freq_pat = copy.deepcopy(suffix)
            
            freq_pat.append(item)
            
            #freq_pat.reverse()
            #print(freq_pat)
            self.freq_pat_list.append(freq_pat)
            
            cond_dataset, cond_freq = self.gen_con_pat(item,freq_items)
            #print(item)
            
            
            new_root, new_freq_items = self.build_trie(cond_dataset, cond_freq)
            
            #print(new_freq_items)
            if(new_freq_items is not None):
                #freq_pat.reverse()
                self.mining(new_freq_items,freq_pat)
        
        
        
        
        
            
        
    
    def build_trie(self,dataset,trans_freq):
        
        #print(dataset)
        #print("---------------")
        #print(trans_freq)
        freq_items = dict()
        for idx,itemset in enumerate(dataset):
            for item in itemset:
                if item not in freq_items:
                    freq_items[item] = trans_freq[idx]
                    #print(freq_items[item])
                else:
                    freq_items[item] += trans_freq[idx]
        #print(freq_items)
        #freq_items = sorted(freq_items,key = freq_items.get,reverse = True)
        freq_items = dict(sorted(freq_items.items(), key=lambda item: item[1],reverse = True))
        
        
        dataset,freq_items,trans_freq = self.update_dataset(dataset,freq_items,trans_freq)
        if(len(freq_items) == 0):
            return None, None
        
        
        
        freq_items_head = dict()
        for items in freq_items:
            freq_items_head[items] = [freq_items[items] , None]
            #print(freq_items_head[items])
            # [frequency,head node] of that item
        
        
        root_node  = Node(-1,0,None)
        
        for idx,transection in enumerate(dataset):
            cur_node = root_node
            for item in transection:
                cur_node = self.update_trie(item,cur_node,freq_items_head,trans_freq[idx])
        
        #self.print_FS(root_node,[])
        
        return root_node, freq_items_head
                
        
        
        
    def print_FS(self, cur_node, cur_set):
        if cur_node.label != -1:
            cur_set.append(cur_node.label)
            if len(cur_node.child) == 0:
                print(cur_set, " : ", cur_node.support)
                return 1
        cnt = 0
        for child in cur_node.child:
            cnt += self.print_FS(cur_node.child[child], copy.deepcopy(cur_set))
        return cnt
        
    def update_trie(self,item,cur_node,freq_items,freq):
        if item in cur_node.child:
            cur_node.child[item].support += freq
        else:
            cur_node.child[item] = Node(item,freq,cur_node)
            
            
            self.link_similar_nodes(cur_node.child[item],freq_items)
            
        return cur_node.child[item]
            
        
        
    def link_similar_nodes(self,newnode,freq_items):
        #print(newnode.label)
        #print(freq_items[newnode.label][0])
        if (freq_items[newnode.label][1] == None):
            #node added for the first time in trie
            freq_items[newnode.label][1] = newnode          
        else:
            node = freq_items[newnode.label][1]          
            while node.next != None:
                node = node.next              
            node.next = newnode
        
            
            
        
        
    def update_dataset(self,dataset,freq_items,trans_freq):
        
        #print(freq_items)
        temp_dataset = []
        temp_freq = []
        for idx,transection in enumerate(dataset):            
            temp_transection = []
            temp_items = copy.deepcopy(freq_items) 
            
            for item in temp_items:
                
                if temp_items[item] >= self.minSup:            
                    if item in transection:
                        temp_transection.append(item)
                else:
                    del freq_items[item]
            
            if len(temp_transection):
                temp_dataset.append(temp_transection)
                temp_freq.append(trans_freq[idx])
                
        dataset = temp_dataset
        return dataset,freq_items,temp_freq
        


class Node():

    def __init__(self,label,support,parent):
        self.label = label
        self.support = support
        self.child = dict()
        self.next = None
        self.parent = parent
        