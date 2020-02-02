import SoftLayer
import datetime

def main(dict):

    API_USERNAME = dict['user']
    API_KEY = dict['apikey']
    VSI = dict['vsi']
    client = SoftLayer.create_client_from_env(username=API_USERNAME, api_key=API_KEY)
    mgr = SoftLayer.VSManager(client)
    imageName = VSI + '_' + datetime.datetime.today().isoformat()

    try:
        virtualGuests = client['SoftLayer_Account'].getVirtualGuests()

    except SoftLayer.SoftLayerAPIError as e:
        print("Unable to retrieve virtual guest. "
              % (e.faultCode, e.faultString))

    vsiFound = False
    res = "ERROR"
    virtualMachines = 'None'
    for virtualGuest in virtualGuests:
        if virtualGuest['hostname'] == VSI:
            vsiFound = True
            try:
                res = mgr.capture(instance_id=virtualGuest['id'], name=imageName, notes=API_USERNAME)
                print ("VSI", VSI, "is found. Now capturing an image template:", imageName)

            except SoftLayer.SoftLayerAPIError as e:
                 vsiFound = e

    return { 'VSI' : VSI, 'ImageName' : imageName, 'Action_Performed' : vsiFound, 'result' : res }
