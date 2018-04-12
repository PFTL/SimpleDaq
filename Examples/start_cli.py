from PythonForTheLab.Model.experiment.IV_measurement import Experiment

e = Experiment()
e.load_config('Config/experiment.yml')
e.load_daq()
e.do_scan()
e.save_scan_data('filename.txt')