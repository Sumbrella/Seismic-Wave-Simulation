cd $(dirname $(dirname $(realpath "$0"))) || exit

python main.py save_gif \
  --input_file data/test_x.sfd \
  --file_format '.txt' \

