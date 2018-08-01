#include <iostream>
#include "findPoWa.h"
#include <vector>
#include <string>
#include <sstream>

using namespace std;


const char* findPotentialWave(double * data,int length,int leftWidth,int rightWidth,double judge){
   string S1,spl,spr;
   int wide=0;
   int left_edge=0,right_edge=0;
   stringstream ssl,ssr;
   //cout << "length" <<length << endl;
   for (int i=0;i!=length;i++){
       if (data[i] > judge){
           wide++;
           if (wide == 1)
               left_edge=i;
       }
       else{
           right_edge=i;
           //cout << right_edge << endl;
           if ((wide > leftWidth) && (wide < rightWidth)) {
               ssl << left_edge;
               ssr << right_edge;
              // cout << left_edge << " " << right_edge << endl;
               S1+= ssl.str() + "," + ssr.str() + ";"; 
               ssl.str("");
               ssr.str("");
           };
           wide=0;
       };   
   }
   return S1.c_str();
 
}
