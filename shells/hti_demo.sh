# simple demo for simulate 2D wave field on homogeneous HTI medium.

cd $(dirname $(dirname $(realpath "$0"))) || exit

python main.py run\
    --xmin 0 \
    --xmax 1024 \
    --nx 256 \
    --zmin 0 \
    --zmax 1024 \
    --nz 256 \
    --medium_type VTI \
    --rho 2.8 \
    --c_matrix 15.6e6 6.11e6 26.4e6 4.38e6\
    --source_x_args 40 \
    --source_z_args 40 \
    --simulate_time 0.2 \
    --simulate_delta_t 2e-4 \
    --save_times 10 \
    --run_with_show \
    --source_x_type ricker \
    --source_z_type none \
    --save \
    --x_outfile data/test_x.sfd \
    --z_outfile data/test_z.sfd
