import subprocess

def replaceParameterInFile (inputFile, outputFile, substitute): 
    f = open (inputFile)
    s = f.read ()
    f.close ()
    for k,v in substitute.items () :
        s = s.replace (k, v)
    f = open (outputFile, 'w')
    f.write (s)
    f.close ()


wps = ["loose","medium","tight","50p"]


categories = { 't':['fj_nn_top','fj_decorr_nn_top'],
               'w':['fj_nn_w','fj_decorr_nn_w']
               }

massbins={'t':['t1','t2','t3','t4'],
        'w':['w1','w2','w3']
        }

ranges={ 't1':[300,400],
         't2':[400,480],
         't3':[480,600],
         't4':[600,1200],
         'w1':[200,300],
         'w2':[300,400],
         'w3':[400,800],
         }


for part in ['w']:#['t','w']:
    for cat in categories[part]:
        for wp in wps: 
            for bin in massbins[part]:
                for err in ['stat','syst']:                    
                    fitres = "Hists_"+part+"_"+cat+"_"+wp+"_"+bin+"_"+err+".root"
                    print "processing",fitres
                    plotf = "plot_"+part+"_"+cat+"_"+wp+"_"+bin+"_"+err
                    replacemap={
                        '<FNAME>': fitres,
                        '<OUTNAME>': plotf
                        }
                    replaceParameterInFile('sframplot_template.steer','tmp.steer',replacemap)
                    
                    subprocess.call(["SFramePlotter/bin/Plots","-f","tmp.steer"])
                    
                
                
