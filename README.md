# Seismic Wave Simulation
 Numberical simulation for seismic wave equation, provide simple commands to run.
 This program using Pseudo-spectral method to simulate seismic wave propagate in anisotropic/isotropic medium.

# Install

## Download code
You can download the code by click the download button or use git clone.

```
git clone https://github.com/Sumbrella/Seismic-Wave-Simulation
```

## Install dependency 
We need python 3.7.X or higher versions.
Then change to the project dir:
run command:
```
pip install -r requirements.txt
```
# Usage
## Run program by config file
You can simply run the test simulation by the following command
```
```

you can also change parameter in test.cfg.

The config file constants parameter:
```
[run]
simulate_time =    # time for simulate (s)
simulate_delta_t =   # time segmentation (s)

run_with_show =      # True / False, True => the program will real time display the simulation result.  
show_times =         # int or list, if the value is int, program will show that times of frames; if the value in list, the program will show frames at the show_times;

use_anti_extension # True / False, True => use the anti extension method. False => on the other hand.

[medium]             # Meidum Configs
xmin        = 0                    
xmax        = 1024                 
nx          = 256                  
zmin        = 0                    
zmax        = 1024                 
nz          = 256                  
medium_type = I                    
rho         = 2.7                  
c11         = 24300000             
c12         = 607500               

[source]              #  Source config
source_x      = 512   #  Source position 
source_z      = 100   #  Source position

source_x_type = ricker           
source_x_args = 40                
source_z_type = ricker           
source_z_args = 40              

[save]
save = False          # Save the result or not     
save_format = txt     # Save format, txt or bin.
save_times  = 100     # How many frames to save
x_outfile   = data/testx.sfd   # Save Result Path
z_outfile   = data/testz.sfd   # Save Result Path

[boundary]            # Boundary
# solid boundary
boundary_type   = solid 
x_absorb_length = 0       
z_absorb_length = 0
# absorb_alpha    = 0.010        

# # atten boundary
# boundary_type = atten
# x_absorb_length = 20
# z_absorb_length = 20
# absorb_alpha = 0.009
```


## Simulate in VTI medium


## Simulate in HTI medium

## Use anti extension method

## positional arguments
```
    run                 run simulation
    show                draw sfd format file
    save_gif            save sfd file to gif
    save_png            save sfd file into pngs
    show_point          show one point seismic record.
    show_section        show one section seismic record.
```
