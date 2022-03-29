import ROOT

path = "/eos/uscms/store/user/bgreenbe/"
rootname = "data_DoubleMuonB_2017.root"
f0 = path + "4mu_2017/all/" + rootname
f1 = "data_DoubleMuonB_skimmed_test2017.root"
tf0 = ROOT.TFile(f0)

#only bother finding this many event nums in the first file.
maxn = 1000
#this is one of the runs, has 500+ for one root file but <200 for the other.
run = 297099

ttree0 = tf0.Get("Events")

print("opened %s"%f0)
#keep track of all event numbers at this run number
all_events = [] 
for i,e in enumerate(ttree0):
    if len(all_events) >= maxn: break
    if e.run != run: continue
    all_events.append(e.evt)
    print("event number %d added. all_events size: %d"%(e.evt, len(all_events)))
tf0.Close()

totn = len(all_events)
#now remove from all_events any event nums that are also here.
tf1 = ROOT.TFile(f1)
ttree1 = tf1.Get("Events")
print("opened %s"%f1)
n1 = ttree1.GetEntries()
for i,e in enumerate(ttree1):
    if e.run != run: continue
    if i % 10000 == 0:
        print("Processing event %d out of %d."%(i, n1))
    if e.event in all_events:
        all_events.remove(e.event)
tf1.Close()

print("%d events out of %d not in %s. Here they are:"%(len(all_events), totn, f1))
print(all_events) #[:10])
