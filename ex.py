tracking_object = {2: (951, 558), 3: (887, 632), 4: (1071, 708)}
tracking_object_prev = {2: (951, 548), 3: (887, 642), 4: (1071, 718)}

d = []
for vid,pt in tracking_object.items():
    for vidp,ptp in tracking_object_prev.items():
        if vid==vidp:
            if pt[1]-ptp[1]<0:
                print(f"{vid} and {vidp} is Going")
            else:
                print(f"{vid} and {vidp} is Coming")





            
            
