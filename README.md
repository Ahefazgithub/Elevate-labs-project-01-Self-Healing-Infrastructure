Self-Healing Infrastructure with Prometheus, Alertmanager & Ansible


Introduction

In today's cloud-native environments, maintaining high availability and ensuring service resilience is crucial. Automation plays a key role in achieving these goals. This project demonstrates how to create a self-healing infrastructure using Prometheus for monitoring, Alertmanager for alerting, and Ansible for automating remediation actions. The project uses an EC2 instance running Ubuntu as the base environment, with NGINX as a sample service.


The aim of this project is to automatically detect service failures (like NGINX going down) and recover them by executing an Ansible playbook that restarts the service. This process is fully automated and managed by Prometheus, Alertmanager, and Ansible.



Abstract

This project integrates monitoring and automation tools to create a self-healing infrastructure. By monitoring the NGINX service with Prometheus, we can automatically restart the service if it fails, reducing downtime and minimizing manual intervention. The key components of this project include:


    Prometheus: Monitors the NGINX service and collects metrics.

    Alertmanager: Sends alerts when the service fails.

    Ansible: Executes an automation playbook to restart the service.

    Webhook: Used to trigger the Ansible playbook from Alertmanager.



The solution uses an EC2 instance running Ubuntu, along with Docker to host the NGINX exporter for Prometheus.



Tools Used

    Prometheus: Open-source monitoring and alerting toolkit.

    Alertmanager: Handles alerts sent by Prometheus and manages the notification and remediation process.

    Ansible: Automation tool for managing configuration and running tasks such as restarting services.

    NGINX: Web server used as a sample service for monitoring.

    NGINX Prometheus Exporter: Exports metrics from the NGINX server to be scraped by Prometheus.

    Docker: Used to run the NGINX Prometheus Exporter container.

    EC2 Instance (Ubuntu): Cloud-based virtual machine used for deploying the solution.

    Webhook: A method used to trigger the Ansible playbook from Alertmanager.



Steps Involved in Building the Project



1. Setting Up Prometheus


    Install Prometheus on the EC2 instance to monitor the NGINX service.

    Configure Prometheus by editing the prometheus.yml file to scrape NGINX metrics from a local endpoint.

    Example configuration:

    scrape_configs:
      - job_name: "nginx_exporter"
        static_configs:
          - targets: ["localhost:9113"]


2. Setting Up Alertmanager


    Install Alertmanager on the EC2 instance.

    Configure Alertmanager to send notifications when an alert is triggered. For simplicity, it is set to send alerts via webhook.

    Example configuration in alertmanager.yml:

    route:
      receiver: 'webhook'
    receivers:
      - name: 'webhook'
        webhook_configs:
          - url: 'http://localhost:5000/webhook'


3. Setting Up NGINX Exporter


    Install NGINX Prometheus Exporter using Docker to export NGINX metrics.

    The exporter collects statistics about NGINX and exposes them to Prometheus.

    Example Docker command to run the exporter:

    docker run -d -p 9113:9113 --name nginx-prometheus-exporter nginx/nginx-prometheus-exporter


4. Configuring Ansible for Automation


    Install Ansible on the EC2 instance to execute the automation playbook.

    Write an Ansible playbook that restarts the NGINX service in case of failure. For example, restart_nginx.yml:

    ---
    - name: Restart NGINX if it fails
      hosts: localhost
      tasks:
        - name: Restart NGINX
          service:
            name: nginx
            state: restarted



5. Setting Up Webhook



    Create a Python webhook service to listen for alerts from Alertmanager.

    The webhook will trigger the Ansible playbook to restart the NGINX service when an alert is received.

    Example webhook script:

    from flask import Flask, request
    import subprocess

    app = Flask(__name__)

    @app.route('/webhook', methods=['POST'])
    def webhook():
        data = request.json
        if data['status'] == 'firing':
            subprocess.run(['ansible-playbook', 'restart_nginx.yml'])
        return 'OK', 200

    if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0', port=5000)



6. Testing the Self-Healing Process



    Stop NGINX manually to simulate a failure.

    Verify that Prometheus detects the failure, triggers an alert via Alertmanager, which then calls the webhook, and the webhook runs the Ansible playbook to restart NGINX automatically.




7. Docker Setup for NGINX Prometheus Exporter



    The NGINX Prometheus exporter was installed and configured using Docker to run as a container, enabling the monitoring of NGINX without direct installation on the host machine.





Conclusion




This project successfully demonstrates how to build a self-healing infrastructure using Prometheus, Alertmanager, and Ansible. By monitoring the NGINX service with Prometheus and utilizing Alertmanager to trigger an Ansible playbook via a webhook, we have automated the recovery of NGINX if it fails, ensuring minimal downtime and intervention.

This self-healing mechanism can be adapted to other services as well, offering a robust and scalable solution for infrastructure management. The integration of monitoring, alerting, and automation enhances the resilience of cloud-native applications.
Configuration Files and Scripts
prometheus.yml

global:
  scrape_interval: 15s
  evaluation_interval: 15s

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093

rule_files:
  - "alert_rules.yml"

scrape_configs:
  - job_name: "nginx_exporter"
    static_configs:
      - targets: ["localhost:9113"]

alertmanager.yml

route:
  receiver: 'webhook'
receivers:
  - name: 'webhook'
    webhook_configs:
      - url: 'http://localhost:5000/webhook'

restart_nginx.yml

---
- name: Restart NGINX if it fails
  hosts: localhost
  tasks:
    - name: Restart NGINX
      service:
        name: nginx
        state: restarted

Webhook Python Script (webhook.py)

from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if data['status'] == 'firing':
        subprocess.run(['ansible-playbook', 'restart_nginx.yml'])
    return 'OK', 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


![prometheus status](https://github.com/user-attachments/assets/410779db-092b-44f4-a609-adfa40ac27da)
![alertmananger](https://github.com/user-attachments/assets/0b63c4fa-6e5c-4487-84c0-97a7b2a57090)
![node exporter](https://github.com/user-attachments/assets/c0d43f65-e2e5-42fc-85c9-9ce15713e0d4)
