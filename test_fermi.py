
import unittest
import os
import subprocess as subp
import sys
import glob


class FermiError(Exception):
    pass



class TestFermi(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """setting up"""
        
        cls.file = 'L1506091032539665347F73_PH00.fits'
        cls.url  = ('https://fermi.gsfc.nasa.gov/ssc/data/analysis/scitools/data/'
                    f'dataPreparation/{cls.file}')
        cls.fermi_outdir  = f'tmp.fermi'
        
        if os.path.exists(cls.fermi_outdir):
            os.system(f'rm -rf {cls.fermi_outdir}')
        os.system(f'mkdir -p {cls.fermi_outdir}')
        
    @classmethod
    def tearDownClass(cls):
        os.system(f'rm -rf {cls.fermi_outdir}')
        if os.path.exists('gtselect.par'):
            os.system('rm gtselect.par')
    
    def test_conda_env(self):
        """Test we are in heasoft conda env"""
        self.assertIn('CONDA_PREFIX', os.environ)
        
        env = os.environ['CONDA_PREFIX'].split('/')[-1]
        self.assertEqual(env, 'fermi')
    
    def test_env(self):
        """Test envirenment vairables are set"""
        self.assertIn('CALDB', os.environ)
        self.assertIn('FERMI_DIR', os.environ)
       
    def test_fermipy(self):
        """Test fermipy can be imported"""
        import fermipy
    
    
    def test_fermi_pipeline(self):
        """test a call to chandra data reduction"""
                
        file   = self.file
        url    = self.url
        outdir = self.fermi_outdir
        os.chdir(outdir)
        if not os.path.exists(file):
            os.system(f'wget {url}')
        os.chdir('..')
        
        cmd = (f'gtselect evclass=128 evtype=3 infile={outdir}/{file} '
               f'outfile={outdir}/cena_filtered.fits ra=201.47 dec=-42.97 rad=10 '
                'tmin=239557420 tmax=265507200 emin=300 emax=300000 zmax=90')
                
        proc = subp.Popen(cmd.split(), stdout=subp.PIPE, stderr=subp.PIPE)
        out, err = proc.communicate()
        
        if proc.returncode != 0:
            raise FermiError('gtselect in test_fermi_pipeline failed!\n' + 
                               out.decode()+err.decode())


if __name__ == '__main__':
    
    unittest.main()