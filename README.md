# Easy-Label-Ordinality-Regression (ELO-Regression)
A simple GUI python script for labeling relative ordinality between images

## Why labeling expert/subjective regression problem is hard?
1) Only a domain expert is able to give direct score. (e.g. Which one has better muscle? Can you score them?)
2) Subjective label depends on a single person. (e.g. Which one do I prefer?)
3) One cannot give a globally consistent score between [0,100] for large-scale images.

## Why ordinality can help?
1) Average people can tell which one is better even without the absolute score.
2) Very few choices. (Left is better. Right is better. I cannot tell. Bad pair.)

## How do I run this thing?
```
# Download your images set into one single folder (e.g. './download').
# Run command
python ELO.py


# 1. Selected the image folder you want to label.
# 2. Labeling!!!
# 3. Save the label into npz file.
```
## Labeling command

+ Left (&#x2190;): Left is better. Save as number 0
+ Down (&#x2193;): I cannot tell which one is better. Save as number 1
+ Right (&#x2192;): Right is better. Save as number 2
+ Up (&#x2191;): Bad Pair. Save as number -1

## System command
+ q: Quit the program.
+ b: Back to previous pair.
+ s: Save the current results.

## Dependencies
+ python
+ tkinter
+ numpy
+ PIL
+ glob

## To do
+ Resume the label results

## Contact
If you find this respository useful, or you want to do some cooperation. 
Feel free to contact me: shamangary@hotmail.com

