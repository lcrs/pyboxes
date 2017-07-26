![Ls_LUTy](http://lewissaunders.com/rubbish/Ls_LUTy_thumb.jpg)

Demo vid: https://www.youtube.com/watch?v=df2yIh3nx_4

This samples patches from two colour charts, then builds a 3x3 matrix to match one to the other.  It will try to match any two charts, but it works best on two scene-linear images which are already matched in exposure.  For matching stills cameras to Alexa, it's best to use dcraw to convert the still images to linear TIFFs - going near Adobe products with RAW files tends to lead to contrast curves being baked in to the results, which are too complex to reverse with a matrix.

I hope to extend this to create 3D LUTs from charts for more complicated cases, or even from two arbitrary images.

On macOS, hopefully this will work out of the box because I've tried to package up OpenEXR inside the Python file.  On Linux, you may need to install a few dependencies - check the message printed in the Flame log, or try:
`sudo yum install numpy openexr openexr-devel gcc-c+; sudo easy_install -Z openexr`


![Ls_nukeBLG](http://lewissaunders.com/rubbish/Ls_nukeBLG_thumb.jpg)

Demo vid: https://www.youtube.com/watch?v=RWUgEo4UMMw

This starts a background Nuke render process which applies a Baselight BLG grade to the input.  It requires a Nuke render licence and the Baselight for Nuke plugin installed.  You may need to set the path to Nuke at the top of the file.
