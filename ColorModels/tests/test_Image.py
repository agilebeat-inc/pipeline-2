import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import unittest
from  Image import Image
import tempfile
import io
import base64

class TestImage(unittest.TestCase):
    tile_construction = "iVBORw0KGgoAAAANSUhEUgAAAQAAAAEACAMAAABrrFhUAAAA1VBMVEVVVVVbW1thYWFnZ2dsbGxzc3N9fX2BgYGNjY2RkZGdnZ2jo6Otra2wsLC9vbnBwbnHx7TDw73GyLXExL7DybvJybbFxcK9zMS0ztDMzLqw0NbJycaq097Qz7/Ly8nQ0L/My8nNzcrS0cHOzs3T08TU08PU08TQz87R0c7W1cbS0tHU09HY18nV1NLW1tXb2c3Y19Ta2dXe3NDa2tnc2tff3dnh3tfd3d3i4dbh4eHl4tzn5ODo5t3l5eXp5uHq6N/p6ent6uTu7u7y7+nx8fH29vb///89D3A3AAAQZUlEQVR4nNWdC7ecthHHceo8mqTVhe3Sbjd37b2bhA2bJbnBLsEJDl7Dfv+PVNADBIi3RpLn9JymscuiH9LMaP5osL4r7L//fpBl6JTea4tdtOJaUXkJX9qtic0qx/8vSRdz7DCvR58FyFl1ubC8ykXSvfVZAeA/626zMrSPuYefHNY8fGwYQCDj1gbM+k7S9EeXWz36PNysHv7DQ1BeKlx/nUGzpIwfuRE399OThNEXdlECQMI1Go4vX+f4eDuX14skXazPVgNoOb7rSsfH2wkHEmmXE9tKAM4+4R3fXtbDx3bA15QHVGjrANic389DW/K97rFDMRgAOtWTX5bj4801HED9+PNImuPjbVNe+wZxZc4WA0Aee/y3i0THx5ttMgCbOb/8CHaHCMcVIwHUjz8GvD8MIDcRgM0Sn+wA6aJQbiYA5LPHH8HeHAZwNw2A41aPfw8coYwEgK4s9oXAd1b8VmYeAO7xw9wPbwhvsG3YH5kFAAXqHv8DA+DC/sgMAI7LSh43F3j10x/E0w14qk0HgEL2+AMVj78wJzEIAP/4QW+I/0282TjC/shEAOof/wMDcIL9kUkAnH3Gdr1qVj81FcLAFAAoYo//qu7xl4an3RX2N8YBcI9/A3svHcNRF1gYGAVQPf7cV/v4H9QIAyMAnEOu6/EX5uMdF+xvDANArOqVe8off2EerjjA/sYQgPrxJ8AJeY8d9QJw2MYvB6j4TjIiDMD+xgCAEx0/ZNVr2FQIA/0A9pof/4MaYaAXgJ1rfvwPaoSBPgCkGgNd9RsxFXXxHgCIVH5SrePXCICmf9CixJipEAaEAGgAzDUkfw1TIQwIARxJAFBQ9xw2FXVxAQCHBsCTyq2/0DQBsGnpR/v4lQgDXQCkGK3dAda3AuuJOgAQ0731pgDkXnAwhi3CtgHU1U814segqRAGWgAc/16bfi+gQBhoATjQh0/+66qbgAJhoAnAJTsgj2nAF80EFAgDDQB0BxQ6Dw6VQT29BBQIAzwAosSQHbBDVwGwLjNiCoQBHgDJAOn+G5lAQIEwwAEgCyBn9U8mCBxAf3/YFAgDHICw9cRZTVzjnkiBMFADwAW4e8JlP5RAro+AAmGgAkDSzmYJgKbFubI3AtpGhAHQSFQBIClgy+PSypg2AgpODDAApAjcqcBqJqBAGKAA6GTvjpNujjURIMIA6KaMAjiyFLBjNiWgpT6o4IV5AoDUnsQ1EEog06GPKqiLYwBONJTy2Jk2AqoA7Os9gMgoAeizGwJTIAyUAIijy/uf8CbXRECBMFACIFtfb+Bv0TqBcqVMQV3cYjnw8OA0EVBQF7dYrjMS6CmBRC0BJQDwhmN8073XQUCBMGD15MBdo4KZ0jcmFAgDVjx5z08rxioFEwXCgEUGNWW/4agnQE4MgNakrDmpBn1vTJ1kpODEgDXnFxziMO/Pyorl8ViGstqsWZ6dKWfKJCN4YcAazIG7diEEVElG8J10rJmAmWTkqyEALwxYc9NbJhmBLszK4DvpWLPTDCYZHVXMAXhhwJqPl0lGwOfZsMF30rEWxHQmGSkQzeBPDCxqoKBONMMbENATAwtbaKiSjOCFgYVNVFQRgBcGlnaRUSQZwZ8YWN5HiBKAFUzg6+LLO0kx0QxULoCvi69opYUUSEZGA1AhGcELA6va6THJCI4AvDCwrp8guGQEXxdf2VFyAyyYEACQXmZtT1FgyQheGFjdVBVWMnLAhYH1bXVBJSN4YUBCX2FQyQhcGJDRWPkASABcGJABAFI0i6Drj1IAOHCSEbgwIAVAJRnJP2UELgzIAcDetJVPAPyFeVkAoCQjcGFAGoBKMpJ1QWLgwoA0AEDnrMCFAXkAYE4ZvcYAAMvCEgGAnDIiwsAnAgBCMgIXBqQCAJCMXOi6uFwAlWAijQD4iQHJAKRLRuDCgGwAsiUj8Lq4dACSJaNPEEAlGUkhAC4MAACQesoIXBiAAMD6EMggAC4MgACQeMoIvMU+DADWjXA9AXBhAAiANMkIXBiAAiBLMgIXBsAAyCIALQzAAZAkmkF30gEEwESzdYIJrjGcZd1S1yABSBHNoL+9CwpAhmQELQzAApAgGUELA7AAaB8YcWuGaQYtDEADWC2aQQsD0AAeHCoZLT1nBS0MgAOouvQvPGUE3WIfHsBKyQhaGFAAYJ1kNPWFeQctsOL/pAJARWDJBzonvDCPkH0M4jQXWdawW9PSwpQAWCOaDQkDxQN0T2Fy4z5+PtvUAFghGQmFgXK+7y9Rmg0NzSgAy1vzterixdA3xXxf9dC1AFgsGVV18XK+e2GS9Q+drHpTASyVjEhdfGS+Z2nk76e4fRvZ9qb4T2kuNnUAFkpGaPCR5rc4PLloxcfPFQJYIhkhL+0behpfD/aaoRNTCaA6ZTSRAHJj0ePPkhDPdzn3pBTAnFNGjn29tUZezPfguFn/0BumFsDkU0bokDSGnkaXcr4D3JFiANUpoyECaBPyHj/1JT/0hqkGwIrl/dl90+/loavnU1twNiiYIDfi/V5yBG9ZpB5APwEHNfxeFtgKOjZpANAjGaFDzI0+j/dq+lXpACCQjJym37v5gG6vaVoAtCUjdGr4vWiV3yu2i6cgCK7Xi+97nnc6HY+Hw76wMvMvtgCt3YEeALxk1PJ76XK/V+4X/Sidvh8sN4+aALDvuYXo0vJ7y6Z+MfZDEC+pj+gCUH3SlbNlfq+Y8l4447GbAoBJRsyW+L2yLra2OKQNQOOjVrP9noPsQ5D0TPliuxiEhUWFxdiSJEmx4WJwWR9mVWONAOoPO6ezvuw7OOWL/eK+u3NwqIlqRBoBkEJp/jw93xua8sWG0WuVhra7p1/e/f7bL7/8/PNPP37//dPTq8fHxx22bWn4L+kEUCR/0cSHX0z5Yzgw5Y+dvfLu1c9/fRyzP3//TSuAKYaLwX3BPb/FF8GU3z3+9G508NTMBoD2QdyuC3FTXlQd2j7++PvUwZsOAHniOZ8lwWtheWi7++G3OYM3GwC6dqd9z5QvrfR4cwdvMgAUtIafp+Fp01cVLDzeksEbC8CxQ374WRwc+suCczzepwHA2XCVkcR3B4rBcz3epwAAudzw403//mCJxzMfANrXekAe9dbOl3o80wGgQ10ZysO+0sAKj2c2AHSqc548EC/8lR7PZADIr7OezBcNX4LHMxcAH/Zvgg2SJI9nKIBG2E8P7eFL9HhGAnBsriqcdMqCO5kez0AAjawn7hTGdj/BDl83gJGsZ/sj9PD1AkD7wbC/ffoTfvwaAaAjN/xu2N++Aoh5BgFAHpf1XLtx7xEo6hkCAF24rMfrDn8HGPcMANDIegRaqMLhawAwkvUUix888mkFsIm4YodADFUR+fQBaIZ9gRyoJvJpA+ByLz9GolrPo5rIpwmAU78RkIeiEqeyyKcHAAq4rEcwfKWuXwMAdmjonl1ExQ7oPZ92ALS3kjDrUR75NACgr0aKGwlsv9c3fDUAnCMdv2j2b58kVznNA8DcXy46Nqkj8ikGwNxfJjgupifyqQVg012/4PV4XZGvYdAAXLrv7XaS0Rf5GgbcROVA3V+n4qMz8jUMFABrn9HpHLD9YfwNLkUGCYAdmm+fltUd+RoGCIAele2cENMe+RoG2E1O7P52+iNfw6AAOPRYTKuJlBGRr2FAAKqX4RutYwyJfA2DAcC6pjQaRigv900ymLa6tPZ144+JPxkT+RoGAWBDN/+Ng4GmJD5tAwDgCtzf1jjnx0w+AFb75HuHbQ2LfZxJ/74A2/zvufGbFvt5k/2FCdHmf2dU6tcyuQBY7bOx+d8pV3vmmFQAwtrno+4hDptMAKz22Xjf4Un3CEdMHgBEjwHmRz77NTL7400aAKH7M6bu02+yALDNf8pv/s1Nf2qTBEC4+Tc4/alNDgBh7dPk9Kc2GQCqc+Cnxubf5PSnNgkAxLVPs9Of2tYDENc+DU9/alsNwBbWPk1Pf2pbC4C2CGzVPo1Pf2pbCUDYNntrYO2z11YCcLu1z08i/anNWvW9cLoAGu7/k0h/arPu2X5x2y6HVL+v/L8rw/+Hd+91j2uyWaUDX/otM1dQ/SjG78VZ6nvXtx90D26KWXgNC19eGzX6VT2++P/418eP72j/4Ft89fy3ps8Fi27i3AXrgCwA/htAOP2hreJoehQH/vnNH7qH2W8Wu9Oew7oDtu8sAJL+tHpk3XEHBP98eat5qGKzTuz4wlxnSBYA3yaapD8fog4AsiSyyD8/vzPNMVjVXmbmJ7FoBPCrf8HSn2cM5iZuAJOnoe/9ahKFMhHaswNc+YymXu0FUKU/zAXckjgR9wAq2yQbEyRwJli/yp5ObXzeXgB1+uPzY8UUhF2gTKFAUmFnUx3mmOYMHbJuPPa/d/+rrrjvjLWkIJwKZZDQHSrZXgBVzvA2xRmSUVb6N1/9edvjBMvPIIg7ghWh8qwtVNabIbu68fGv49EFwDLIx8a7D+/3h2tPB7BbHMU9FLIkcE/PfyhfEtxu0JnsDB2iAbDXH191L/v+re/19UErKETdznjBN59/hj8dcFYbJBrbYd4ZDq0D0hSXLYDe6s8YBa4LbP6FZVmf0xxaaahs1QM21YnuAWdIvqrMFsBI9QdT6PlOxi0OQwoo/7tlvfzbZ19+Q8/WKQsS7YII8mpn2DN+xC+ASdWfDzhpuvXNhZJCfv/nC/eeed9+9fLbel7coqt3gQ0S3YpQdb6rzxmSBUDSxmnVH7I/PA+uiDBodlDj/ywoKEDNBUFJzNmztSl0hnQBkPFPq/68wRf0yn8c9gtB0Ncv9lauCAi/IKwJ1s4w6WSGdIIcy3+eKv6cMbJr9b9HKFx7KJTeUXqMEBdFHZe5rU53B/ISWFwGid3Ut97xBvnW2g6PULj09E3Oy0j5LC9r6qsK886Qj4ioXgCPk1/9xOcmYpEvG4mUl56G6VnhFs5ynGN/WVzoDOm/LA/A7Sb/BqkQBL1/Pkzh6l3FFPAfrXaOA7oA5wyrPhf1AphR/SZBwB/+SyMUfPGKKNKFlUnToDDCOUOS9XARYIb6R0ok5wl/c8wviL0jdo5L3cKIMrRpOEP6Fvi8BdANAiM2QCG9FpFS3Ga62Eydl7iFMWmMc4YuIuXOqHSKc+QfYRAYsfe/8t+cuX/78qt/+PndfuHeGxl0m8L8nGlcG+ScIWaRzVwAHz/i9+eEQWDA3uIRHthcSNxvvnjx8qVlfV2tiIKC2DkWOdN0tzBBHHUOjd/Zz1wAo0FAbKSydiYrgtYXkgKA9SW3AG5pEiV9bsF7npKnTFKH2QmYagHM0n8nBYGONdcNpfDi869PnfH2Vlny0i28GZl5E+XxKjPEC0BQARmw53onMMOC7rp5/+x6vbWmJO53C/6AW5j6fgDyuQUw7/QPCQK/zhv/e+x5BJGDWxEiCuL8uUgkzj050+QXJAgArAPMfAFiSRDgN5ACIxR69o1pIvxAbVliKSi0V8RUAJs6Asx9AWxREJiQO5xJZbaXgtAtdOrwEwHQd+HKV0G2M18AXBYEzuPThszJQ/+KyNJULMqUJZbXlz/mACDn4MMyAsx9A+odiWD+qD9uGPaB0VBO8wZfNy6HMZRBlxSEf5CnWI34PxGR/cTFG0wSAAAAAElFTkSuQmCC"
    tile_runway = "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"

    def setUpFileSystemTest(self):
        pass

    #@unittest.skip("use it if you need it")
    def test_load_from_b64string(self):
        img = Image.load_from_b64string(self.tile_construction)
        self.assertEqual(65536, len(img.RGBs))
    
    #@unittest.skip("use it if you need it")
    def test_load_from_filesystem(self):
        with tempfile.NamedTemporaryFile(suffix='.png') as nt_file:
            img = base64.urlsafe_b64decode(self.tile_construction)
            nt_file.write(img)
            img = Image.load_from_filesystem(nt_file.name)
            self.assertEqual(65536, len(img.RGBs))

    def test_save_from_filesystem(self):
        with tempfile.NamedTemporaryFile(suffix='.png') as nt_file:
            img_from_b64 = Image.load_from_b64string(self.tile_construction)
            img_from_b64.save(nt_file.name)
            img = Image.load_from_filesystem(nt_file.name)
            self.assertEqual(65536, len(img.RGBs))


if __name__ == '__main__' and __package__ is None:
    unittest.main()