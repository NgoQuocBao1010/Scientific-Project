from django.apps import AppConfig
from datetime import datetime

class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        from .models import RaspDevice
        from .customPrint import MyCustomPrint
        
        # Handle untrack devices if server was down previously
        onlineRasp = RaspDevice.objects.filter(status="online")
        if onlineRasp.exists():
            for rasp in onlineRasp:
                rasp.status = "offline"
                rasp.save()
                
                drives = rasp.drive_set.all().filter(status="ongoing")

                for drive in drives:
                    drive.status = "ended"
                    drive.endTime = datetime.now()
                    drive.save()
            
            MyCustomPrint("Server is down earlier, fixed", style="error")

        import accounts.signals
