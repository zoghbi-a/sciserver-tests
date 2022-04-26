#!/bin/bash -i


# a function to check if pytest is installed.
# if not, install it.
check_pytest () {
    if python -c "import pytest" > /dev/null 2>&1; then
        echo "using pytest ..."
    else
        pip install pytest
    fi
}


echo
echo "**************************"
echo "Running scierver tests ..."
echo "**************************"
echo


echo
echo "Testing conda (heasoft)"
echo "-----------------------"
echo
conda activate heasoft
check_pytest
if python -m pytest test_heasoft.py; then
    echo "Tests for (heasoft) passed successfully"
else
    echo "Tests for (heasoft) failed"
fi


echo
echo "Testing conda (ciao)"
echo "-----------------------"
echo
conda activate ciao
check_pytest
if python -m pytest test_ciao.py; then
    echo "Tests for (ciao) passed successfully"
else
    echo "Tests for (ciao) failed"
fi
conda deactivate

echo
echo "Testing conda (fermi)"
echo "-----------------------"
echo
conda activate fermi
check_pytest
if python -m pytest test_fermi.py; then
    echo "Tests for (fermi) passed successfully"
else
    echo "Tests for (fermi) failed"
fi
conda deactivate


echo
echo "Testing conda (xmmsas)"
echo "-----------------------"
echo
conda activate xmmsas
check_pytest
if python -m pytest test_xmmsas.py; then
    echo "Tests for (xmmsas) passed successfully"
else
    echo "Tests for (xmmsas) failed"
fi
conda deactivate