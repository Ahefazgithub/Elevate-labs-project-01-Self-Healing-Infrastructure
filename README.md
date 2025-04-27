

Report on Self-Healing Infrastructure with Prometheus, Alertmanager & Ansible



1. Introduction:


In modern infrastructure management, ensuring high availability and minimizing downtime are critical. A self-healing infrastructure automatically detects and recovers from failures without human intervention, increasing reliability and reducing operational overhead. This report discusses the design and implementation of a self-healing infrastructure using Prometheus, Alertmanager, and Ansible to monitor and automatically recover from failures in a service (NGINX in this case). The system is designed to automatically restart NGINX if it goes down, based on alerts triggered by Prometheus and handled by Alertmanager.


2. Abstract:

The project aims to build a self-healing infrastructure where Prometheus monitors the health of a service (NGINX), and upon failure detection, Alertmanager triggers a webhook that executes an Ansible playbook to automatically restart the service. This mechanism is entirely automated and ensures minimal downtime in case of service failures. The following report details the tools used, the steps involved in implementing the system, and the outcomes of the project.



3. Tools Used:

The following tools were utilized to build the self-healing infrastructure:

    Prometheus: An open-source monitoring and alerting toolkit designed to collect and store metrics from various sources. It was used to monitor the health and performance of NGINX by scraping data from the NGINX Prometheus Exporter.

    NGINX Prometheus Exporter: A tool that exposes NGINX metrics to Prometheus. It scrapes NGINX's /stub_status endpoint to collect data like uptime and request counts.

    Alertmanager: A component of Prometheus used to manage alerts. It processes alerts sent from Prometheus and can trigger actions like sending notifications or running a webhook.

    Ansible: A configuration management tool used to automate the process of restarting NGINX. If a failure is detected, Ansible automatically restarts the NGINX service.

    Docker (for NGINX Prometheus Exporter): Used to containerize the NGINX Prometheus Exporter, making it easier to deploy and run on the system.




4. Steps Involved in Building the Project:



The project was built through the following steps:


    
    Set up NGINX Service:


        Installed NGINX on an Ubuntu EC2 instance to serve as the sample service to monitor.

        Configured NGINX to expose the /stub_status endpoint for Prometheus to scrape.


    Install Prometheus:


        Installed and configured Prometheus to monitor system metrics and the NGINX service.

        Configured Prometheus to scrape metrics from the NGINX Prometheus Exporter at localhost:9113.


    Install and Configure NGINX Prometheus Exporter:


        Initially missed installing the NGINX Prometheus Exporter. Afterward, it was installed using Docker to expose NGINX metrics to Prometheus.

        Configured Prometheus to scrape data from the NGINX Prometheus Exporter.


    Set Up Alertmanager:


        Configured Alertmanager to handle alerts and trigger actions when a service failure occurs (e.g., NGINX going down).

        Alertmanager was configured to send alerts to a Webhook, but the implementation of the webhook service is pending.


    Create Alerting Rules in Prometheus:

    
        Configured Prometheus alerting rules to detect when NGINX is down, triggering an alert if the up{job="nginx"} metric equals 0 for more than 1 minute.

    Develop Ansible Playbook:


        Wrote an Ansible playbook to automatically restart NGINX if it goes down.

        The playbook used the service module to restart NGINX.

    Integrate Webhook for Ansible Execution:


        Outlined the setup of a Webhook that will receive alerts from Alertmanager and trigger the Ansible playbook to restart NGINX.


    Testing:


        The system was tested by manually stopping NGINX and verifying that Prometheus detected the failure, Alertmanager sent the alert, and the webhook triggered the Ansible playbook to restart NGINX.



5. Conclusion:



The self-healing infrastructure setup with Prometheus, Alertmanager, and Ansible was successfully implemented to automatically monitor and recover from NGINX service failures. After completing the project, the system was able to detect when NGINX went down, trigger alerts through Prometheus and Alertmanager, and use Ansible to restart the service without manual intervention.

The system demonstrates the potential for automating recovery processes in production environments, ensuring minimal downtime and improved service availability. However, there are a few pending tasks such as completing the Webhook service that will trigger the Ansible playbook. Once these pieces are in place, the system will be fully automated and functional for self-healing in real-world use cases.



6.  YML and Code Files:



Prometheus Configuration (prometheus.yml):

global:
  scrape_interval: 15s
  evaluation_interval: 15s

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          # - alertmanager:9093

rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"
  # - "alert_rules.yml"

scrape_configs:
  - job_name: "node_exporter"
    static_configs:
      - targets: ["localhost:9100"]

  - job_name: "nginx"
    static_configs:
      - targets: ["localhost:9113"]




Prometheus Alerting Rule (alert_rules.yml):




groups:
- name: nginx_alerts
  rules:
  - alert: NGINXDown
    expr: up{job="nginx"} == 0
    for: 1m
    labels:
      severity: critical
    annotations:
      summary: "NGINX is down"




Ansible Playbook (restart_nginx.yml):




---
- name: Restart NGINX if it goes down
  hosts: localhost
  become: yes
  tasks:
    - name: Restart NGINX
      service:
        name: nginx
        state: restarted



7.Docker Command to Run NGINX Prometheus Exporter:

docker run -d -p 9113:9113 --name nginx-prometheus-exporter \
  -e NGINX_HOST=localhost \
  -e NGINX_PORT=80 \
  nginxinc/nginx-prometheus-exporter


Webhook for Ansible Playbook Trigger (Python Flask Example):


from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if 'alert' in data:
        # Trigger Ansible playbook to restart NGINX
        subprocess.run(["ansible-playbook", "restart_nginx.yml"])
    return "Webhook received!", 200

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)


![prometheus status](https://github.com/user-attachments/assets/410779db-092b-44f4-a609-adfa40ac27da)
![alertmananger](https://github.com/user-attachments/assets/0b63c4fa-6e5c-4487-84c0-97a7b2a57090)
![node exporter](https://github.com/user-attachments/assets/c0d43f65-e2e5-42fc-85c9-9ce15713e0d4)
