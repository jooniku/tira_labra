# Requirement Specification

## Problem specification
The idea is to create a tool that can take an image of hand-written numbers which are then recognized and classified appropriately.

## Solution specification
The solution is implemented with a convolutional neural network (CNN) trained on the [MNIST](http://yann.lecun.com/exdb/mnist/) dataset of hand-written digits.

The neural network follows the LeNet-5 architecture and for classification, a softmax regression model is used to return probabilities for each digit 0-9.



## Sources
- The project is based on this paper _J. Li, G. Sun, L. Yi, Q. Cao, F. Liang and Y. Sun, "Handwritten Digit Recognition System Based on Convolutional Neural Network"_, 2020 [IEEE](https://ieeexplore.ieee.org/document/9213619)
- [The Deep Learning textbook](https://www.deeplearningbook.org/) was used as a learning resource 

## Course management
- I am in the bachelor's of computer science programme (TKT)
- Currently I only understand python well enough to give meaningful critique
- The language for the complete project is English