# TOCO command lne for TFLite conversion
```
toco \
    --input_file="tf_files/garage_graph.pb" \
    --input_format=TENSORFLOW_GRAPHDEF \
    --output_file=tf_files/optimized_graph.lite \
    --output_format=TFLITE \
    --input_shape=1,224,224,3 \
    --input_array=input \
    --output_array=final_result \
    --inference_type=FLOAT \
    --input_data_type=FLOAT
```
## Command Line options
	--input_file=""                  	string	Input file (model of any supported format). For Protobuf formats, both text and binary are supported regardless of file extension.
	--output_file=""                 	string	Output file. For Protobuf formats, the binary format will be used.
	--input_format=""                	string	Input file format. One of: TENSORFLOW_GRAPHDEF, TFLITE.
	--output_format=""               	string	Output file format. One of TENSORFLOW_GRAPHDEF, TFLITE, GRAPHVIZ_DOT.
	--default_ranges_min=0.000000    	float	If defined, will be used as the default value for the min bound of min/max ranges used for quantization.
	--default_ranges_max=0.000000    	float	If defined, will be used as the default value for the max bound of min/max ranges used for quantization.
	--inference_type=""              	string	Target data type of arrays in the output file (for input_arrays, this may be overridden by inference_input_type). One of FLOAT, QUANTIZED_UINT8.
	--inference_input_type=""        	string	Target data type of input arrays. If not specified, inference_type is used. One of FLOAT, QUANTIZED_UINT8.
	--input_type=""                  	string	Deprecated ambiguous flag that set both --input_data_types and --inference_input_type.
	--input_types=""                 	string	Deprecated ambiguous flag that set both --input_data_types and --inference_input_type. Was meant to be a comma-separated list, but this was deprecated before multiple-input-types was ever properly supported.
	--drop_fake_quant=false          	bool	Ignore and discard FakeQuant nodes. For instance, to generate plain float code without fake-quantization from a quantized graph.
	--reorder_across_fake_quant=false	bool	Normally, FakeQuant nodes must be strict boundaries for graph transformations, in order to ensure that quantized inference has the exact same arithmetic behavior as quantized training --- which is the whole point of quantized training and of FakeQuant nodes in the first place. However, that entails subtle requirements on where exactly FakeQuant nodes must be placed in the graph. Some quantized graphs have FakeQuant nodes at unexpected locations, that prevent graph transformations that are necessary in order to generate inference code for these graphs. Such graphs should be fixed, but as a temporary work-around, setting this reorder_across_fake_quant flag allows TOCO to perform necessary graph transformaitons on them, at the cost of no longer faithfully matching inference and training arithmetic.
	--allow_custom_ops=false         	bool	If true, allow TOCO to create TF Lite Custom operators for all the unsupported TensorFlow ops.
	--drop_control_dependency=false  	bool	If true, ignore control dependency requirements in input TensorFlow GraphDef. Otherwise an error will be raised upon control dependency inputs.
	--debug_disable_recurrent_cell_fusion=false	bool	If true, disable fusion of known identifiable cell subgraphs into cells. This includes, for example, specific forms of LSTM cell.
usage: /Users/Golf/miniconda3/envs/tflite37/bin/toco
Flags:
	--input_array=""                 	string	Deprecated: use --input_arrays instead. Name of the input array. If not specified, will try to read that information from the input file.
	--input_arrays=""                	string	Names of the output arrays, comma-separated. If not specified, will try to read that information from the input file.
	--output_array=""                	string	Deprecated: use --output_arrays instead. Name of the output array, when specifying a unique output array. If not specified, will try to read that information from the input file.
	--output_arrays=""               	string	Names of the output arrays, comma-separated. If not specified, will try to read that information from the input file.
	--input_shape=""                 	string	Deprecated: use --input_shapes instead. Input array shape. For many models the shape takes the form batch size, input array height, input array width, input array depth.
	--input_shapes=""                	string	Shapes corresponding to --input_arrays, colon-separated. For many models each shape takes the form batch size, input array height, input array width, input array depth.
	--input_data_type=""             	string	Deprecated: use --input_data_types instead. Input array type, if not already provided in the graph. Typically needs to be specified when passing arbitrary arrays to --input_array.
	--input_data_types=""            	string	Input arrays types, comma-separated, if not already provided in the graph. Typically needs to be specified when passing arbitrary arrays to --input_arrays.
	--mean_value=0.000000            	float	Deprecated: use --mean_values instead. mean_value parameter for image models, used to compute input activations from input pixel data.
	--mean_values=""                 	string	mean_values parameter for image models, comma-separated list of doubles, used to compute input activations from input pixel data. Each entry in the list should match an entry in --input_arrays.
	--std_value=1.000000             	float	Deprecated: use --std_values instead. std_value parameter for image models, used to compute input activations from input pixel data.
	--std_values=""                  	string	std_value parameter for image models, comma-separated list of doubles, used to compute input activations from input pixel data. Each entry in the list should match an entry in --input_arrays.
	--variable_batch=false           	bool	If true, the model accepts an arbitrary batch size. Mutually exclusive with the 'batch' field: at most one of these two fields can be set.
	--rnn_states=""                  	string	
	--model_checks=""                	string	A list of model checks to be applied to verify the form of the model.  Applied after the graph transformations after import.
	--graphviz_first_array=""        	string	If set, defines the start of the sub-graph to be dumped to GraphViz.
	--graphviz_last_array=""         	string	If set, defines the end of the sub-graph to be dumped to GraphViz.
	--dump_graphviz=""               	string	Dump graphviz during LogDump call. If string is non-empty then it defines path to dump, otherwise will skip dumping.
	--dump_graphviz_video=false      	bool	If true, will dump graphviz at each graph transformation, which may be used to generate a video.
	--allow_nonexistent_arrays=false 	bool	If true, will allow passing inexistent arrays in --input_arrays and --output_arrays. This makes little sense, is only useful to more easily get graph visualizations.
	--allow_nonascii_arrays=false    	bool	If true, will allow passing non-ascii-printable characters in --input_arrays and --output_arrays. By default (if false), only ascii printable characters are allowed, i.e. character codes ranging from 32 to 127. This is disallowed by default so as to catch common copy-and-paste issues where invisible unicode characters are unwittingly added to these strings.
	--arrays_extra_info_file=""      	string	Path to an optional file containing a serialized ArraysExtraInfo proto allowing to pass extra information about arrays not specified in the input model file, such as extra MinMax information.