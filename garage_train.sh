python -m scripts.retrain  \
   --bottleneck_dir=tf_files/bottlenecks \
   --how_many_training_steps=500  \
   --model_dir=tf_files/models/  \
   --summaries_dir=tf_files/training_summaries/"${ARCHITECTURE}"   \
   --output_graph=tf_files/garage_graph.pb   \
   --output_labels=garage_labels.txt   \
   --architecture="${ARCHITECTURE}"   \
   --image_dir=tf_files/garage_data
