python -m pip install -r evocraft-requirements.txt
cp Evocraft-py/minecraft_pb2.py .
cp Evocraft-py/minecraft_pb2_grpc.py .
cd Evocraft-py && java -jar spongevanilla-1.12.2-7.3.0.jar
cd .. && python evocraft_setup_scripts/edit_eula_file.py --file_path=Evocraft-py/eula.txt
