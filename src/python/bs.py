from grongier.pex import BusinessService

from dataclass_csv import DataclassReader

from obj import Formation,Patient
from msg import FormationRequest,PatientRequest

import requests
class ServiceCSV(BusinessService):

    def getAdapterType():
        """
        Name of the registred adaptor
        """
        return "Ens.InboundAdapter"
    
    def OnInit(self):
        if not hasattr(self,'Path'):
            self.Path = '/irisdev/app/misc/'
        return

    def OnProcessInput(self,request):
        filename='formation.csv'
        with open(self.Path+filename) as formation_csv:
            reader = DataclassReader(formation_csv, Formation,delimiter=";")
            for row in reader:
                msg = FormationRequest()
                msg.formation = row
                self.SendRequestSync('Python.Router',msg)

        return

class FlaskService(BusinessService):

    def OnInit(self):
        
        if not hasattr(self,'Target'):
            self.Target = "Python.Router"
        
        return

    def OnProcessInput(self,request):

        return self.SendRequestSync(self.Target,request)

if __name__ == "__main__":

    svc = ServiceCSV()
    svc.OnInit()
    svc.OnProcessInput('')

class PatientService(BusinessService):

        def getAdapterType():
            """
            Name of the registred adaptor
            """
            return "Ens.InboundAdapter"

        def OnInit(self):
            if not hasattr(self,'Target'):
                self.Target = "Python.PatientProcess"

            if not hasattr(self,'ApiUrl'):
                self.ApiUrl = "https://lucasenard.github.io/Data/patients.json"
        
            return

        def OnProcessInput(self,request):
            r = requests.get(self.ApiUrl)
            if r.status_code == 200:

                dat = r.json()

                for key,val in dat.items():

                    patient = Patient()
                    patient.name = key
                    patient.infos = val

                    msg = PatientRequest()
                    msg.patient = patient

                    self.SendRequestSync(self.Target,msg)
            return 

