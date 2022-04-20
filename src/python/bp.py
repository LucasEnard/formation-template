import grongier.pex

from msg import FormationRequest, FormationIrisRequest
from obj import FormationIris


class Router(grongier.pex.BusinessProcess):

    def OnRequest(self, request):
        if isinstance(request,FormationRequest):
            msg = FormationIrisRequest()
            msg.formation = FormationIris()
            msg.formation.name = request.formation.nom
            msg.formation.room = request.formation.salle
            self.SendRequestSync('Python.FileOperation',request)
            formIrisResp = self.SendRequestSync('Python.IrisOperation',msg)
            if formIrisResp.bool:
                self.SendRequestSync('Python.PostgresOperation',request)

        return 