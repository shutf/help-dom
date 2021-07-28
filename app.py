import streamlit as st
import os
import subprocess
import numpy as np
import tensorflow as tf
import autokeras as ak
from tensorflow.keras.models import load_model

labels = {5: 'Julia', 0: 'C', 1: 'C++', 2: 'Dart', 3: 'Go', 4: 'Java', 6: 'JS', 7: 'Python'}

def app():
	st.title("Anti-Family-Virus")
	loaded_model = load_model("model_autokeras", custom_objects=ak.CUSTOM_OBJECTS)
	st.markdown("Dom has failed us! Run a python script to create and save a file named \"please.txt\" with the contents \"Give my family back!\"")
	datafile = st.file_uploader("Upload File")
	if datafile is not None and st.button("Upload"):
		for file in os.listdir():
			if file not in ['.git', 'app.py', 'LICENSE', 'model_autokeras', 'README.md', 'test.py', 'text_classifier', '.streamlit']:
				os.remove(file)
		try:
			datafile_bytes = datafile.read()
			datafile_bytes_str = datafile_bytes.decode('utf-8')
			with open(datafile.name, mode="w", encoding="utf-8") as f:
				f.write(datafile_bytes_str)
			st.write("Current Files:", os.listdir())
			predicted_y = loaded_model.predict(np.array([datafile_bytes_str]))
			predicted_y = predicted_y[0]
			label = np.argmax(predicted_y)
			predicted_y = [float(i) for i in predicted_y]
			predicted_y = {labels[i]: round(predicted_y[i], 4) for i in range(8)}
			st.write(predicted_y)
			if labels[label]=='Python' or labels[label]=='Julia':
				st.write("Sorry, we don't run Python code here!")
			else:
				proc = subprocess.Popen(["python", datafile.name], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				try:
					outs, errs = proc.communicate(timeout=30)
				except TimeoutExpired:
					proc.kill()
					outs, errs = proc.communicate()
				st.write(outs, errs)
			os.remove(datafile.name)
			st.write("Current Files:", os.listdir())
			if 'please.txt' in os.listdir():
				st.write("You are Successful, the flag is nite\{stop-checking-the-github-repo\}")
		except Exception as e:
			st.write(e)


if __name__ == '__main__':
	app()
