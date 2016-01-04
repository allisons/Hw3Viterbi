#!/usr/bin/env python -O
# Copyright (c) 2016 Allison Sliter
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the 'Software'), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# viterbi.py: simple Viterbi decoding, with protections against underflow
# Steven Bedrick <bedricks@ohsu.edu> and Kyle Gorman <gormanky@ohsu.edu>


from bitweight import BitWeight
from numpy import array, int8, ones, zeros
from collections import defaultdict



class LatticeNode(object):

    
    def __init__ (self, cur_state, cur_obs, cur_time, pointer):
        self.cur_state = cur_state
        self.cur_obs = cur_obs
        self.cur_time = cur_time
        self.pointer = pointer
        self.viterbi = BitWeight(0.)
        
        
    def set_viterbi(self):
        VB = defaultdict(BitWeight)
        TO = defaultdict(BitWeight)
        NN = defaultdict(BitWeight)
        PPSS = defaultdict(BitWeight)
        VB = {"name" : "VB", "start" : BitWeight(.019), "VB" : BitWeight(.0038), "TO" : BitWeight(.83), "NN" : BitWeight(.0040), "PPSS" : BitWeight(.23)}
        TO = {"name" : "TO", "start" : BitWeight(0.0043), "VB" : BitWeight(0.035), "TO" : BitWeight(0.), "NN" : BitWeight(0.016), "PPSS" : BitWeight(0.00079)}
        NN = {"name" : "NN", "start" : BitWeight(0.041), "VB" : BitWeight(0.047), "TO" : BitWeight(0.00047), "NN" : BitWeight(0.087), "PPSS" : BitWeight(0.0012)}
        PPSS = {"name" : "PPSS", "start" : BitWeight(0.067), "VB" : BitWeight(0.007), "TO" : BitWeight(0.), "NN" : BitWeight(0.0045), "PPSS" :      BitWeight(0.00014)} 
        transitions = [VB, TO, NN, PPSS]
        
        I =  defaultdict(BitWeight)
        want =  defaultdict(BitWeight)
        to =  defaultdict(BitWeight)
        race =  defaultdict(BitWeight)
        
        I = {"name" : "I", "VB" : BitWeight(0.), "TO" : BitWeight(0.), "NN" : BitWeight(0.), "PPSS" : BitWeight(.37)}
        want = {"name" : "want", "VB" : BitWeight(0.0093), "TO" : BitWeight(0.), "NN" : BitWeight(0.000054), "PPSS" : BitWeight(0.)}
        to = {"name" : "to", "VB" : BitWeight(0.), "TO" : BitWeight(0.99), "NN" : BitWeight(0.), "PPSS" : BitWeight(0.)}
        race = {"name" : "race", "VB" : BitWeight(0.00012), "TO" : BitWeight(0.), "NN" : BitWeight(0.00057), "PPSS" : BitWeight(0.)}

        emissions = [I, want, to, race]
        
        for s in transitions:
            if s["name"] == self.cur_state:
                tprob = s[self.pointer.cur_state]
                break
     
        for e in emissions:
            if e["name"] == self.cur_obs:
                eprob = e[self.cur_state]
                break
            
        
        self.viterbi = (eprob * tprob)          
        

obs = ('I', "want", 'to', 'race')
states = ['VB', 'TO', 'NN', 'PPSS']
cur_time = 0
initial = LatticeNode('start', "#", cur_time, None)
lattice = list()
previous = initial
best = initial
for s in states:
    n = LatticeNode(s, obs[cur_time], cur_time, previous)
    lattice.append(n)
    n.set_viterbi()
    if best.viterbi < n.viterbi:
        best = n
    previous = best
cur_time += 1
while cur_time < len(obs):
    best.viterbi = BitWeight(0.)
    for s in states:
        n = LatticeNode(s, obs[cur_time], cur_time, previous)
        lattice.append(n)
        n.set_viterbi()
        if best.viterbi < n.viterbi:
            best = n
        previous = best
    cur_time += 1
    
p = lattice[-1]
tagseq = list()
while p.cur_state != "start":
    tagseq.append(p.pointer)
    p = p.pointer

tagseq.reverse()

for tag in tagseq:
    print str(tag.cur_obs) + " : " + str(tag.cur_state) + " " + str(tag.viterbi)
        
        
    
