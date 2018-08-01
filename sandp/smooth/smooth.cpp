#include <iostream>
#include "smooth.h"
#include <vector>
#include <string>
#include <sstream>
#include <cmath>

using namespace std;

void smooth(double * dataSmooth,
         int   meanNum,
         int   length,
         int   coverNum)
{
   vector<double> data;
   double tmp,mean=0;
   int count=0;
   
   for (size_t i=0;i!=length;i++)
       data.push_back(dataSmooth[i]);
   
       
   for (size_t i=0;i!=meanNum;i++)
       mean+=data[i];
   mean/=meanNum;
   
   
   for (size_t i=coverNum;i!=length;i++)
   {
       tmp=0;
       count=0;
       
       for (size_t j=i-coverNum; (j!=length)&&(j<=i+coverNum); j++)
       {
           tmp+=data[j];
           count++;
       }
       dataSmooth[i]=abs(mean-tmp/count);
   }
 
   //cout << coverNum << " " <<length<< endl;
   //return 0;
}

