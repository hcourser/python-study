Kubernetes 1.21在CentOs 7.9下的安装笔记

[TOC]



# 基础环境准备

以下是所有主机都必须要做的

## 必备包部分

yum install -y yum-utils tar net-tools vim wget

## 网络部分
### 打开ROOT的SSH访问权限

vim /etc/ssh/sshd_config

### 配置静态IP

Vim /etc/sysconfig/network-scripts/ifcfg-eth0

### 关闭防火墙

systemctl stop firewalld

systemctl disable firewalld

### 配置hosts主机名互访

### 加载桥接模式防火墙

*#目的：转发 IPv4 并让 iptables 看到桥接流量*

cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF

sudo modprobe overlay
sudo modprobe br_netfilter

*#通过运行 lsmod | grep br_netfilter 来验证 br_netfilter 模块是否已加载。*

lsmod | grep br_netfilter
lsmod | grep overlay

### 为桥接配置内核参数

*# 为了让 Linux 节点的 iptables 能够正确查看桥接流量*

*# 设置所需的 sysctl 参数，参数在重新启动后保持不变*

cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward         = 1
EOF

*# 应用 sysctl 参数而不重新启动*

sudo sysctl --system

## Linux配置部分
### 关闭交换文件

swapoff -a

vim /etc/fstab

​	#注释调swap那一行 

### 关闭Selinux
setenforce 0
vim /etc/selinux/config
	SELINUX=disabled

## 源配置与安装部分
### Docker
#### 配置Docker仓库

*#使用国内源*
yum-config-manager --add-repo https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo

*#查看源所包含的Docker版本
yum list docker-ce --showduplicates | sort -r
对于本次要安装的K8s 1.21.1，经查所匹配的Docker版本为20.10.2-3.el7 
查找链接为：https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.21.md
其他也这么查*

#### 安装Docker
*#通过上述查询得出的版本号，确认Docker安装命令：*
yum install docker-ce-20.10.2-3.el7 docker-ce-cli-20.10.2-3.el7 containerd.io docker-compose-plugin -y

*#对应k8s 1.20.1的Docker版本19.03, 3:19.03.0-3.el7*
yum install docker-ce-19.03.0-3.el7 docker-ce-cli-19.03.0-3.el7 containerd.io docker-compose-plugin -y

#### 修正Docker的CGroup驱动
cat <<EOF> /etc/docker/daemon.json 
{
  "exec-opts": ["native.cgroupdriver=systemd"]
}
EOF

#### 启用
systemctl start docker
systemctl enable docker

### Kubernetes
#### 配置K8s仓库
cat <<EOF | sudo tee /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=http://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=0
gpgkey=http://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg http://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
exclude=kubelet kubeadm kubectl
EOF

#### 安装K8s组件
yum install -y kubelet-1.21.1-0 kubeadm-1.21.1-0 kubectl-1.21.1-0 --disableexcludes=kubernetes

*#如果安装1.20.1*
yum install -y kubelet-1.20.1-0 kubeadm-1.20.1-0 kubectl-1.20.1-0 --disableexcludes=kubernetes

#### 启动kubelet
systemctl enable --now kubelet



# 控制平面部署
## 预下载Coredns
因为阿里云的服务器上居然没有coredns，要从Docker Hub上下载后改标签
docker pull coredns/coredns:1.8.0
docker tag coredns/coredns:1.8.0 registry.aliyuncs.com/google_containers/coredns:v1.8.0
docker rmi coredns/coredns:1.8.0

## 主节点Master初始化前准备工作

### 输出一个初始化模版配置文件

kubeadm config print init-defaults > initial.yaml

### 修改模版文件中几个重要的Key:Value

advertiseAddress: 192.168.50.101	*#Master的IP*
imageRepository: registry.aliyuncs.com/google_containers 	*#镜像拉取位置*
kubernetesVersion: v1.20.1	*#k8s版本号*
podSubnet: 10.244.0.0/16	*#Pod子网*

### 测试一下配置文件里所配源是否能获取到想要的K8S组件

kubeadm config images list --config initial.yaml

*#如果可以，直接拉下来！*

 kubeadm config images pull --config initial.yaml



## master节点初始化

### 用参数初始化

kubeadm init \
--apiserver-advertise-address=192.168.50.101 \
--image-repository registry.aliyuncs.com/google_containers \
--kubernetes-version v1.20.1 \
--service-cidr=10.96.0.0/12 \
--pod-network-cidr=10.244.0.0/16

### 用配置文件初始化【最优*因为可以慢慢校对】

kubeadm init --config=initial.yaml --upload-certs | tee kubeadm-init.log

## 安装Calico网络
wget https://docs.projectcalico.org/v3.19/manifests/calico.yaml --no-check-certificate

对yaml文件修改以下内容：
- name: CALICO_IPV4POOL_CIDR
 value: "10.244.0.0/16"

对yaml生效：

kubectl apply -f calico.yaml 

## Kubectl的快捷TAB

yum install -y bash-completion

vim /etc/profile
加入以下内容：
source <(kubectl completion bash)

生效一下：
source /etc/profile

创建:
vim /root/.vimrc
set paste

# 监控服务部署
## 拉取镜像
*#因为镜像位置在k8s.gcr.io上，直接设置后面会因为自动部署场景下获取不到，所以要提前从Docker Hub上拉，再打标签伪装，后续的故障处理理由与思路也一样*
**在所有的节点上**
步骤1:拉取国内镜像，如果无效了再找吧
docker pull registry.cn-hangzhou.aliyuncs.com/zailushang/metrics-server:v0.6.0
步骤2:打tag
docker tag registry.cn-hangzhou.aliyuncs.com/zailushang/metrics-server:v0.6.0 k8s.gcr.io/metrics-server/metrics-server:v0.6.0
**在master节点上**
步骤1:下载部署yaml文件
wget https://github.com/kubernetes-sigs/metrics-server/releases/download/v0.6.0/components.yaml
步骤2:对yaml增加一行

```
containers:
      - args:
        - --cert-dir=/tmp
        - --secure-port=4443
        - --kubelet-preferred-address-types=InternalIP,ExternalIP,Hostname
        - --kubelet-use-node-status-port
        - --metric-resolution=15s
        - --kubelet-insecure-tls **就是这一行**
        image: k8s.gcr.io/metrics-server/metrics-server:v0.6.0
        imagePullPolicy: IfNotPresent

```
步骤3:对yaml文件应用生效
kubectl apply -f components.yaml

# 附加工具安装

## kubens & Kubectx

快速切换context和命名空间的第三方工具

```
sudo git clone https://github.com/ahmetb/kubectx /opt/kubectx
sudo ln -s /opt/kubectx/kubectx /usr/local/bin/kubectx
sudo ln -s /opt/kubectx/kubens /usr/local/bin/kubens
```



# 常见故障处理

## coredns状态为ImagePullBackOff问题
kubectl get pods coredns-[实际编号] -n kube-system -o yaml | grep image:
会列出故障pod所需的【image名字】

kubectl get pods coredns-[实际编号] -n kube-system -o wide
会列出故障pod所在的主机名

登录pod所在的宿主机拉取镜像
docker pull coredns/coredns:1.8.0

修改docker的tag，进行伪装
docker tag coredns/coredns:1.8.0 【image名字】

搞定！



# 升级K8S
## 升级顺序要点
1、节点的升级顺序
先升级Master ，再升级Node，如果多台Master，则全部Master升级完毕再升级Node
2、软件的升级顺序
所有类型的节点，都是先升级kubeadm，然后执行kubeadm upgrade，再升级kubelet 和kubectl。
