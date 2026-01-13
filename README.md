<div align="center">

# 🌊 fluid.sh 

### Autonomous AI Agents for Infrastructure

**Make Infrastructure Safe for AI**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Go](https://img.shields.io/badge/Go-1.21+-00ADD8?logo=go)](https://go.dev)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://python.org)
[![React](https://img.shields.io/badge/React-18+-61DAFB?logo=react&logoColor=black)](https://react.dev)

[Features](#-features) • [Quick Start](#-quick-start) • [Demo](#-demo) • [Documentation](#-documentation)

</div>

---

## Problem

AI agents are ready to do infrastructure work, but they can't touch prod:

- Agents can install packages, configure services, write scripts—autonomously
- But one mistake on production and you're getting called at 3 am to fix it
- So we limit agents to chatbots instead of letting them *do the work*
- Containers aren't realistic enough—agents need full OS environments

## Solution

**fluid.sh** lets AI agents work autonomously in isolated VMs, then a human approves before anything touches production:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Autonomous AI Sysadmin Workflow                      │
│                                                                         │
│  ┌─────────┐     ┌─────────────────┐     ┌──────────┐     ┌──────────┐  │
│  │  Agent  │────►│  Sandbox VM     │────►│  Human   │────►│Production│  │
│  │  Task   │     │  (autonomous)   │     │ Approval │     │  Server  │  │
│  └─────────┘     └─────────────────┘     └──────────┘     └──────────┘  │
│                         │                      │                        │
│                    • Full root access     • Review diff                 │
│                    • Install packages     • Approve Ansible             │
│                    • Edit configs         • One-click apply             │
│                    • Run services                                       │
│                    • Snapshot/restore                                   │
└─────────────────────────────────────────────────────────────────────────┘
```

**The agent does real work. The human just approves.**

## Features

| Feature | Description |
|---------|-------------|
|  **Autonomous Execution** | Agents run commands, install packages, edit configs—no hand-holding |
|  **Full VM Isolation** | Each agent gets a dedicated KVM virtual machine with root access |
|  **Snapshot & Restore** | Checkpoint progress, rollback mistakes, branch experiments |
|  **Human-in-the-Loop** | Blocking approval workflow before any production changes |
|  **Diff & Audit Trail** | See exactly what changed, every action logged |
|  **Ansible Export** | Auto-generate playbooks from agent work for production apply |
|  **Tmux Integration** | Watch agent work in real-time, intervene if needed |
|  **Python SDK** | First-class SDK for building autonomous agents |

## Demo

```python
from virsh_sandbox import VirshSandbox

client = VirshSandbox("http://localhost:8080")

# Agent gets its own VM with full root access
sandbox = client.sandbox.create_sandbox(
    source_vm_name="ubuntu-base",
    agent_id="nginx-setup-agent",
    auto_start=True,
    wait_for_ip=True
).sandbox

run_agent("Install nginx and configure TLS, create an Ansible playbook to recreate the task.")

# NOW the human reviews:
# - Diff between snapshots shows exactly what changed
# - Auto-generated Ansible playbook ready to apply
# - Human approves → playbook runs on production
# - Human rejects → nothing happens, agent tries again

# Clean up sandbox
client.sandbox.destroy_sandbox(sandbox.id)
```

## 🏄 Quick Start

### Prerequisites

- **mprocs** - For local dev
- **Docker & Docker Compose** - For containerized deployment in production
- **libvirt/KVM** - For virtual machine management
- **macOS**:
  - **libvirt** - `brew install libvirt`
  - **socket_vmnet** - `brew install socket_vmnet`

### 30-Second Start

```bash
# Clone and start
git clone https://github.com/aspectrr/fluid.sh.git
cd fluid.sh
mprocs

# Services available at:
# API:      http://localhost:8080
# Web UI:   http://localhost:5173
```

---

## Platform Setup

<details>
<summary><b>Mac</b></summary>

You will need to install libvirt and socket_vmnet on Mac:

```bash
# Install Lima and libvirt client
brew install libvirt socket_vmnet

# Set up SSH CA (Needed for Sanbox VMs)
cd fluid.sh
./virsh-sandbox/scripts/setup-ssh-ca.sh --dir .ssh-ca

# Set up libvirt VM (ARM64 Ubuntu)
cd fluid.sh
./virsh-sandbox/scripts/reset-libvirt-macos.sh

# Verify connection
virsh -c "$LIBVIRT_URI" list --all

# Start services
mprocs
```

**What happens:**
1. A SSH CA is generated and then is used to build the golden VM
2. libvirt runs on the machine and is queried by the virsh-sandbox API
4. Test VMs run on your root machine

**Architecture:**
```
┌─────────────────────────────────────────────────────────────────────┐
│                     Apple Silicon Mac                               │
│  ┌─────────────────┐                                                │
│  │ virsh-sandbox   │                                                │
│  │ API + Web UI    │────►  ┌──────────────────────────────────┐     │
│  │                 │       │     libvirt/QEMU (ARM64)         │     │
│  │ LIBVIRT_URI=    │       │  ┌──────────┐  ┌──────────┐      │     │
│  │ qemu+tcp://     │       │  │ sandbox  │  │ sandbox  │ ...  │     │
│  │ localhost:16509 │       │  │ VM (arm) │  │ VM (arm) │      │     │
│  └─────────────────┘       │  └──────────┘  └──────────┘      │     │
│                            └──────────────────────────────────┘     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Create ARM64 test VMs:**
```bash
./virsh-sandbox/scripts/reset-libvirt-macos.sh
```

**Default test VM credentials:**
- Username: `testuser` / Password: `testpassword`
- Username: `root` / Password: `rootpassword`

</details>

<details>
<summary><b>Linux x86_64 (On-Prem / Bare Metal)</b></summary>

Direct libvirt access for best performance:

```bash
# Install libvirt and dependencies (Ubuntu/Debian)
sudo apt update
sudo apt install -y \
    qemu-kvm qemu-utils libvirt-daemon-system \
    libvirt-clients virtinst bridge-utils ovmf \
    cpu-checker cloud-image-utils genisoimage

# Or on Fedora/RHEL
sudo dnf install -y \
    qemu-kvm qemu-img libvirt libvirt-client \
    virt-install bridge-utils edk2-ovmf \
    cloud-utils genisoimage

# Enable and start libvirtd
sudo systemctl enable --now libvirtd

# Add your user to libvirt group
sudo usermod -aG libvirt,kvm $(whoami)
newgrp libvirt  # or log out and back in

# Verify KVM is available
kvm-ok

# Create image directories
sudo mkdir -p /var/lib/libvirt/images/{base,jobs}

# Create environment file
cat > .env << 'EOF'
LIBVIRT_URI=qemu:///system
LIBVIRT_NETWORK=default
DATABASE_URL=postgresql://virsh_sandbox:virsh_sandbox@localhost:5432/virsh_sandbox
BASE_IMAGE_DIR=/var/lib/libvirt/images/base
SANDBOX_WORKDIR=/var/lib/libvirt/images/jobs
EOF

# Start the default network
sudo virsh net-autostart default
sudo virsh net-start default

# Verify
virsh -c qemu:///system list --all

# Start services
docker-compose up --build
```

**Architecture:**
```
┌─────────────────────────────────────────────────────────────────────┐
│                    Linux x86_64 Host                                │
│                                                                     │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────┐  │
│  │ virsh-sandbox   │  │   PostgreSQL    │  │    Web UI           │  │
│  │ API (Go)        │  │   (Docker)      │  │    (React)          │  │
│  │ :8080           │  │   :5432         │  │    :5173            │  │
│  └────────┬────────┘  └─────────────────┘  └─────────────────────┘  │
│           │                                                         │
│           │ LIBVIRT_URI=qemu:///system                              │
│           ▼                                                         │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                    libvirt/KVM (native)                      │   │
│  │                                                              │   │
│  │   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │   │
│  │   │  sandbox-1   │  │  sandbox-2   │  │  sandbox-N   │  ...  │   │
│  │   │  (x86_64)    │  │  (x86_64)    │  │  (x86_64)    │       │   │
│  │   └──────────────┘  └──────────────┘  └──────────────┘       │   │
│  └──────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

**Create a base VM image:**
```bash
# Download Ubuntu cloud image
cd /var/lib/libvirt/images/base
sudo wget https://cloud-images.ubuntu.com/jammy/current/jammy-server-cloudimg-amd64.img

# Create test VM using the provided script
./virsh-sandbox/scripts/setup-ssh-ca.sh --dir [ssh-ca-dir]
./virsh-sandbox/scripts/reset-libvirt-macos.sh [vm-name] [ca-pub-path] [ca-key-path]
```

**Default test VM credentials:**
- Username: `testuser` / Password: `testpassword`
- Username: `root` / Password: `rootpassword`

</details>

<details>
<summary><b>Linux ARM64 (Ampere, Graviton, Raspberry Pi)</b></summary>

Native ARM64 Linux with libvirt:

```bash
# Install libvirt and dependencies (Ubuntu/Debian ARM64)
sudo apt update
sudo apt install -y \
    qemu-kvm qemu-utils qemu-efi-aarch64 \
    libvirt-daemon-system libvirt-clients \
    virtinst bridge-utils cloud-image-utils genisoimage

# Enable and start libvirtd
sudo systemctl enable --now libvirtd

# Add your user to libvirt group
sudo usermod -aG libvirt,kvm $(whoami)
newgrp libvirt

# Create environment file
cat > .env << 'EOF'
LIBVIRT_URI=qemu:///system
LIBVIRT_NETWORK=default
DATABASE_URL=postgresql://virsh_sandbox:virsh_sandbox@localhost:5432/virsh_sandbox
BASE_IMAGE_DIR=/var/lib/libvirt/images/base
SANDBOX_WORKDIR=/var/lib/libvirt/images/jobs
EOF

# Start the default network
sudo virsh net-autostart default
sudo virsh net-start default

# Start services
docker-compose up --build
```

**Download ARM64 cloud images:**
```bash
cd /var/lib/libvirt/images/base
sudo wget https://cloud-images.ubuntu.com/jammy/current/jammy-server-cloudimg-arm64.img
```

**Architecture is the same as x86_64 but with ARM64 VMs.**

**Default test VM credentials:**
- Username: `testuser` / Password: `testpassword`
- Username: `root` / Password: `rootpassword`

</details>

<details>
<summary><b>Remote libvirt Server</b></summary>

Connect to a remote libvirt host over SSH or TCP:

```bash
# SSH connection (recommended - secure)
export LIBVIRT_URI="qemu+ssh://user@remote-host/system"

# Or with specific SSH key
export LIBVIRT_URI="qemu+ssh://user@remote-host/system?keyfile=/path/to/key"

# TCP connection (less secure - ensure network is trusted)
export LIBVIRT_URI="qemu+tcp://remote-host:16509/system"

# Test connection
virsh -c "$LIBVIRT_URI" list --all

# Create .env file
cat > .env << EOF
LIBVIRT_URI=${LIBVIRT_URI}
LIBVIRT_NETWORK=default
DATABASE_URL=postgresql://virsh_sandbox:virsh_sandbox@localhost:5432/virsh_sandbox
EOF

# Start services
docker-compose up --build
```

**Remote server setup (on the libvirt host):**
```bash
# For SSH access, ensure SSH is enabled and user has libvirt access
sudo usermod -aG libvirt remote-user

# For TCP access (development only!), configure /etc/libvirt/libvirtd.conf:
#   listen_tls = 0
#   listen_tcp = 1
#   auth_tcp = "none"  # WARNING: No authentication!
# Then restart: sudo systemctl restart libvirtd
```

</details>

---

## Project Structure

```
virsh-sandbox/
├── virsh-sandbox/          #    Main API server (Go)
│   ├── cmd/api/            #    Entry point
│   ├── internal/           #    Business logic
│   └── scripts/            #    Setup scripts
├── web/                    #    React frontend
│   └── src/                #    Components, hooks, routes
├── sdk/                    #    Python SDK
│   └── virsh-sandbox-py/   #    Auto-generated client
├── examples/               #    Example implementations
│   └── agent-example/      #    AI agent with OpenAI
└── docker-compose.yml      #    Container orchestration
```

## API Reference


### Sandbox Lifecycle

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/v1/sandboxes` | Create a new sandbox |
| `GET` | `/v1/sandboxes/{id}` | Get sandbox details |
| `POST` | `/v1/sandboxes/{id}/start` | Start a sandbox |
| `POST` | `/v1/sandboxes/{id}/stop` | Stop a sandbox |
| `DELETE` | `/v1/sandboxes/{id}` | Destroy a sandbox |

### Command Execution

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/v1/sandboxes/{id}/command` | Run SSH command |
| `POST` | `/api/v1/tmux/panes/send-keys` | Send keystrokes to tmux |
| `POST` | `/api/v1/tmux/panes/read` | Read tmux pane content |

### Snapshots

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/v1/sandboxes/{id}/snapshots` | Create snapshot |
| `GET` | `/v1/sandboxes/{id}/snapshots` | List snapshots |
| `POST` | `/v1/sandboxes/{id}/snapshots/{name}/restore` | Restore snapshot |

### Human Approval

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/human/ask` | Request approval (blocking) |

## Security Model

### Isolation Layers

1. **VM Isolation** - Each sandbox is a separate KVM virtual machine
2. **Network Isolation** - VMs run on isolated virtual networks
3. **SSH Certificates** - Ephemeral credentials that auto-expire (1-10 minutes)
4. **Human Approval** - Gate sensitive operations

### Safety Features

-  Command allowlists/denylists
-  Path restrictions for file access
-  Timeout limits on all operations
-  Output size limits
-  Full audit trail
-  Snapshot rollback

##  Documentation

- [Docs from Previous Issues](./docs/) - Documentation on common issues working with the project
- [Scripts Reference](./virsh-sandbox/scripts/README.md) - Setup and utility scripts
- [SSH Certificates](./virsh-sandbox/scripts/README.md#ssh-certificate-based-access) - Ephemeral credential system
- [Agent Connection Flow](./docs/agent-connection-flow.md) - How agents connect to sandboxes
- [Examples](./examples/) - Working examples

## Development

To run the API locally, first build the `virsh-sandbox` binary:

```bash
# Build the API binary
cd virsh-sandbox && make build
```

Then, use `mprocs` to run all the services together for local development.

```bash
# Install mprocs for multi-service development
brew install mprocs  # macOS
cargo install mprocs # Linux

# Start all services with hot-reload
mprocs

# Or run individual services
cd virsh-sandbox && make run
cd web && bun run dev
```

### Running Tests

```bash
# Go services
(cd virsh-sandbox && make test)

# Python SDK
(cd sdk/virsh-sandbox-py && pytest)

# All checks
(cd virsh-sandbox && make check)
```

##  Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Run `make check` 
5. Submit a pull request

All contributions must maintain the security model and include appropriate tests.

## License

MIT License - see [LICENSE](LICENSE) for details.

---

<div align="center">

Made with ❤️

</div>
