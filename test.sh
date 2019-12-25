 #!/bin/bash
for filename in ~/test_*.jpg; do
  echo $filename
  python -m scripts.label_image     \
    --graph=tf_files/garage_graph.pb      \
    --image $filename \
    --labels garage_labels.txt 2> /dev/null 

done