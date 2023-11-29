# batch-image-enhacement
Pipeline code to stitch together several image enhancement steps and process a folder of images. Offers heuristics and statistics for before/after enhancement. Currently only using openCV modules, but other modules are planned to be added.

# Run process

$ runscript.py --pipeline current_pipeline.json --input_directory ~/datafolder --output_directory ~/outputfolder


# Currently implemented processes:

## CLAHE - contrast limited adaptive histogram equalization
Uses window to locally adjust Lightness histogram in LAB color space to adaptively improve contrast
function name: clahe()
parameters: 
- tile_size: default is 20, sets comparison window size for localized histogram equalization
- clip_limit: default is 2.0, sets clipping limit for CLAHE

## RGB equalization
Stretches histograms for R,G,B channels separately to attempt to fix color
function name: rgb_eq()
parameters:
- none currently, should change to allow batch norm

## Gamma correction
Scales brightness to make minimum brightness above a certain level
function name: gamma_corr()
parameters:
- minimum_brightness: default is 0.3, sets minimum gamma
- planned to add additional inputs to allow batch norm

## Unsharp Mask
Applies an unsharp mask to image to enhance edges
function name: unsharp_mask()
parameters:
- kernel_size: default is 5, size of gaussian blur filter used, assuming square filter of equal dimension
- sigma: default is 2.0, sigma of gaussian blur filter used
- amount: default is 2.0, amount of "sharpness" to apply
- threshold: default is 0, if positive non-zero, sets threshold for mask to use original image instead of 



## Median filter
Applies a median filter to image to reduce shot noise
parameters:
- kernel_size: default is 7

## Gaussian blur
Applies a Gaussian blur to the image
parameters:
- kernel_size: default is 9, assumes square filter
- sigma: default is 0, sigma of Gaussian

## Bilateral filter
Applies a bilateral filter to the image
parameters:
- diameter: default is 9
- sigma_color: default is 100
- sigma_space: default is 100





# Notes:
- 'params' field in pipeline json needs to have an empty dict ('{}') if you don't want to pass any arguments


# Things to add:
- batch normalization
- add statistics computation
- add median, bilinear, and gaussian filters
<<<<<<< HEAD
- tests for inputs
=======
- tests for input and modules
>>>>>>> a3ec5ae (Added smoothing filters)
