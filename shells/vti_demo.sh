# simple demo for simulate 2D wave field on homogeneous VTI medium.

cd $(dirname $(dirname $(realpath "$0"))) || exit

python main.py \
    run \
    --run_with_show\
    --simulate_time 0.2 \
    --simulate_delta_t 2e-4 \
    --show_times 10 \
    --use_anti_extension \
    \
    --xmin 0 \
    --xmax 1024 \
    --nx 256 \
    --zmin 0 \
    --zmax 1024 \
    --nz 256 \
    --medium_type VTI \
    --rho 2.17 \
    --c11 26.4e6 \
    --c12 6.11e6 \
    --c33 15.6e6 \
    --c44 4.36e6 \
    \
    --source_x_type none \
    --source_z_type ricker \
    --source_z_args 40 \
    \
    --save \
    --x_outfile data/test_x.sfd \
    --z_outfile data/test_z.sfd \
