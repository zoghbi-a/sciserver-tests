
import unittest
import os
import subprocess as subp
import sys
import glob


class SASError(Exception):
    pass



class TestSAS(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """setting up"""
        
        cls.xmm_basedir = '/home/idies/workspace/headata/FTP/xmm/data/rev0' 
        cls.xmm_obsid   = '0861680501'
        cls.xmm_outdir  = f'tmp.{cls.xmm_obsid}'
        
        if os.path.exists(cls.xmm_outdir):
            os.system(f'rm -rf {cls.xmm_outdir}')
        os.system(f'mkdir -p {cls.xmm_outdir}')
        
    @classmethod
    def tearDownClass(cls):
        os.system(f'rm -rf {cls.xmm_outdir}')
    
    def test_conda_env(self):
        """Test we are in heasoft conda env"""
        self.assertIn('CONDA_PREFIX', os.environ)
        
        env = os.environ['CONDA_PREFIX'].split('/')[-1]
        self.assertEqual(env, 'xmmsas')
    
    def test_env(self):
        """Test envirenment vairables are set"""
        self.assertIn('SAS_PATH', os.environ)
        self.assertIn('SAS_CCFPATH', os.environ)
        
        
    def test_xmmsas_pipeline(self):
        """test a call to xmmsas data reduction"""
                
        basedir = self.xmm_basedir 
        obsid   = self.xmm_obsid
        outdir  = self.xmm_outdir
        obsdir  = f'{basedir}/{obsid}'
        
        # prepare data
        os.system(f'cp -rL {obsdir} {outdir}')
        os.chdir(f'{outdir}/{obsid}/ODF')
        os.system('gzip -d *gz')

        
        os.environ['SAS_ODF'] = f'{os.getcwd()}'
        cmd = 'cifbuild'
        proc = subp.Popen(cmd.split(), stdout=subp.PIPE, 
                          stderr=subp.PIPE, env=os.environ)
        out, err = proc.communicate()
        if proc.returncode != 0:
            raise SASError('cifbuild in test_xmmsas_pipeline failed!\n' + 
                               out.decode()+err.decode())
        os.environ['SAS_CCF'] = f'{os.getcwd()}/ccf.cif'
           
        cmd = 'odfingest'
        proc = subp.Popen(cmd.split(), stdout=subp.PIPE, 
                          stderr=subp.PIPE, env=os.environ)
        out, err = proc.communicate()
        if proc.returncode != 0:
            raise SASError('odfingest in test_xmmsas_pipeline failed!\n' + 
                               out.decode()+err.decode())
        
            
        
        cmd = 'epchain'
        proc = subp.Popen(cmd.split(), stdout=subp.PIPE, 
                          stderr=subp.PIPE, env=os.environ)
        out, err = proc.communicate()
        if proc.returncode != 0 or len(glob.glob('*EVL*')) == 0:
            raise SASError('epchain in test_xmmsas_pipeline failed!\n' + 
                               out.decode()+err.decode())
        os.chdir('../../..')
        
        


if __name__ == '__main__':
    
    unittest.main()