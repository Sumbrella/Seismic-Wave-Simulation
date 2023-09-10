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
python main.py run --conf configs/test.cfg
```

you can also change parameter in test.cfg.

The config file constants parameter:
```
[run]
simulate_time       = 0.2
simulate_delta_t    = 5e-4

run_with_show       = True          
show_times          = 20           

use_anti_extension = False         

[medium]
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

[source]
source_x      = 512                
source_z      = 100               

source_x_type = ricker           
source_x_args = 40               
source_z_type = ricker           
source_z_args = 40              

[save]
save = False                   
save_format = .txt             
save_times  = 100
x_outfile   = data/testx.sfd  
z_outfile   = data/testz.sfd 

[boundary]
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
