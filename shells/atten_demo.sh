# simple demo for simulate 2D wave field on homogeneous isotropic medium with atten boundary.

cd $(dirname $(dirname $(realpath "$0"))) || exit

python main.py 
    run \
    --run_with_show \
    --show_times 21 \
    --simulate_time 0.25 \
    --simulate_delta_t 2e-4 \
    \
    --xmin 0 \
    --xmax 1024 \
    --nx 256 \
    --zmin 0 \
    --zmax 1024 \
    --nz 256 \
    --medium_type I \
    --c11 24300000 \
    --c12 6075000 \
    \
    --source_x_type ricker \
    --source_x_args 40 \
    --source_z_type ricker \
    --source_z_args 40 \
    \
    --save \
    --x_outfile data/test_x.sfd \
    --z_outfile data/test_z.sfd \
    \
    --boundary_type atten \
    --x_absorb_length 20 \
    --z_absorb_length 20 \
    --boundary_args 0.015