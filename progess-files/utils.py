def dateRev(inp):
    print("input date:",inp)
    year,month,day=inp.split("-")
    newDate = day+"/"+month+"/"+year[2:]
    print("newDate:",newDate)
    
if (__name__=="__main__"):
    inp = input("input:")
    dateRev(inp)