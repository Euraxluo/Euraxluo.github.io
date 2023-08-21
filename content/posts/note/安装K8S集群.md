---
title: "安装K8S集群"
date: "2023-08-01"
description: "安装K8S集群"
featured : false
categories: ["notes"]
tags: [ "notes" ]
series: [ "notes" ]
images: []
---

- [1. 安装环境](#1-安装环境)
- [2. 修改节点的hosts](#2-修改节点的hosts)
- [3. 安装依赖，并且下载kk](#3-安装依赖并且下载kk)
- [4.创建配置](#4创建配置)
- [5.进行安装](#5进行安装)


## 1. 安装环境
![安装环境截图](/image/k8s_install.png)

## 2. 修改节点的hosts
最后得到节点：
192.168.110.21 paas-node1
192.168.110.22 paas-node2
192.168.110.23 paas-node3


|主机 IP	|主机名	|角色|
| :-----| ----: | :----: |
|192.168.110.21	|paas-node1  |control plane, etcd|
|192.168.110.22	|paas-node2	|worker|
|192.168.110.23	|paas-node2	|worker|


配置ssh三个节点互相免密
在每一个节点运行以下命令：
- ssh-keygen 三次回车，生成rsa 公钥和私钥
- ssh-copy-id user@ip 将公钥分发给所有的机器
- 可以上别的机器，查看 cat ~/.ssh/authorized_keys
- 可以本机直接ssh ip，登录别的机器


## 3. 安装依赖，并且下载kk
sudo apt install socat conntrack ebtables ipset curl openssl tar -y

然后我们在node1 上安装kk

curl -sfL https://get-kk.kubesphere.io | VERSION=v3.0.7 sh -

## 4.创建配置
./kk create config --with-kubesphere v3.3.2 --with-kubernetes v1.22.12

集群配置如下
```yaml
apiVersion: kubekey.kubesphere.io/v1alpha2
kind: Cluster
metadata:
  name: sample
spec:
  hosts:
  - {name: paas-node1, address: 192.168.110.21, internalAddress: 192.168.110.21, privateKeyPath: "~/.ssh/id_rsa"}
  - {name: paas-node2, address: 192.168.110.22, internalAddress: 192.168.110.22, privateKeyPath: "~/.ssh/id_rsa"}
  - {name: paas-node3, address: 192.168.110.23, internalAddress: 192.168.110.23, privateKeyPath: "~/.ssh/id_rsa"}
  roleGroups:
    etcd:
    - paas-node[1:3]
    control-plane: 
    - paas-node[1:3]
    worker:
    - paas-node[1:3]
  controlPlaneEndpoint:
    ## Internal loadbalancer for apiservers 
    internalLoadbalancer: haproxy

    domain: lb.kubesphere.local
    address: ""
    port: 6443
  kubernetes:
    version: v1.22.12
    clusterName: cluster.local
    autoRenewCerts: true
    containerManager: docker
  etcd:
    type: kubekey
  network:
    plugin: calico
    kubePodsCIDR: 10.233.64.0/18
    kubeServiceCIDR: 10.233.0.0/18
    ## multus support. https://github.com/k8snetworkplumbingwg/multus-cni
    multusCNI:
      enabled: false
  registry:
    privateRegistry: ""
    namespaceOverride: ""
    registryMirrors: []
    insecureRegistries: []
  addons: []



---
apiVersion: installer.kubesphere.io/v1alpha1
kind: ClusterConfiguration
metadata:
  name: ks-installer
  namespace: kubesphere-system
  labels:
    version: v3.3.2
spec:
  persistence:
    storageClass: ""
  authentication:
    jwtSecret: ""
  zone: ""
  local_registry: ""
  namespace_override: ""
  # dev_tag: ""
  etcd:
    monitoring: true
    endpointIps: localhost
    port: 2379
    tlsEnable: true
  common:
    core:
      console:
        enableMultiLogin: true
        port: 30880
        type: NodePort
    # apiserver:
    #  resources: {}
    # controllerManager:
    #  resources: {}
    redis:
      enabled: true
      volumeSize: 2Gi
    openldap:
      enabled: true
      volumeSize: 2Gi
    minio:
      volumeSize: 20Gi
    monitoring:
      # type: external
      endpoint: http://prometheus-operated.kubesphere-monitoring-system.svc:9090
      GPUMonitoring:
        enabled: false
    gpu:
      kinds:
      - resourceName: "nvidia.com/gpu"
        resourceType: "GPU"
        default: true
    es:
      # master:
      #   volumeSize: 4Gi
      #   replicas: 1
      #   resources: {}
      # data:
      #   volumeSize: 20Gi
      #   replicas: 1
      #   resources: {}
      logMaxAge: 7
      elkPrefix: logstash
      basicAuth:
        enabled: false
        username: ""
        password: ""
      externalElasticsearchHost: ""
      externalElasticsearchPort: ""
  alerting:
    enabled: true
    # thanosruler:
    #   replicas: 1
    #   resources: {}
  auditing:
    enabled: true
    # operator:
    #   resources: {}
    # webhook:
    #   resources: {}
  devops:
    enabled: true
    # resources: {}
    jenkinsMemoryLim: 8Gi
    jenkinsMemoryReq: 4Gi
    jenkinsVolumeSize: 8Gi
  events:
    enabled: true
    # operator:
    #   resources: {}
    # exporter:
    #   resources: {}
    # ruler:
    #   enabled: true
    #   replicas: 2
    #   resources: {}
  logging:
    enabled: true
    logsidecar:
      enabled: true
      replicas: 2
      # resources: {}
  metrics_server:
    enabled: true
  monitoring:
    storageClass: ""
    node_exporter:
      port: 9100
      # resources: {}
    # kube_rbac_proxy:
    #   resources: {}
    # kube_state_metrics:
    #   resources: {}
    # prometheus:
    #   replicas: 1
    #   volumeSize: 20Gi
    #   resources: {}
    #   operator:
    #     resources: {}
    # alertmanager:
    #   replicas: 1
    #   resources: {}
    # notification_manager:
    #   resources: {}
    #   operator:
    #     resources: {}
    #   proxy:
    #     resources: {}
    gpu:
      nvidia_dcgm_exporter:
        enabled: false
        # resources: {}
  multicluster:
    clusterRole: none
  network:
    networkpolicy:
      enabled: false
    ippool:
      type: none
    topology:
      type: weave-scope
  openpitrix:
    store:
      enabled: true
  servicemesh:
    enabled: true
    istio:
      components:
        ingressGateways:
        - name: istio-ingressgateway
          enabled: false
        cni:
          enabled: false
  edgeruntime:
    enabled: false
    kubeedge:
      enabled: false
      cloudCore:
        cloudHub:
          advertiseAddress:
            - ""
        service:
          cloudhubNodePort: "30000"
          cloudhubQuicNodePort: "30001"
          cloudhubHttpsNodePort: "30002"
          cloudstreamNodePort: "30003"
          tunnelNodePort: "30004"
        # resources: {}
        # hostNetWork: false
      iptables-manager:
        enabled: true
        mode: "external"
        # resources: {}
      # edgeService:
      #   resources: {}
  terminal:
    timeout: 600
```

## 5.进行安装
./kk create cluster -f config-sample.yaml