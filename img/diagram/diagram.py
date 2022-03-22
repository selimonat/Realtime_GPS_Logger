from diagrams import Cluster, Diagram
from diagrams.generic.database import SQL
from diagrams.aws.database import RDSMysqlInstance
from diagrams.generic.device import Mobile
from diagrams.programming.language import Python
from diagrams.custom import Custom
from diagrams.onprem.monitoring import Grafana

with Diagram("Event processing",show=False):
    phone = Mobile("Phone running Owntracks")
    with Cluster("Services"):
        connector = Python("Connector")
        mysql = RDSMysqlInstance("MYSQL DB")
        mqtt = Custom("MQTT broker", "./mosquitto.png")
        grafana = Grafana("Grafana")
    phone >> mqtt >> connector >> mysql << grafana
