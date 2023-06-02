
cd $(dirname $(dirname $(realpath "$0"))) || exit

python main.py show \
  --input_file data/test_x.sfd \
  --file_format '.txt' \
  --seg 0.2

