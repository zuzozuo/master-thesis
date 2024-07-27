
Monitoring and Managing RabbitMQ on CentOS

### RabbitMQ Management Plugin
The RabbitMQ management plugin provides a web-based UI to manage and monitor RabbitMQ. Here's how you can enable and use it:

1. **Enable the Management Plugin**:
   ```bash
   sudo rabbitmq-plugins enable rabbitmq_management
   ```

2. **Access the Management Console**:
   Open your web browser and go to `http://<hostname>:15672/`. The default login credentials are `guest` for both username and password.

### RabbitMQ Command-Line Tools
RabbitMQ provides a set of command-line tools that you can use to manage and monitor RabbitMQ from the terminal. Here are some commonly used commands:

#### Viewing Queues
To list all queues:
```bash
sudo rabbitmqctl list_queues
```

To list queues with more details, such as the number of messages, consumers, and other attributes:
```bash
sudo rabbitmqctl list_queues name messages consumers
```

#### Viewing Exchanges
To list all exchanges:
```bash
sudo rabbitmqctl list_exchanges
```

#### Viewing Bindings
To list all bindings:
```bash
sudo rabbitmqctl list_bindings
```

#### Viewing Nodes
To get the status of the RabbitMQ nodes:
```bash
sudo rabbitmqctl status
```

#### Viewing Connections
To list all connections:
```bash
sudo rabbitmqctl list_connections
```

#### Viewing Channels
To list all channels:
```bash
sudo rabbitmqctl list_channels
```

### Monitoring Tools
For more advanced monitoring, you can integrate RabbitMQ with monitoring tools like Prometheus and Grafana. RabbitMQ has plugins for exporting metrics to Prometheus, which can then be visualized using Grafana dashboards.

#### Enabling Prometheus Plugin
1. **Enable the Prometheus Plugin**:
   ```bash
   sudo rabbitmq-plugins enable rabbitmq_prometheus
   ```

2. **Access Metrics**:
   Metrics will be available at `http://<hostname>:15692/metrics`.

### Log Files
RabbitMQ logs can also provide insights into its behavior. The log files are usually located in `/var/log/rabbitmq/`. You can use standard Linux commands to view and analyze these logs.

#### Viewing Logs
To view the latest log entries:
```bash
tail -f /var/log/rabbitmq/rabbit@<hostname>.log
```

Replace `<hostname>` with your actual hostname.

### Detailed Monitoring via Command Line

1. **Listing Queues with Detailed Info**:
   ```bash
   sudo rabbitmqctl list_queues name messages_ready messages_unacknowledged messages consumers state
   ```

2. **Listing Exchanges**:
   ```bash
   sudo rabbitmqctl list_exchanges name type durable auto_delete internal
   ```

3. **Listing Bindings**:
   ```bash
   sudo rabbitmqctl list_bindings source_name destination_name destination_type routing_key
   ```

4. **Checking Node Health**:
   ```bash
   sudo rabbitmqctl node_health_check
   ```

5. **Getting Node Status**:
   ```bash
   sudo rabbitmqctl status
   ```

6. **Listing Connections**:
   ```bash
   sudo rabbitmqctl list_connections name peer_host peer_port state
   ```

7. **Listing Channels**:
   ```bash
   sudo rabbitmqctl list_channels connection peer_host peer_port state
   ```

8. **Displaying Environment Information**:
   ```bash
   sudo rabbitmqctl environment
   ```

9. **Viewing Memory Usage**:
   ```bash
   sudo rabbitmqctl list_queues name memory
   ```

10. **Viewing Detailed Node Information**:
    ```bash
    sudo rabbitmqctl report
    ```
    This command provides a detailed report of the RabbitMQ node, including configuration, connections, channels, queues, and exchanges.

### Example Commands for Specific Tasks

- **Viewing Messages in Queues**:
  ```bash
  sudo rabbitmqctl list_queues name messages_ready messages_unacknowledged
  ```

- **Viewing Queue Consumers**:
  ```bash
  sudo rabbitmqctl list_consumers
  ```

- **Checking Aliveness**:
  ```bash
  sudo rabbitmqctl aliveness_test vhost_name
  ```

- **Checking Cluster Status**:
  ```bash
  sudo rabbitmqctl cluster_status
  ```

- **Listing Queue Arguments**:
  ```bash
  sudo rabbitmqctl list_queues name arguments
  ```

### Automating Monitoring with Scripts

You can also create scripts to automate and periodically check the RabbitMQ status. Here's a simple bash script example:

```bash
#!/bin/bash

# Script to monitor RabbitMQ status

# Check node status
echo "Node Status:"
sudo rabbitmqctl status

# List queues
echo "Queues:"
sudo rabbitmqctl list_queues name messages_ready messages_unacknowledged messages consumers state

# List connections
echo "Connections:"
sudo rabbitmqctl list_connections name peer_host peer_port state

# List channels
echo "Channels:"
sudo rabbitmqctl list_channels connection peer_host peer_port state
```

Save this script, make it executable, and run it to get a snapshot of your RabbitMQ status:

```bash
chmod +x monitor_rabbitmq.sh
./monitor_rabbitmq.sh
```

Using these commands and scripts, you can effectively monitor and manage RabbitMQ from the command line without needing to rely on the web GUI.
