

### Content
This is are some simple unit tests to check that the different software run smoothly on sciserver. The individual conda environment tests are run in python as unit tests. 


### Running:
The tests should be run from inside the sciserver container, where the data is mounted to ~/workspace/headata/FTP/*
```sh
chmod +x run_tests.sh
./run_tests.sh
```
