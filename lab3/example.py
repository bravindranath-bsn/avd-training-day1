import requests
from jinja2 import Environment, FileSystemLoader
from pprint import PrettyPrinter

# disable warnings about self-signed certs
import urllib3
urllib3.disable_warnings()

CVP_IP = "192.168.0.5"

# USE YOUR CREDENTIALS
USERNAME = 'arista'
PASSWORD = 'aristaivm8'

if __name__ == '__main__':
    pp = PrettyPrinter()
    env = Environment(loader=FileSystemLoader("/home/coder/project/labfiles/day1/lab3/"))
    template = env.get_template("example.j2")
    kwargs = {}
    with open('/home/coder/project/labfiles/day1/lab3/cvp.token') as infile:
        access_token = infile.read()

    s = requests.session()
    s.verify = False
    s.cookies.set("access_token", access_token)

    # change imageurl to the actual endpoint you find in the REST API explorer
    r = s.get('https://{}/cvpservice/image/getImages.do?startIndex=0&endIndex=0'.format(CVP_IP))
    response = r.json()
    kwargs['eos_images'] = response['data']
    
    # change containerurl to the actual endpoint you find in the REST API explorer
    r = s.get('https://{}/cvpservice/inventory/containers'.format(CVP_IP))
    response = r.json()
    kwargs['containers'] = response

    # pass the data you collected above to your jinja tempalte
    print(template.render(kwargs=kwargs))