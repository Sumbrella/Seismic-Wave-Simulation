# simple demo for simulate 2D wave field on homogeneous isotropic meidum.

python main.py run\
    --xmin 0 \
    --xmax 1024 \
    --nx 256 \
    --zmin 0 \
    --zmax 1024 \
    --nz 256 \
    --medium_type I \
    --c_matrix 24300000 6075000\
    --source_x_args 40 \
    --source_z_args 40 \
    --simulate_time 0.2 \
    --simulate_delta_t 2e-4 \
    --save_times 10 \
    --run_with_show \
    --save \
    --source_z_type \
