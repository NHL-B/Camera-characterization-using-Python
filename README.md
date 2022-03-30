# Camera-characterization-using-Python 
> #### *These codes, based on EMVA Standard 1288, are intended to facilitate the characterization of cameras and image sensors.*

## EMVA Standard 1288
![EMVA](https://user-images.githubusercontent.com/92443490/159484319-394a24ef-433c-4ce3-9343-60d90512708f.png)


The different parameters that describe the characteristics and quality of a sensor are gathered and coherently described in the [EMVA 1288](https://www.emva.org/standards-technology/emva-1288/). 

I would highly recommend that you carefully read and understand this document before starting any operation.

This standard illustrates the fundamental parameters that must be given to fully describe the real behavior of a sensor, together with the well-defined measurement methods to get these parameters. 

The standard parameters are:
- Dark current (DC) [ADU/s]
- Quantum efficiency (QE) [%]
- Read noise (RON) [e-]
- Gain (K) [ADU/e-]
- Signal-to-noise ratio (SNR) [dB]
- Dynamic range (DR) [dB]
- Saturation (full-well) capacity [e-] 
- Photo-Response Non-Uniformity (PRNU) [%]
- Dark Signal Non-Uniformity (DSNU) [e-] 

For full documentation, please refer to [Camera characterization Documentation](https://github.com/NHL-B/Camera-characterization-using-Python/tree/main/Camera%20characterization%20Documentation)

For the time being, QE, PRNU and DSNU are not discussed here. 

The results of these tests will give you quantifiable information about the state of your current camera as well as providing a method to compare 
cameras, which may be valuable if you’re in the process of making a decision for a new purchase.

![Results](C:\Users\belgherz\Desktop\Characterization.png)

[Requirements](requirements.txt): A list of Python libraries you'll need for this project.

## License & copyright
© NHL-B
Licensed under the [MIT License](LICENSE).