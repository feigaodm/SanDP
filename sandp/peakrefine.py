import operator

## 1) 
## Split potential S2 Peaks: 
## ------------------------>
def split_S2(data_smooth,
             S2_potential,
             max_threshold,
             boundary_threshold=float(1)/5):
    
    def make_boundary(stmp):
        stmp_split=[]
        for i in range(len(stmp)-1):
            stmp_split.append([stmp[i],stmp[i+1]])
        return stmp_split

    S=[]
    for S2_po in S2_potential:
        MAX_point=S2_po[0]
        MIN_point=S2_po[0]
        stmp=[]
        if max(data_smooth[S2_po[0]:S2_po[1]]) > max_threshold :
            for i in range(S2_po[0],S2_po[1]):  
                if data_smooth[i] * boundary_threshold > data_smooth[MIN_point]:
                    if (MIN_point > MAX_point) and (data_smooth[MAX_point] * boundary_threshold > data_smooth[MIN_point]):
                         stmp.append(MIN_point)
                    MIN_point=i
                    MAX_point=i
                elif data_smooth[i] < data_smooth[MIN_point] :
                    MIN_point=i
        stmp.append(S2_po[1])
        stmp.insert(0,S2_po[0])
        S+=make_boundary(stmp)
    return S
## -------------------------------------------------------------------------------------------------------------- 

## 2) 
## peak width calculation: 
## ---------------------->
def peak_width(data_smooth,
               percentage,
               boundary):
    
    maxIndex=boundary[0]
    for i in range(boundary[0]+1,boundary[1]):
        if data_smooth[i] > data_smooth[maxIndex] :
            maxIndex=i
            
    value=percentage*data_smooth[maxIndex]
    width=[]
    ## before maxIndex
    for i in range(boundary[0], maxIndex):
        if data_smooth[i] > value:
            width.append(i)
            break
    if not width:
        width.append(boundary[0])
    
    ## at maxIndex
    width.append(maxIndex)
    
    ## after maxIndex
    for i in range(maxIndex,boundary[1]):
        if data_smooth[i] < value:
            width.append(i)
            break
            
    if len(width) < 3:
        width.append(boundary[1])
        
    return width
    
## 3)    
## Extract more accurate S1 peaks from S2 peaks (peaks width): 
## ---------------------------------------------------------->
def accurate_peaks(data_smooth,
                   S1_potential,
                   S2_split,
                   S1_width):
    S1=S1_potential
    S2=[]
    for boundary in S2_split:
        if boundary[1] - boundary[0] < S1_width:
            S1.append(boundary)
        else:
            S2.append(boundary)
    return S1,S2

## 4)
## Neglect S1s after the biggest S2: 
## -------------------------------->
def accurate_S1(data_smooth,
                S1,
                S2,
                S1_width,
                nearestS1=100,
                distanceS1=10):

    # Merge nearby S1s for single electron S2s idetification
    pool=[]
    S1_out=[]
    S2_out= []
    maxRiseTime=0
    for boundary in S1:
        halfPeak = peak_width(data_smooth,0.5,boundary)
        if halfPeak[1]-halfPeak[0] > maxRiseTime:
            maxRiseTime=halfPeak[1]-halfPeak[0]
        if pool:
            if (
                (boundary[1]-pool[-1][0] > nearestS1)   or
                (boundary[0]-pool[-1][1] > distanceS1)  #or
                #(not(5. > max(data_smooth[boundary[0]:boundary[1]])/float(max(data_smooth[pool[-1][0]:pool[-1][-1]])) > 1/5. ))
               ):
                if(
                   (pool[-1][1]-pool[0][0] < S1_width)
                   # or ((maxRiseTime <= 25) and (max(data_smooth[pool[-1][0]:pool[-1][-1]])>0.05))
                  ):
                    S1_out.append([pool[0][0],pool[-1][-1]])
                else :
                    S2_out.append([pool[0][0],pool[-1][-1]])
                pool=[]
        pool.append(boundary)
    if pool:
        # tell if the merged signal is S1 or S2 by width
        if (pool[-1][1]-pool[0][0]) < S1_width:
            S1_out.append([pool[0][0],pool[-1][-1]])
        else :
            S2_out.append([pool[0][0],pool[-1][-1]])

    # remove S1s after Main S2
    if len(S2) > 0:
        maxIndex=0
        for boundary in S2:
            for i in range(boundary[0]+1,boundary[1]):
                if data_smooth[i] > data_smooth[maxIndex]:
                    maxIndex=i
        S1_out_final=[]
        for boundary in S1_out:
            if boundary[1] < maxIndex:
                S1_out_final.append(boundary)
    else:
        S1_out_final = S1
        S2_out = []
    
    return S1_out_final, S2_out

## 5)
## Merged S2 together: 
## -------------------------------->

def accurate_S2(S2):
    pool = []
    S2_final = []
    S2 = sorted(S2, key=operator.itemgetter(0))

    for boundary in S2:
        if pool:
            if (boundary[0]-pool[-1][1] >=0):
                S2_final.append([pool[0][0],pool[-1][-1]])
                pool=[]
        pool.append(boundary)
    
    if pool:
        S2_final.append([pool[0][0],pool[-1][-1]])

    return S2_final
   
