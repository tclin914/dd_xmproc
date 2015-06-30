### A. Description
Given several inputs with passing and failing runs and the failed program, your task is to isolate the causes with minimum difference between passing and failing inputs . After this homework, you will know how to simplify and isolate the causes with minimum differences. 

### B. Requirement
In homework 1.3, you are asked to use ddmin or delta to simplify the failure inputs of xmlproc. In this homework, as an extension of ddmin, we have a dd function to isolate the minimum cause between the actual world and the alternate world. You will apply dd to the xmlproc inputs and see the isolated inputs.

### C. Steps
1. Produce failures

2. Write a testing function (test(), split(), minus(), union())

3. Revise the dd module (python)

### D. Results

`$ python xmproc/dd.py demo/urls.xml`
